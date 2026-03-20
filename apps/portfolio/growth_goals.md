# Growth Goals
# Set your targets. The growth agent measures weekly and updates
# the "current" values. Never delete a goal — archive with [achieved].
# growth.yml reads this file every Monday and writes state/growth_report.md.

## Traffic
target_monthly_visitors: 500
current: 0
trend: —
notes: Starting from zero. First goal is consistent weekly visits.

## GitHub
target_agentfolio_stars: 100
current: 0
target_profile_repo_stars: 50
current_profile_repo_stars: 0

## AI Discoverability
target_ai_crawler_visits_week: 20
current: 0
notes: Tracked via GitHub Pages analytics + referrer data

## SEO
target_lighthouse_performance: 95
current: 0
target_lighthouse_accessibility: 95
current_accessibility: 0

## Content
target_projects_showcased: 5
current: 0
target_blog_posts_synced: 3
current: 0

## Notes for Growth Agent
When analyzing metrics, prioritize in this order:
1. Fix any Lighthouse scores below target first (technical SEO)
2. Ensure all content is fresh (< 30 days since last sync)
3. Draft distribution content for any major recent work
4. Report on AI crawler visits as a discoverability signal
