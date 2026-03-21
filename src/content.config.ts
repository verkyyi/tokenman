import { defineCollection, z } from 'astro:content';

const codex = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.string(),
    description: z.string(),
    tags: z.array(z.string()).default([]),
  }),
});

export const collections = { codex };
