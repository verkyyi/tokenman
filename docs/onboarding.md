# Onboarding Guide

Get your living portfolio running in ~5 minutes.
No terminal required.

## Prerequisites
- A GitHub account
- An Anthropic API key ([get one here](https://console.anthropic.com))

---

## Step 1 — Create your repo from the template

1. Go to [github.com/yourusername/agentfolio](https://github.com/yourusername/agentfolio)
2. Click **"Use this template"** → **"Create a new repository"**
3. Name it anything (e.g. `portfolio`, `agentfolio`, your username)
4. Choose Public or Private — your choice

---

## Step 2 — Add your Anthropic API key

1. In your new repo, go to **Settings** → **Secrets and variables** → **Actions**
2. Click **"New repository secret"**
3. Name: `ANTHROPIC_API_KEY`
4. Value: your `sk-ant-...` key
5. Click **"Add secret"**

That's the only secret needed. `GITHUB_TOKEN` is automatic.

---

## Step 3 — Enable GitHub Pages

1. In your repo, go to **Settings** → **Pages**
2. Under **Source**, select **"GitHub Actions"**
3. Don't configure anything else yet

---

## Step 4 — Run the onboard workflow

1. In your repo, go to **Actions**
2. In the left sidebar, click **"Onboard"**
3. Click **"Run workflow"** (top right of the workflow list)
4. Fill in the inputs:
   - **GitHub username**: your GitHub username (required)
   - **Blog RSS URL**: your blog's RSS feed URL (optional)
   - **Custom domain**: if you have one, e.g. `https://lee.dev` (optional)
5. Click **"Run workflow"**

The workflow will take 3-5 minutes. You can watch it run in the
Actions tab. When it completes, it automatically triggers a deployment.

---

## Step 5 — View your live profile

Once the deploy workflow completes (1-2 min after onboard):

**Default URL:** `https://[your-github-username].github.io/[repo-name]`

If you set a custom domain in Step 4, you'll need to configure DNS:
- Add a CNAME record pointing to `[username].github.io`
- Add the domain in Settings → Pages → Custom domain

---

## What just happened

The onboard workflow:
1. Fetched your GitHub profile (bio, location, links)
2. Fetched all your public repos (names, stars, languages, topics)
3. Read the README of your top repos
4. Claude wrote content files for each repo
5. Claude wrote your `profile.json`, `llms.txt`, and constitution
6. Committed everything → deploy fired → your profile is live

---

## After onboarding

The agent works automatically from this point:

| When | What happens |
|------|-------------|
| Every day at 3am UTC | Syncs repo stars, checks for new repos, fixes broken links |
| Every Monday 6am UTC | Writes weekly growth report, runs SEO audit |
| When you push to main | Rebuilds and deploys your profile |
| When a feedback issue is opened | Triage agent classifies within minutes |
| When a bug is triaged | Coder agent opens a fix PR |

---

## Customizing your profile

### Change your bio or availability
Edit `content/profile.json` directly in GitHub UI (pencil icon).
Push to main → deploy fires automatically.

Or tell Claude via the manual task workflow:
1. Actions → "Claude Task (Manual)" → "Run workflow"
2. Prompt: `Update my availability to "busy" and change bio to "[new bio]"`

### Feature a project
Edit the project's `.md` file in `content/projects/`, set `featured: true`.
Push → redeploy.

### Add a custom link
Edit `content/profile.json`, add to the `links` array:
```json
"links": [
  {"label": "Twitter", "url": "https://twitter.com/username"}
]
```

### Adjust growth targets
Edit `apps/portfolio/growth_goals.md` directly.
The growth workflow reads this file every Monday.

---

## Using the manual task channel

The `claude-task.yml` workflow is your dev channel.
No Telegram, no terminal — just GitHub Actions.

1. Go to **Actions** → **"Claude Task (Manual)"**
2. Click **"Run workflow"**
3. Type your instruction in the **"What should Claude do?"** field
4. Toggle **"Open a PR instead?"** if you want to review before it goes live
5. Click **"Run workflow"**

Examples:
- `"Add my new aInbox project to the portfolio with a featured badge"`
- `"The skills section looks outdated, refresh it from my recent repos"`
- `"Update my availability to open for consulting"`

---

## Using the plugin in an existing project

If you have an existing Astro project and want to add the harness:

```bash
npx @agentfolio/plugin
```

Then:
1. Create `apps/[your-app]/CLAUDE.md` with project-specific rules
2. Update `APP_NAME` in each workflow file
3. Add `ANTHROPIC_API_KEY` secret
4. Enable Pages
5. Run `onboard.yml`

---

## Troubleshooting

**Onboard workflow fails:**
- Check that `ANTHROPIC_API_KEY` is set correctly in secrets
- Check Actions tab for the specific error message
- If the API key is correct, try running it again (transient failures happen)

**Profile not showing at expected URL:**
- Wait 2-3 minutes after the deploy workflow completes
- Check Settings → Pages for the exact published URL
- Make sure Pages source is set to "GitHub Actions" not a branch

**Agent isn't fixing my feedback issues:**
- Feedback issues must have the `feedback` label to trigger triage
- Check that triage.yml ran (look in Actions tab)
- If the issue was labeled `agent-ready`, coder.yml should have fired

**Workflow not finding Claude Code:**
- Check that `ANTHROPIC_API_KEY` is not expired or rate-limited
- Check the Actions logs for specific error messages

---

## Further reading

- [Harness philosophy](./harness-philosophy.md) — why the system works this way
- [Customizing](./customizing.md) — replacing the portfolio with your own app
- [EC2 mode](./ec2-mode.md) — for advanced users who need real-time features
