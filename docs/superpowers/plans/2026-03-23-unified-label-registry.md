# Unified Label Registry Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace distributed label creation with a single `.github/labels.yml` registry synced by a dedicated workflow.

**Architecture:** A flat YAML file defines all 19 labels. A standalone workflow parses the file and runs `gh label create --force` for each entry. The old "Ensure labels exist" step in evolve.yml is deleted, and all `project:*` label references are removed from workflow prompts.

**Tech Stack:** GitHub Actions, `yq`, `gh` CLI

**Spec:** `docs/superpowers/specs/2026-03-23-unified-label-registry-design.md`

---

## File Structure

| Action | File | Responsibility |
|--------|------|----------------|
| Create | `.github/labels.yml` | Single source of truth for all labels |
| Create | `.github/workflows/sync-labels.yml` | Syncs labels.yml to GitHub on push/schedule/dispatch |
| Modify | `.github/workflows/evolve.yml` | Remove "Ensure labels exist" step + `project:*` refs |
| Modify | `.github/workflows/watcher.yml` | Remove `project:*` refs from prompt |
| Modify | `.github/workflows/growth.yml` | Remove `project:*` refs from prompt |
| Modify | `.github/workflows/triage.yml` | Remove `project:*` refs from prompt |
| Modify | `.github/workflows/feedback-learner.yml` | Remove `project:*` refs from prompt + `--label` flag |
| Modify | `CLAUDE.md` | Remove `project:*` from APP_NAME Resolution |

---

### Task 1: Create the label registry file

**Files:**
- Create: `.github/labels.yml`

- [ ] **Step 1: Create `.github/labels.yml`**

```yaml
# .github/labels.yml — single source of truth for all GitHub labels
# Synced by .github/workflows/sync-labels.yml
# To add a label: add an entry here and push to main.

# --- Pipeline status ---
- name: agent-ready
  color: "0e8a16"
  description: Ready for coder agent

- name: needs-human
  color: "d93f0b"
  description: Requires human action (external platform, secrets, permissions)

- name: needs-review
  color: "fbca04"
  description: Needs human review

- name: likely-agent-fixable
  color: "0e8a16"
  description: Watcher determined this pipeline issue can be fixed by the coder agent

- name: human-wip
  color: "d93f0b"
  description: Human is actively working on this issue

# --- Pipeline origin ---
- name: evolve-finding
  color: "7057ff"
  description: Issue created by evolve.yml

- name: pipeline-fix
  color: "d73a4a"
  description: Pipeline failure to fix

- name: adopter-insight
  color: "1d76db"
  description: Pattern found from adopter usage

- name: intent-driven
  color: "5319e7"
  description: Issue driven by human intent analysis

# --- Issue type ---
- name: bug
  color: "d73a4a"
  description: Something isn't working

- name: feature
  color: "a2eeef"
  description: New feature request

- name: question
  color: "d876e3"
  description: Further information is requested

- name: ux-request
  color: "e4e669"
  description: UX improvement suggestion

- name: growth-action
  color: "0075ca"
  description: Growth and distribution action

- name: positive
  color: "0e8a16"
  description: Positive feedback

- name: spam
  color: "e4e669"
  description: Spam or irrelevant

# --- Workflow meta ---
- name: auto-merge
  color: "0e8a16"
  description: PR approved for automatic merge

- name: agent-error
  color: "d73a4a"
  description: Issue created by agent failure handling

- name: feedback
  color: "1d76db"
  description: User feedback
```

- [ ] **Step 2: Commit**

```bash
git add .github/labels.yml
git commit -m "feat(harness): add label registry — single source of truth for all GitHub labels"
```

---

### Task 2: Create the sync workflow

**Files:**
- Create: `.github/workflows/sync-labels.yml`

- [ ] **Step 1: Create `.github/workflows/sync-labels.yml`**

