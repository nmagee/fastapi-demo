# Lab: Docker Compose, FastAPI & MongoDB
**Estimated time:** ~60 minutes | **Repo:** https://github.com/nmagee/fastapi-demo

---

## Overview

In this lab you will spin up a multi-container application stack using Docker Compose, explore the running system with built-in Docker tooling, interact with a live REST API from the command line, and inspect the MongoDB database directly with MongoDB Compass.

**By the end of this lab you will be able to:**
- Understand Docker Compose as a multi-service orchestrator
- Start, stop, rebuild, and monitor containers from the CLI
- Read real-time logs and resource stats for running containers
- Issue HTTP GET and POST requests from the command line with `curl`
- Use the FastAPI interactive docs (Swagger UI) in the browser
- Connect MongoDB Compass to a locally running MongoDB container
- Browse collections and individual documents in a NoSQL database
- Read and understand a GitHub Actions workflow file section by section
- Enable and run an automated test workflow using GitHub Actions
- Configure a GHCR image build-and-push workflow triggered by pushes to `main`

---

## Prerequisites

Make sure you have the following installed before you start:

- **Docker Desktop** (Mac/Windows) or Docker Engine + Compose plugin (Linux)
- **Git**
- **MongoDB Compass** — download the free GUI from https://www.mongodb.com/try/download/compass
- A terminal and a web browser

> **Windows users:** Run all commands in PowerShell or Windows Terminal. In `curl` commands, replace single quotes with double quotes and escape inner double quotes with a backslash.

---

## Part 1 — Setup

### 1.1 Fork and clone the repository

Fork the repo to your own GitHub account first, then clone your fork:

```bash
git clone https://github.com/<your-github-username>/fastapi-demo.git
cd fastapi-demo
```

### 1.2 Read the code before you run it

Open the project in VS Code (or any editor) and read through the key files before touching Docker:

```bash
code .
# or just: cat Dockerfile && cat docker-compose.yml
```

As you read, answer these questions for yourself (you may be called on in discussion):

- What base image does the `Dockerfile` use?
- How many services are defined in `docker-compose.yml`? What are their names?
- Which port does FastAPI listen on inside the container, and which host port is it mapped to?
- What environment variable tells FastAPI where to find MongoDB?
- What do `insert-one.py` and `insert-many.py` do?

---

## Part 2 — Bringing the Stack Up

### 2.1 Build and start in detached mode

The `--build` flag forces Docker to (re)build the FastAPI image from the Dockerfile. The `-d` flag runs everything in the background so your terminal stays free.

```bash
docker compose build
docker compose up -d
```

You should see output similar to:

```
✔ Network fastapi-demo_default      Created
✔ Container fastapi-demo-mongo-1    Started
✔ Container fastapi-demo-app-1      Started
```

### 2.2 Verify the stack is running

```bash
docker compose ps
```

The `STATUS` column should show `running` (or `Up`) for both containers. Note the `PORTS` column — it shows exactly which host port maps to which container port.

> **Tip:** `docker compose ps` only shows services defined in the current compose file. To see every container on the system, use `docker ps`.

---

## Part 3 — Watching Your Containers

### 3.1 Streaming logs

Open a second terminal tab and stream logs from the entire stack:

```bash
docker compose logs -f
```

Keep this tab visible. You will see requests arrive here in real time as you work through Part 4.

To filter to a single service:

```bash
docker compose logs -f app
docker compose logs -f mongo
```

**Think about:** What log message appears when FastAPI starts successfully? What does it tell you about the ASGI server being used?

### 3.2 Resource stats

Docker has a built-in `top`-like display for live CPU and memory usage. Open a third terminal tab and run:

```bash
docker stats
```

Watch the numbers for a moment, then hit `Ctrl-C` to exit. Notice:
- Which container uses more memory at idle — the app or the database?
- What is the `MEM USAGE / LIMIT` ratio for each?

For a one-shot snapshot (no live scrolling):

```bash
docker stats --no-stream
```

📸 **Screenshot #1:** Take a screenshot of `docker stats --no-stream` showing both containers with CPU % and memory usage visible. You will submit this on Canvas.

### 3.3 Inspecting a container

`docker inspect` returns a JSON blob of low-level metadata — networking, mounts, environment variables, and more:

```bash
# Substitute the actual container name shown by 'docker compose ps'
docker inspect fastapi-demo-app-1
```

Pull out just the environment variables:

```bash
docker inspect fastapi-demo-app-1 | grep -A1 '"Env"'
```

---

