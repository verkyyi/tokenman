// src/pages/api/profile.json.ts
// Serves content/profile.json as a static endpoint.
// Agents and other tools can query /api/profile.json to read
// your structured profile data without scraping HTML.

import type { APIRoute } from 'astro';
import { readFileSync } from 'fs';
import { join } from 'path';

export const GET: APIRoute = () => {
  const profile = JSON.parse(
    readFileSync(join(process.cwd(), 'content/profile.json'), 'utf-8')
  );

  // Remove internal comment field before serving
  const { _comment, ...publicProfile } = profile;

  return new Response(JSON.stringify(publicProfile, null, 2), {
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
    },
  });
};
