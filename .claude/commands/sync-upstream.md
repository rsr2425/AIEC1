Safely configure and use the Git upstream remote for this fork-style course repository, then pull the latest course materials.

Follow these steps:

## 1. Inspect Before Changing Anything

Run these commands from the repository root:

```bash
git rev-parse --show-toplevel
git status --short --branch
git remote -v
git branch --show-current
```

Confirm:
- The command is running in the intended repository.
- The active branch is `main`.
- Local edits, staged files, and untracked files are visible before pulling.
- `origin` points to the user's repository.
- `upstream`, if present, points to the source repository.

Do not discard, reset, stash, commit, or overwrite local changes unless the user explicitly asks. Do not push to `upstream`.

## 2. Set Up Upstream (if missing)

When `upstream` is missing, add it:

```bash
git remote add upstream git@github.com:AI-Maker-Space/The-AI-Engineering-Certification-v1.0.git
git remote -v
```

When `upstream` already exists with the correct URL, report that setup is complete.

## 3. Pull Changes From Upstream

Before pulling, check `git status --short --branch`.

- If the worktree has local changes, stop and explain that the pull could create conflicts. Ask whether the user wants to commit or stash first.
- If the worktree is clean, pull:

```bash
git pull upstream main --allow-unrelated-histories
```

After a successful pull, run `git status --short --branch` and report what was integrated.

Do not push automatically unless the user asks.

## 4. Push Local Work To Origin (only if asked)

```bash
git push origin main
```

Direction is always: pull from `upstream`, edit locally, push to `origin`.

## Handle Common Problems

- If the directory is not a Git repository, stop and ask for the path.
- If `upstream` is missing, add it using the URL above.
- If authentication fails, recommend checking SSH keys or GitHub access.
- If merge conflicts occur, show conflicted files with `git status --short` and do not reset or push.
- If the branch is not `main`, confirm the intended branch before pulling.