## Part 4 — Interacting with the REST API

### 4.1 Browse the interactive docs

FastAPI auto-generates Swagger UI documentation. Open your browser and go to:

```
http://localhost:8000/docs
```

You should see all available endpoints listed as an interactive, clickable interface. We will also drive the API from the terminal.

### 4.2 GET requests

Root health-check:

```bash
curl http://localhost:8000/
```

List all items (the collection will be empty at first):

```bash
curl http://localhost:8000/items
```

Pretty-print the JSON by piping through Python:

```bash
curl -s http://localhost:8000/items | python3 -m json.tool
```

### 4.3 POST — creating new documents

Use `-X POST` to send data. The `-H` flag sets the `Content-Type` header and `-d` provides the JSON body.

Insert a single record:

```bash
curl -X POST http://localhost:8000/items \
     -H "Content-Type: application/json" \
     -d '{"name": "Alice Nguyen", "email": "anguyen@example.com"}'
```

Add a few more so your database has some variety:

```bash
curl -X POST http://localhost:8000/items \
     -H "Content-Type: application/json" \
     -d '{"name": "Bob Okafor", "email": "bokafor@example.com"}'

curl -X POST http://localhost:8000/items \
     -H "Content-Type: application/json" \
     -d '{"name": "Carmen Reyes", "email": "creyes@example.com"}'
```

Confirm all three are returned:

```bash
curl -s http://localhost:8000/items | python3 -m json.tool
```

📸 **Screenshot #2:** Take a screenshot of your terminal showing the `GET /items` response with at least three JSON documents. Pretty-printed output preferred. Submit on Canvas.

### 4.4 Use the Python helper scripts

The repo includes scripts to bulk-seed data. Run them inside the app container so you don't need a local Python environment:

```bash
docker compose exec app python insert-many.py
```

After running it, GET `/items` again and note how many documents are now in the collection.

### 4.5 Try the Swagger UI

Return to `http://localhost:8000/docs`. Click any endpoint, then **Try it out** → **Execute**. Compare the response to what you got with `curl`. Notice that Swagger also shows you the exact `curl` command it used — handy for learning the syntax.

---

## Part 5 — MongoDB Compass

### 5.1 Install MongoDB Compass

If you have not done so already, download and install from:

https://www.mongodb.com/try/download/compass

Choose the **Stable** release for your OS. No account is required.

### 5.2 Connect to the running container

MongoDB is exposed on the standard port `27017`. Use this connection string in Compass:

```
mongodb://localhost:27017
```

Steps:
1. Launch MongoDB Compass.
2. Click **New Connection** (or use the connection string bar at the top).
3. Paste `mongodb://localhost:27017` into the URI field.
4. Click **Connect**.
5. In the left sidebar you will see a list of databases. Look for the one your FastAPI app uses — check `app/main.py` or the compose environment variables to confirm the name.
6. Click the database, then click the collection to view documents.

### 5.3 Explore the data

Once inside the collection, try the following:

- Switch between **List View**, **JSON View**, and **Table View** using the icons in the top-right of the document panel.
- Click any document to expand it and inspect the full BSON structure, including the `_id` ObjectId field that MongoDB assigns automatically.
- Use the **Filter** bar to query. For example, filter by name:
  ```
  { "name": "Alice Nguyen" }
  ```
- Click **Add Data → Insert Document** to add a record directly from Compass, then verify it appears when you run `GET /items` from the terminal.

📸 **Screenshot #3:** Take a screenshot of Compass showing your collection with several documents visible and at least one fully expanded. Submit on Canvas.

---

## Part 6 — Compose Lifecycle Operations

### 6.1 Stopping and restarting

Stop all containers without removing them (data is preserved):

```bash
docker compose stop
```

Start them again:

```bash
docker compose start
```

Wait a few seconds and confirm the API still responds and your data is still there:

```bash
curl -s http://localhost:8000/items | python3 -m json.tool
```

MongoDB stores data in a named volume that survives stops and restarts.

### 6.2 Restarting a single service

Restart only the app container (e.g., after a code change):

```bash
docker compose restart app
```

### 6.3 Shell access inside a container

You can open an interactive shell inside any running container:

```bash
# Shell into the FastAPI app container
docker compose exec app /bin/bash

# Once inside, explore:
ls /app
python3 --version
exit
```

```bash
# Shell into MongoDB and run mongosh
docker compose exec mongo mongosh

# Once in mongosh:
show dbs
use <your-db-name>
show collections
db.<collection>.find().pretty()
exit
```

