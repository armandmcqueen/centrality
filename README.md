# Centrality

Centrality is a toolkit for managing GPU clusters and training workflows. 

It is complementary to orchestrators like k8s and slurm, and is designed to allow users to easily add high-level, 
cross-layer behavior such as:
- if TrainingJob exits and 'Training Complete' not in logs, restart job from checkpoint
- if TrainingJob fails 5 times, drain/taint the nodes, run a GPU and networking benchmark and send the results to Slack

## High-level design

It achieves this by providing a control plane that centralizes all data related to the cluster/jobs, providing a number 
of agents that automatically collect the relevant data\*, offering a high-level abstraction for accessing that data, and 
providing an event bus/hooks so that custom behavior can be trivially triggered given certain conditions. The agents are 
also extensible, so you can add custom behavior to the system without needing to replicate the overall infrastructure.
For example, it will be very easy to add a custom healthcheck to the existing healthchecks that are run by the Machine Agent.

Additionally, Centrality defines a flexible, but structured view of how the basic building blocks of a training platform 
should work, allowing for the development of reusable, higher-level components. For example, a tool that messages you when 
a flagship training job fails shouldn't need to think about the details of whether a job is a Slurm sbatch or a Volcano Job,
it should just be able to think in terms of TrainingJobs. However, Centrality is all about making your existing setup better,
so the abstractions are broad and simple enough that the vast majority of set ups should have no problem fitting into them. 

\*For more bespoke setups where the out-of-the-box agents won't work, there is an SDK that can be used to send the relevant 
data to the control plane REST endpoints.

## Development Status

Early

Currently the control plane exists and there is a VMAgent (technically a bad name because it works just as well on bare metal)
that sends data to the control plane. Check out https://centrality-dev.fly.dev/Cluster for a rough UI that displays some of the
data being collected.




---
# Developing Centrality

## Testing

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

Note that the `-f` flags go before `up`

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


## Monorepo

Each of `common`, `controlplane`, `vmagent`, `cli`, `rapidui` and `deploy` are developed as independent Python 
packages, with many of them having a dependency on `common`. They are versioned together, so the monorepo 
essentially has a single version number.


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
