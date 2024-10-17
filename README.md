# FastAPI Demo

## Getting Started

### GitHub Codespaces

The easiest way to start working is to open your GitHub repository in GitHub Codespaces.

From within that environment, you have a full IDE to work with the code, run commands in the terminal, preview the application by running the `./preview.sh` script, and perform normal `git` add/commit/push commands.

### Local

After forking this repository for your own work, you may need to set up an isolated environment in Python. I suggest using `pipenv` for this:

```
# Install pipenv itself
python3 -m pip install pipenv

# Then from within the root directory of this project,
# create a new virtual environment
pipenv shell

# Exit the virtual environment at any point with "exit"
# Return to it by running "pipenv shell" from the directory.
```

## Development 

As typical with FastAPI development, run the local server as you code:
```
# cd into the app/ directory
cd app

# run the local uvicorn server (install locally first)
uvicorn main:app --reload
```

Your dev site is now running locally at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)


## Sample Endpoints and Methods

This template contains a variety of methods and endpoints:

### `http://127.0.0.1:8000/add/7/3`

Adds two integers taken as URL path parameters
```
{
  "sum": 10
}
```

### `http://127.0.0.1:8000/items/1234567890?q=foo&s=bar`

Takes an integer path parameter `1234567890` as well as two query string parameters `foo` and `bar`.

```
{
  "item_id": 1234567890,
  "q": "foo",
  "s": "bar"
}
```

For more on catching POST payloads in JSON, or form parameters, consult the FastAPI documentation.

## Build the Container

Build locally using the `docker build` command:
```
docker build -t some_org/some_image:some_tag .
```

## Run the Container Locally

Run the image locally and map the container port (80) to some host port (8080):
```
docker run -d -p 8080:80 --rm some_org/some_image:some_tag
```

## Set up a Build Pipeline

Look in `.build.yml` for a sample template that completes the following steps:

1. Builds the container image.
2. Pushes the new image to the container registry of your choice (i.e. Docker Hub, GHCR, etc.)
3. Pushes an SQS message to Amazon triggering a re-deployment of the app in DCOS.

To enable this pipeline, place it in `.github/workflows/` and git push. Some repository secrets must be set before builds will work.

> post template