### 6.4 Tearing everything down

When you are completely finished:

```bash
docker compose down          # stops and removes containers + network
docker compose down -v       # also removes volumes (wipes MongoDB data permanently)
```

> ⚠️ **Warning:** `docker compose down -v` is destructive — it permanently deletes all data stored in volumes. Only run this when you are sure you are done.

---

## Deliverables

Submit the following four screenshots to Canvas:

| # | Screenshot | Must show |
|---|------------|-----------|
| 1 | `docker stats --no-stream` | Both containers listed; CPU % and memory usage visible |
| 2 | `GET /items` response | Terminal with curl command visible; at least 3 JSON documents; pretty-printed preferred |
| 3 | MongoDB Compass | Connected to `localhost:27017`; collection open with documents visible; at least one document fully expanded |
| 4 | GitHub Actions | Green checkmark on the test workflow run **and** a successful build workflow run showing your Docker Hub image name |

---

## Quick Reference

| Command | What it does |
|---------|--------------|
| `docker compose up -d` | Start the full stack in detached mode |
| `docker compose up -d --build` | Rebuild images before starting |
| `docker compose down` | Stop and remove containers |
| `docker compose down -v` | Also wipe volumes (destroys data) |
| `docker compose ps` | List running services and ports |
| `docker compose logs -f` | Stream logs from all services |
| `docker compose logs -f <svc>` | Stream logs from one service |
| `docker stats` | Live CPU/memory for all containers |
| `docker stats --no-stream` | One-time snapshot of stats |
| `docker inspect <container>` | Full JSON metadata for a container |
| `docker compose exec <svc> bash` | Open a shell in a running container |
| `docker compose restart <svc>` | Restart a single service |

---

## Part 7 — GitHub Actions: Automated Testing and Image Builds

So far everything has run on your laptop. In this part you will set up two GitHub Actions workflows that run automatically in the cloud whenever you push code — one that tests your application, and one that builds and publishes a Docker image to the GitHub Container Registry (GHCR).

### Background: What is GitHub Actions?

GitHub Actions is a CI/CD (Continuous Integration / Continuous Delivery) platform built directly into GitHub. A **workflow** is a YAML file stored in `.github/workflows/` that describes:

- **When** to run (the trigger — a push, a pull request, a schedule, etc.)
- **Where** to run (what kind of virtual machine to use)
- **What** to run (a sequence of steps — shell commands, or pre-built community actions)

GitHub provides free runner minutes for public repositories. Every time you push to the repo, GitHub spins up a fresh VM, runs your workflow, and reports success or failure right on the commit and the Actions tab.

The repo ships two workflow files with a `.yml.disabled` suffix so they don't run accidentally. Enabling them is as simple as renaming the files.

---

### 7.1 Enable the test workflow

#### Rename the file to activate it

```bash
cd .github/workflows
mv test.yml.disabled test.yml
```

> **Why `.yml.disabled`?** GitHub Actions only recognizes files ending in `.yml` or `.yaml` inside `.github/workflows/`. Any other extension is silently ignored. This is a common pattern for shipping an example workflow that students or users opt into rather than having it fire on the first clone.

#### Read the file

Open `test.yml` and read through it. It will look something like this — we'll walk through each section:

```yaml
# ── 1. Workflow name ─────────────────────────────────────────────
name: Run Tests

# ── 2. Trigger ───────────────────────────────────────────────────
on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

# ── 3. Jobs ──────────────────────────────────────────────────────
jobs:
  test:
    # ── 4. Runner ──────────────────────────────────────────────
    runs-on: ubuntu-latest

    steps:
      # ── 5. Checkout ──────────────────────────────────────────
      - name: Check out repository
        uses: actions/checkout@v4

      # ── 6. Python setup ──────────────────────────────────────
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      # ── 7. Install dependencies ──────────────────────────────
      - name: Install dependencies
        run: pip install -r requirements.txt

      # ── 8. Run tests ─────────────────────────────────────────
      - name: Run pytest
        run: pytest
```

#### Section-by-section explanation

**`name`** — A human-readable label shown in the GitHub Actions UI. Can be anything; keep it descriptive.

**`on`** — The event trigger. This workflow fires on two events:
- Any `push` to the `main` branch
- Any `pull_request` targeting `main`

You can trigger on dozens of events: `schedule` (cron), `workflow_dispatch` (manual button), `release`, `issue_comment`, and more. The `branches` filter means this won't fire on pushes to feature branches unless you add them.