```yaml
name: Sync Labels

on:
  push:
    branches: [main]
    paths: ['.github/labels.yml']
  schedule:
    - cron: '0 0 * * 1'  # weekly Monday midnight UTC
  workflow_dispatch:
    inputs:
      prune:
        description: 'Delete labels not in registry'
        required: false
        default: 'false'
        type: choice
        options: ['false', 'true']

permissions:
  issues: write

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install yq
        run: |
          sudo wget -qO /usr/local/bin/yq https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64
          sudo chmod +x /usr/local/bin/yq

      - name: Sync labels
        run: |
          COUNT=$(yq '. | length' .github/labels.yml)
          for i in $(seq 0 $(( COUNT - 1 ))); do
            NAME=$(yq ".[$i].name" .github/labels.yml)
            COLOR=$(yq ".[$i].color" .github/labels.yml)
            DESC=$(yq ".[$i].description" .github/labels.yml)
            echo "Syncing label: $NAME"
            gh label create "$NAME" --color "$COLOR" --description "$DESC" --force
          done
        env:
          GH_TOKEN: ${{ github.token }}

      - name: Prune unlisted labels
        if: inputs.prune == 'true'
        run: |
          # Get labels from registry
          REGISTRY=$(yq '.[].name' .github/labels.yml)

          # Get labels from GitHub
          GITHUB_LABELS=$(gh label list --limit 200 --json name -q '.[].name')

          # Delete labels not in registry
          while IFS= read -r label; do
            if ! echo "$REGISTRY" | grep -qxF "$label"; then
              echo "Pruning label: $label"
              gh label delete "$label" --yes
            fi
          done <<< "$GITHUB_LABELS"
        env:
          GH_TOKEN: ${{ github.token }}
```

- [ ] **Step 2: Commit**

```bash
git add .github/workflows/sync-labels.yml
git commit -m "feat(harness): add sync-labels workflow — syncs .github/labels.yml to GitHub"
```

---

### Task 3: Remove "Ensure labels exist" step from evolve.yml

**Files:**
- Modify: `.github/workflows/evolve.yml:448-460`

- [ ] **Step 1: Delete the "Ensure labels exist" step**

Remove lines 448-460 from evolve.yml:
```
      - name: Ensure labels exist
        run: |
          gh label create "evolve-finding" --color "7057ff" --description "Issue created by evolve.yml" --force
          gh label create "pipeline-fix" --color "d73a4a" --description "Pipeline failure to fix" --force
          gh label create "adopter-insight" --color "1d76db" --description "Pattern found from adopter usage" --force
          gh label create "intent-driven" --color "5319e7" --description "Issue driven by human intent analysis" --force
          gh label create "agent-ready" --color "0e8a16" --description "Ready for coder agent" --force
          gh label create "needs-review" --color "fbca04" --description "Needs human review" --force
          gh label create "likely-agent-fixable" --color "0e8a16" --description "Watcher determined this pipeline issue can be fixed by the coder agent" --force
          REPO_NAME=$(echo "$GITHUB_REPOSITORY" | cut -d/ -f2)
          gh label create "project:${REPO_NAME}" --color "c5def5" --description "${REPO_NAME} project" --force
        env:
          GH_TOKEN: ${{ github.token }}
```

- [ ] **Step 2: Commit**

```bash
git add .github/workflows/evolve.yml
git commit -m "fix(workflow): remove label creation from evolve.yml — now managed by sync-labels"
```

---

### Task 4: Remove `project:*` references from evolve.yml prompts

**Files:**
- Modify: `.github/workflows/evolve.yml:126,239`

- [ ] **Step 1: Edit line ~126 (PIPELINE WATCH posture)**

Change:
```
`gh issue create --title "[pipeline] Brief description" --body "..." --label "pipeline-fix,project:$(echo $GITHUB_REPOSITORY | cut -d/ -f2)"`
```
To:
```
`gh issue create --title "[pipeline] Brief description" --body "..." --label "pipeline-fix"`
```

- [ ] **Step 2: Edit line ~239 (Issue Creation section)**

Change:
```
intent-driven (human intent) + project:$(echo $GITHUB_REPOSITORY | cut -d/ -f2)
```
To:
```
intent-driven (human intent)
```

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/evolve.yml
git commit -m "fix(workflow): remove project:* label refs from evolve.yml prompts"
```

---

### Task 5: Remove `project:*` references from watcher.yml

**Files:**
- Modify: `.github/workflows/watcher.yml:176-177,204,233`

- [ ] **Step 1: Edit lines ~176-177 (issue creation instructions)**

Change:
```
- Create issue: use the project label from the Evolve Config (e.g., `project:<reponame>`) — not `project:scaffold`
  e.g.: gh issue create --title "[pipeline] ..." --body "..." --label "pipeline-fix,project:<reponame>"
