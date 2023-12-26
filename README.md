# Centrality

# Testing

There are a couple forms of testing. 

Docker compose (`dockercompose`) is the primary local development environment. This will spin up all the 
components locally with a small number of agents. It is easy to add and remove agents to test dynamism 
(see instructions at top of compose.yaml). This currently does a build of the Docker images, so it isn't 
super fast. This could be improved by mounting the source code into the containers, so a rebuild isn't 
necessary.

Python testing (`quicktest`) is also possible for rapid iteration, but it is preferable to do unit testing. However, 
if a docker compose stack is running, it is possible to launch an agent/webui outside of docker for rapid
iteration. See the `quicktest` config for an example.

There is a missing testing piece that allows us to simulate very large-scale deployments with ~1000+ agents. This
will require external machines as my laptop isn't powerful enough to run that many agents. Possibly we can use a 
single, very large machine with docker compose?

Fly (`fly`) is the fully deployed environment. There is a fly application for the control plane + rapidui and a 
separate fly application for the agent cluster. There is currently only a single Fly stack (i.e. no dev/prod).


## Docker Compose

Local testing is primarily done with Docker Compose launching all the components.

```bash
docker compose build
docker compose up
```

To use the current code without needing to build new containers, we use an override file that mounts the source code
into the containers. This is much faster than rebuilding the containers.

```bash
docker compose -f compose.yaml -f compose-override-mountcode.yaml up
```

Add the `-d` flag to run in the background, which makes the logs more manageable.

To see logs for all containers:
```bash
docker compose logs -f
```

## Quick tests

To quickly run a test outside of a container, you can use the `quicktest` config.

```bash
python vmagent/vmagent/cli.py launch -f tests/configs/quicktest/vmagent.yaml
```

## Fly

To deploy the Fly applications:

```bash
# Control plane
fly deploy

# Agent cluster
fly --config fly-agent-cluster.toml deploy
```

To scale the agent cluster.

```bash
fly --config fly-agent-cluster.toml scale count --process-group agent 5
```

To run a local VM Agent that talks to the Fly control plane:

```bash
python vmagent/vmagent/cli.py launch -f tests/configs/fly/vmagent-local.yaml
```

To access the DB locally on port 5433:
```bash
fly proxy 5433 -a centrality-datastore-dev
```


# Development

Each of `common`, `controlplane`, and `vmagent` are developed as independent Python packages, with 
each of the others having a dependency on `common`. They are versioned together, so the monorepo 
essentially has a single version number.

This is developed for Python 3.11 and we embrace the newest features. I'm sure that won't be 
painful in the future as software that needs to run in users' environments! :).

The `cli` package should be focused on portability - being able to run on older version of Python 
and with minimal dependencies. 

## Requirements


```bash
brew install redis
brew install openapi-generator
brew install flyctl
```


## Conclib

We use the pykka actor model with `conclib` extensions for lots of the Python code. This is partially for the
good startup and cleanup behavior given an actor tree. If we need to use threads or processes that aren't actors
they must be cleaned up by a parent actor so that `pykka.ActorRegistry.stop_all()` completely cleans up all 
execution.