**`jobs`** — A workflow contains one or more jobs. Jobs run in parallel by default (you add `needs:` to serialize them). Each job gets its own fresh VM.

**`runs-on`** — The type of runner (virtual machine) GitHub will provision. `ubuntu-latest` is the most common choice; `windows-latest` and `macos-latest` are also available.

**`steps`** — An ordered list of tasks within the job. Each step has a `name` (shown in the UI log) and either:
- `uses:` — a pre-built community action (e.g., `actions/checkout@v4` clones your repo onto the runner)
- `run:` — a raw shell command

**`actions/checkout@v4`** — This is the official GitHub action that clones your repository into the runner's working directory. Without this step, the runner has no access to your code. The `@v4` pins to a specific major version of the action.

**`actions/setup-python@v5`** — Installs and activates a specific Python version on the runner. The `with:` block passes parameters to the action — here it sets `python-version: "3.11"`.

**`pip install -r requirements.txt`** — A plain shell command. Any `run:` step is just a bash command (or PowerShell on Windows runners). Multiple lines are written with a `|` (literal block scalar in YAML).

**`pytest`** — Runs the test suite. If any test fails, this step exits non-zero, the job is marked as failed, and GitHub blocks the commit from being merged (if branch protection rules are set).

#### Commit and push to trigger it

```bash
git add .github/workflows/test.yml
git commit -m "Enable test workflow"
git push origin main
```

Then go to your fork on GitHub, click the **Actions** tab, and watch the workflow run. Click into the run to see each step's log output in real time.

📸 **Screenshot #4a:** Take a screenshot of the Actions tab showing the test workflow with a green ✅ checkmark.

---

### 7.2 Enable the build workflow

This workflow builds your Docker image and pushes it to the **GitHub Container Registry (GHCR)** automatically on every push to `main`. GHCR is GitHub's own container registry — your image lives right alongside your repository, no separate account needed, and visibility follows your repo's access settings.

Before enabling the workflow you need to create a Personal Access Token (PAT) and store it as a repository secret.

#### Step 1 — Create a GitHub Personal Access Token (PAT)

A PAT is a scoped credential that lets a script or workflow authenticate to GitHub's APIs and services — including GHCR — on your behalf.

1. On GitHub, click your avatar in the top-right → **Settings**.
2. In the left sidebar scroll to the bottom and click **Developer settings**.
3. Click **Personal access tokens** → **Tokens (classic)** → **Generate new token (classic)**.
4. Give it a descriptive note, e.g. `ghcr-push`.
5. Set an expiration (90 days is reasonable for a class token).
6. Under **Select scopes**, check **`write:packages`** — this automatically also selects `read:packages` and `repo`. These scopes allow the token to push images to GHCR and read repository metadata.
7. Click **Generate token**.
8. **Copy the token immediately** — GitHub will never show it again. Paste it somewhere safe for the next step.

> **Why a PAT and not your password?** A PAT is scoped to only the permissions you select, expires on a schedule, and can be revoked at any time without changing your account password. It's the standard credential for automation against GitHub services.

#### Step 2 — Store the PAT as a repository secret

GitHub Secrets are encrypted environment variables attached to a specific repository. Workflow files reference them with `${{ secrets.SECRET_NAME }}` — the raw value is never exposed in job logs.

1. Navigate to your fork on GitHub.
2. Click **Settings** → **Secrets and variables** → **Actions** → **New repository secret**.
3. Add the following secret:

| Secret name | Value |
|-------------|-------|
| `CR_PAT` | The Personal Access Token you just generated |

That's it — one secret is all GHCR requires because your GitHub username is already available to workflows via the built-in `github.actor` context variable.

#### Step 3 — Rename and edit the build workflow file

```bash
cd .github/workflows
mv build.yml.disabled build.yml
```

Open `build.yml` and update it to match the following. Read the inline comments — the section-by-section explanation follows below:

```yaml
# ── 1. Workflow name ─────────────────────────────────────────────
name: Build and Push Docker Image

# ── 2. Trigger ───────────────────────────────────────────────────
on:
  push:
    branches:
      - main

# ── 3. Jobs ──────────────────────────────────────────────────────
jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      # ── 4. Checkout ──────────────────────────────────────────
      - name: Check out repository
        uses: actions/checkout@v4

      # ── 5. Log in to GHCR ────────────────────────────────────
      - name: Log in to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.CR_PAT }}

      # ── 6. Build and push ────────────────────────────────────
      - name: Build and push image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ghcr.io/${{ github.actor }}/fastapi-demo:latest
```

#### ⚠️ Important: do not change `${{ github.actor }}`