```
To:
```
- Create issue with appropriate labels
  e.g.: gh issue create --title "[pipeline] ..." --body "..." --label "pipeline-fix"
```

- [ ] **Step 2: Edit line ~204 (label flag)**

Change:
```
--label "pipeline-fix,project:<reponame from Evolve Config>"
```
To:
```
--label "pipeline-fix"
```

- [ ] **Step 3: Edit line ~233 (project name instruction)**

Delete the line:
```
Use the project name from the config for labels (not "project:scaffold").
```

- [ ] **Step 4: Commit**

```bash
git add .github/workflows/watcher.yml
git commit -m "fix(workflow): remove project:* label refs from watcher.yml"
```

---

### Task 6: Remove `project:*` references from growth.yml

**Files:**
- Modify: `.github/workflows/growth.yml:146,188`

- [ ] **Step 1: Edit line ~146 (label instruction)**

Change:
```
- Label: use the project label from the Evolve Config (e.g., `growth-action,needs-review,project:<reponame>`)
```
To:
```
- Label: `growth-action,needs-review`
```

- [ ] **Step 2: Edit line ~188 (project name instruction)**

Delete the line:
```
Use the project name from the config for labels (not "project:scaffold").
```

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/growth.yml
git commit -m "fix(workflow): remove project:* label refs from growth.yml"
```

---

### Task 7: Remove `project:*` references from triage.yml

**Files:**
- Modify: `.github/workflows/triage.yml:59,64`

- [ ] **Step 1: Edit line ~59**

Delete the line:
```
Use the project name from the config for labels (not "project:scaffold").
```

- [ ] **Step 2: Edit line ~64**

Delete the line:
```
Use the repo name as the project label (e.g., \`project:<reponame>\`) instead of hardcoding \`project:scaffold\`.
```

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/triage.yml
git commit -m "fix(workflow): remove project:* label refs from triage.yml"
```

---

### Task 8: Remove `project:*` references from feedback-learner.yml

**Files:**
- Modify: `.github/workflows/feedback-learner.yml:119,275`

- [ ] **Step 1: Edit line ~119 (project name instruction)**

Delete the line:
```
Use the project name from the config for labels (not "project:scaffold").
```

- [ ] **Step 2: Edit line ~275 (label flag in gh issue create)**

Change:
```
--label "agent-ready,project:$(gh repo view --json name -q .name)" \
```
To:
```
--label "agent-ready" \
```

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/feedback-learner.yml
git commit -m "fix(workflow): remove project:* label refs from feedback-learner.yml"
```

---

### Task 9: Remove `project:*` references from analyze.yml

**Files:**
- Modify: `.github/workflows/analyze.yml:64`

- [ ] **Step 1: Edit line ~64 (project name instruction)**

Delete the line:
```
Use the project name from the config for labels (not "project:scaffold").
```

- [ ] **Step 2: Commit**

```bash
git add .github/workflows/analyze.yml
git commit -m "fix(workflow): remove project:* label refs from analyze.yml"
```

---

### Task 10: Update CLAUDE.md

**Files:**
- Modify: `CLAUDE.md:23-24`

- [ ] **Step 1: Edit APP_NAME Resolution section**

Change:
```
1. Issue/PR-triggered (triage, coder, reviewer): read from issue/PR
   label (e.g., project:profile, project:scaffold). Default: scaffold.
```
To:
```
1. Issue/PR-triggered (triage, coder, reviewer): read from issue/PR metadata. Default: scaffold.
```

- [ ] **Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: remove project:* label pattern from CLAUDE.md"
```

---

### Task 11: Verify sync workflow works

- [ ] **Step 1: Trigger the sync workflow manually**

```bash
gh workflow run sync-labels.yml
```

- [ ] **Step 2: Check the run completes successfully**

```bash
gh run list --workflow=sync-labels.yml --limit 1
```

Expected: status `completed`, conclusion `success`

- [ ] **Step 3: Verify labels on GitHub match the registry**

```bash
gh label list --limit 50 --json name -q '.[].name' | sort
```

Expected: all 19 labels from `.github/labels.yml` are present.
