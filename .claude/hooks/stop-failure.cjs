#!/usr/bin/env node
'use strict';

// StopFailure hook for Claude Code.
// Registered under StopFailure — fires when a turn ends due to an API error
// (rate limits, auth errors, etc.). Complements circuit-breaker.cjs which
// handles tool-level failures (PostToolUseFailure).
//
// On API failure:
//   1. Detects failure type (rate limit, auth, other)
//   2. Appends structured entry to state/agent_log.md
//   3. Triggers graceful state commit via scripts/commit-state.sh

const fs = require('fs');
const path = require('path');

const REPO_ROOT = path.resolve(__dirname, '..', '..');
const AGENT_LOG = path.join(REPO_ROOT, 'state', 'agent_log.md');
const COMMIT_SCRIPT = path.join(REPO_ROOT, 'scripts', 'commit-state.sh');

// Safety timeout — never hang the agent (5s)
setTimeout(() => process.exit(0), 5000);

function classifyError(data) {
  const message = (data.error || data.message || '').toLowerCase();
  const status = data.status_code || data.status || 0;

  if (status === 429 || message.includes('rate limit') || message.includes('rate_limit')) {
    return 'rate-limit';
  }
  if (status === 401 || status === 403 || message.includes('auth') || message.includes('unauthorized') || message.includes('forbidden')) {
    return 'auth-failure';
  }
  if (status === 529 || message.includes('overloaded')) {
    return 'overloaded';
  }
  return 'api-error';
}

function timestamp() {
  return new Date().toISOString().replace('T', ' ').replace(/\.\d{3}Z$/, 'Z');
}

function appendLog(failureType, detail) {
  try {
    const entry = `${timestamp()} | stop-failure hook | ${failureType} | ${detail}\n`;
    fs.appendFileSync(AGENT_LOG, entry);
  } catch {
    // Silently fail — must not block agent
  }
}

function tryCommitState(failureType) {
  try {
    if (fs.existsSync(COMMIT_SCRIPT)) {
      const { execSync } = require('child_process');
      execSync(`bash "${COMMIT_SCRIPT}" "state: graceful save — ${failureType} triggered StopFailure"`, {
        cwd: REPO_ROOT,
        timeout: 10000,
        stdio: 'ignore'
      });
    }
  } catch {
    // Silently fail — best-effort commit
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
}

function handleInput(rawInput) {
  let data;
  try {
    data = JSON.parse(rawInput);
  } catch {
    // If we can't parse input, still log the failure
    appendLog('unknown', 'StopFailure fired but input was not parseable JSON');
    return;
  }

  const failureType = classifyError(data);
  const detail = (data.error || data.message || 'no detail').substring(0, 200);

  // Log the failure
  appendLog(failureType, detail);

  // Emit guidance to stdout (agent sees this)
  const guidance = {
    'rate-limit': 'API rate limit hit. State has been saved. The agent should wind down gracefully or wait before retrying.',
    'auth-failure': 'API auth failure. State has been saved. Check CLAUDE_CODE_OAUTH_TOKEN or ANTHROPIC_API_KEY configuration.',
    'overloaded': 'API overloaded. State has been saved. The agent should reduce scope or retry later.',
    'api-error': 'API error encountered. State has been saved. The agent should wind down gracefully.'
  };
  process.stdout.write('STOP-FAILURE: ' + guidance[failureType]);

  // Best-effort commit of current state before exit
  tryCommitState(failureType);
}

main();
