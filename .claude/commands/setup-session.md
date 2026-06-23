Set up a new course session folder: create the virtual environment, install dependencies, and register a Jupyter kernel so the notebook is usable in VS Code.

The user will specify which folder (e.g. "07" or the full folder name). If not specified, detect new session folders that don't have a `.venv` yet.

## 1. Identify the target folder

List session folders in the repo root:

```bash
ls -d /Users/ryanrodriguez/src/AIEC1/[0-9]*/
```

Match the user's input to a folder. If no input, find folders missing a `.venv`:

```bash
for d in /Users/ryanrodriguez/src/AIEC1/[0-9]*/; do [ ! -d "$d/.venv" ] && echo "$d"; done
```

If no folder matches or multiple match without user guidance, ask for clarification.

## 2. Check for pyproject.toml

Verify the folder has a `pyproject.toml`. If not, stop and report — the session materials may not be released yet.

Check that `ipykernel` and `jupyterlab` are in the dependencies. If missing, add them:
- `"ipykernel>=6.29.0"`
- `"jupyterlab>=4.2.0"`

## 3. Run uv sync

From the target folder:

```bash
VIRTUAL_ENV= uv sync
```

The `VIRTUAL_ENV=` prefix prevents interference from any activated venv in the shell.

Wait for completion. The git-based `ragas` dependency can take a few minutes to resolve on first run.

## 4. Register the Jupyter kernel

Derive a kernel name and display name from the folder name. Follow the existing convention in `~/Library/Jupyter/kernels/`:
- Directory name: lowercase, underscored (e.g. `07_advanced_retrievers`)
- Display name: numbered with topic (e.g. `"07 Advanced Retrievers"`)

Look at an existing kernel for the format:

```bash
cat ~/Library/Jupyter/kernels/04_multi_agent_systems/kernel.json
```

Create the kernel spec directory and write `kernel.json`:

```bash
mkdir -p ~/Library/Jupyter/kernels/<kernel_name>/
```

Write `kernel.json` with this structure (adjust paths and names):

```json
{
 "argv": [
  "/Users/ryanrodriguez/src/AIEC1/<folder_name>/.venv/bin/python",
  "-Xfrozen_modules=off",
  "-m",
  "ipykernel_launcher",
  "-f",
  "{connection_file}"
 ],
 "display_name": "<NN> <Topic> (<Subtitle>)",
 "language": "python",
 "metadata": {
  "debugger": true
 },
 "kernel_protocol_version": "5.5"
}
```

## 5. Verify

Confirm the kernel appears:

```bash
ls ~/Library/Jupyter/kernels/
```

Then tell the user to run **Developer: Reload Window** in VS Code (Cmd+Shift+P) to pick up the new kernel.