Unlike a Docker Hub workflow where you hard-code your username, here the owner is set dynamically using `${{ github.actor }}` — a built-in context variable that resolves to the GitHub username of whoever triggered the workflow run. This means:

- You never need to hard-code your username into the file
- The workflow works correctly for everyone who forks the repo
- The image is always pushed to `ghcr.io/<your-username>/fastapi-demo:latest`

The only field you might want to customize is the image name `fastapi-demo` — change it to anything you like, but keep the `ghcr.io/${{ github.actor }}/` prefix.

#### Section-by-section explanation of new concepts

**`on: push: branches: [main]`** — This workflow only fires on pushes to `main`, not pull requests or feature branches. The intent is to publish a new image only once code has been reviewed and merged — a standard production convention.

**`docker/login-action@v3`** — The official Docker action for authenticating to a container registry. Three parameters are needed for GHCR:
- `registry: ghcr.io` — tells the action to target GitHub's registry rather than Docker Hub (the default)
- `username: ${{ github.actor }}` — the GitHub username of the person who pushed; the `github` context is a built-in object available in every workflow, no secret needed
- `password: ${{ secrets.CR_PAT }}` — your PAT, read from the repository secret you created in Step 2

**`${{ secrets.CR_PAT }}`** — GitHub Actions expression syntax. `secrets` is a built-in context; `.CR_PAT` is the secret name you chose. The value is injected at runtime and automatically masked — it will never appear as plain text in any log, even if you accidentally `echo` it.

**`docker/build-push-action@v5`** — Wraps `docker buildx build` and `docker push` into a single step. Key parameters:
- `context: .` — use the current directory as the Docker build context (where your `Dockerfile` lives)
- `push: true` — actually push to the registry after a successful build; set `false` on PR workflows to build without publishing
- `tags:` — the fully-qualified image reference. GHCR images follow the format `ghcr.io/<owner>/<image-name>:<tag>`. The `latest` tag is a floating convention pointing to the most recent build.

#### Step 4 — Commit and push

```bash
git add .github/workflows/build.yml
git commit -m "Enable GHCR build workflow"
git push origin main
```

Go to the **Actions** tab on GitHub and watch both workflows queue and run. When the build job finishes, click your avatar → **Your profile** → **Packages** to see your newly published container image listed under your GitHub account.

You can also view the package directly at:

```
https://github.com/<your-github-username>?tab=packages
```

📸 **Screenshot #4b:** Take a screenshot showing the build workflow with a green ✅ checkmark **and** your image visible on your GitHub Packages page.

---

### 7.3 Verify the full CI/CD loop

Make a small, harmless change to trigger both workflows and confirm the loop is working end to end:

```bash
# Add a blank line to the README, or change a comment in app/main.py
echo "" >> README.md
git add README.md
git commit -m "Trigger CI check"
git push origin main
```

Watch the Actions tab — both the test and build workflows should start within seconds. This is the fundamental CI/CD loop: **push code → tests run → image builds and publishes**, all without any manual steps.

---

## Bonus Challenges (optional)

If you want to explore these concepts further, try one or more of these:

**Bonus A — Add a DELETE endpoint**
Open `app/main.py` and add a `DELETE /items/{id}` route that removes a document by its MongoDB `_id`. Rebuild with `docker compose up -d --build` and test with `curl -X DELETE http://localhost:8000/items/<id>`.

**Bonus B — Add a volume mount for live reload**
Edit `docker-compose.yml` to mount the `./app` directory into the container and add `--reload` to the uvicorn startup command. Changes to `app/main.py` will now take effect immediately without a rebuild.

**Bonus C — Tag images with the Git SHA**
Update the `tags:` line in `build.yml` to publish three tags on every build: the build number, `latest` and the exact commit SHA. In GHCR this looks like:

```yaml
tags: |
  ghcr.io/${{ github.actor }}/fastapi-demo:${{ env.IMAGE_TAG }}
  ghcr.io/${{ github.actor }}/fastapi-demo:latest
  ghcr.io/${{ github.actor }}/fastapi-demo:${{ github.sha }}
```

This gives you an immutable, traceable tag for every build alongside the floating `latest` convenience tag. You'll see both appear on your GitHub Packages page after the next push.

**Bonus D — Add a branch protection rule**
In your fork's GitHub settings, go to **Branches** → **Add branch protection rule** for `main`. Require the test workflow to pass before a pull request can be merged. Create a feature branch, open a PR, and observe how GitHub blocks the merge until the green check appears.
