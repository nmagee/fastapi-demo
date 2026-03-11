![Build Status](https://img.shields.io/github/actions/workflow/status/nmagee/fastapi-demo/build.yaml)
![Commits](https://img.shields.io/github/commit-activity/t/nmagee/fastapi-demo)
![GitHub Release](https://img.shields.io/github/v/release/nmagee/fastapi-demo)
[![Static Badge](https://img.shields.io/badge/Demo-HTTP-yellow)](https://uvasds.sh/spotify/)


# FastAPI Demo

## Getting Started

### Local

After forking this repository for your own work, you may need to set up an isolated environment in Python. I suggest using `pipenv` for this:

```
# Install pipenv itself
python3 -m pip install pipenv

# Then from within the root directory of this project,
# create a new virtual environment and install dependencies
pipenv shell

pipenv install -r requirements.txt

# Exit the virtual environment at any point with "exit"
# Return to it by running "pipenv shell" from the directory.
```

## Development 

As typical with FastAPI development, run the local server as you code

## Build & Launch the Compose Stack

Build locally using the `docke compose build` command. Then run the stack in detached mode:

```
docker compose up -d
```

## Set up a GitHub Action Build

Look in `.github/workflows/build.yml` for a sample template that completes the following steps:

1. Builds the container image.
2. Pushes the new image to the container registry of your choice (i.e. Docker Hub, GHCR, etc.)
3. (Optional) Pushes a message to a cluster triggering a re-deployment of the app.
