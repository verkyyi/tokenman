import { defineCollection, z } from 'astro:content';

const projects = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    status: z.enum(['active', 'maintained', 'archived', 'experiment']),
    description: z.string(),               // one sentence — agent writes this
    longDescription: z.string().optional(), // agent-written from README
    url: z.string().url().optional(),       // live URL if any
    github: z.string().url(),              // repo URL — always present
    stars: z.number().default(0),          // synced daily by maintenance.yml
    language: z.string(),                  // primary language
    tags: z.array(z.string()).default([]), // from GitHub topics
    featured: z.boolean().default(false),  // you control this manually
    agent_written: z.boolean().default(true),
    last_synced: z.string(),               // ISO date
  }),
});

const posts = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    published: z.string(),                 // ISO date from RSS
    url: z.string().url(),                 // link to original post
    source: z.string().optional(),         // blog name / platform
    agent_synced: z.boolean().default(true),
  }),
});

export const collections = { projects, posts };
