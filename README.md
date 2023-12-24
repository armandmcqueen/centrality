# Centrality

# Testing


There are a couple forms of testing. 

Docker compose (`dockercompose`) is the primary local development environment. This will spin up all the components locally with
a small number of agents. It is easy to add and remove agents to test dynamism (see instructions at top of compose.yaml).
This currently does a build of the Docker images, so it isn't super fast. This could be improved by mounting
the source code into the containers, so a rebuild isn't necessary.

Python testing (`quicktest`) is also possible for rapid iteration, but it is preferable to do unit testing. However, if a 
docker compose stack is running, it is possible to launch an agent/webui outside of docker for rapid
iteration. See the `quicktest` config for an example.

There is a missing testing piece that allows us to simulate very large-scale deployments with ~1000+ agents. This
will require external machines as my laptop isn't powerful enough to run that many agents. 

Fly (`fly`) is the fully deployed environment. This hasn't been set up yet. Possibly there should be a dev and prod
version of this environment. 


## Docker Compose

Local testing is primarily done with Docker Compose launching all the components.

```bash
docker compose build
docker compose up
```

```bash
#python cli/cli/cli.py watch-vm
python cli/cli/cli.py watch-cpu
````

## Quick tests

To quickly run a test outside of a container, you can use the `quicktest` config.

```bash
python vmagent/vmagent/cli.py launch -f tests/configs/quicktest/vmagent.yaml
```

## Fly

```bash
flyctl deploy
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
brew install openapi-generator
brew install flyctl
```



## Conclib

We use the pykka actor model with `conclib` extensions for lots of the Python code. This is partially for the
good startup and cleanup behavior given an actor tree. If we need to use threads or processes that aren't actors
they must be cleaned up by a parent actor so that `pykka.ActorRegistry.stop_all()` completely cleans up all 
execution.
