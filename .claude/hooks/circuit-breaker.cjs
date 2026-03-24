#!/usr/bin/env node
'use strict';

// Circuit breaker hook for Claude Code.
// Registered under PostToolUseFailure (track failures) and PostToolUse (reset on success).
// Tracks consecutive failures and escalates intervention messages,
// mechanically enforcing "Do NOT retry more than once automatically."
//
// Complements guard.sh (prevents bad actions) with failure recovery
// (prevents repetitive failure loops).

const fs = require('fs');
const path = require('path');

const STATE_FILE = path.join(__dirname, '..', 'circuit-breaker-state.json');
const CONSECUTIVE_THRESHOLD = 3;
const LIFETIME_TRIP_THRESHOLD = 5;

function readState() {
  try {
    return JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
  } catch {
    return { consecutive: 0, lifetimeTrips: 0, sessionId: null };
  }
}

function writeState(state) {
  try {
    fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2) + '\n');
  } catch {
    // Silently fail — must not block agent
  }
}

function main() {
  let input = '';

  process.stdin.setEncoding('utf8');
  process.stdin.on('data', (chunk) => { input += chunk; });
  process.stdin.on('end', () => {
    try {
      handleInput(input);
    } catch {
      // Must not block agent operation
    }
    process.exit(0);
  });

  // Safety timeout — never hang
  setTimeout(() => process.exit(0), 5000);
}

function handleInput(rawInput) {
  let data;
  try {
    data = JSON.parse(rawInput);
  } catch {
    return;
  }

  const state = readState();
  const sessionId = data.session_id || null;

  // Reset on new session
  if (sessionId && state.sessionId !== sessionId) {
    state.consecutive = 0;
    state.lifetimeTrips = 0;
    state.sessionId = sessionId;
  }

  // Determine if this is a failure event.
  // PostToolUseFailure provides error context; PostToolUse does not.
  const isFailure = !!(data.error || data.tool_error);

  if (!isFailure) {
    // Successful tool use — reset consecutive counter
    if (state.consecutive > 0) {
      state.consecutive = 0;
      writeState(state);
    }
    return;
  }

  // Failure — increment consecutive counter
  state.consecutive++;

  // Check if we hit the consecutive threshold (trip the breaker)
  if (state.consecutive >= CONSECUTIVE_THRESHOLD) {
    const failCount = state.consecutive;
    state.lifetimeTrips++;
    state.consecutive = 0; // Reset after trip

    if (state.lifetimeTrips >= LIFETIME_TRIP_THRESHOLD) {
      process.stdout.write(
        'CIRCUIT BREAKER (hard): ' + state.lifetimeTrips + ' trip(s) this session. ' +
        'STOP. You are in a failure loop. Step back and rethink your entire approach. ' +
        'Re-read the error messages from scratch and try a fundamentally different strategy.'
      );
    } else {
      process.stdout.write(
        'CIRCUIT BREAKER: ' + failCount + ' consecutive failures detected. ' +
        'The current approach is not working. Try a different strategy — ' +
        'read the error message carefully and adjust your approach.'
      );
    }
  }

  writeState(state);
}

main();
