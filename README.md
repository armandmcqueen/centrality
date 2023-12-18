# Centrality

# Testing

### Docker Compose

Local testing is primarily done with Docker Compose launching all of the components.

```bash
docker compose build
docker compose up
```

```bash
#python cli/cli/cli.py watch-vm
python cli/cli/cli.py watch-cpu
````

### Quick tests

To quickly run a test outside of a container, you can use the `quicktest` config.

```bash
python vmagent/vmagent/cli.py launch -f tests/configs/quicktest/vmagent.yaml
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


# Conclib

We use the pykka actor model with `conclib` extensions for lots of the Python code. This is partially for the
good startup and cleanup behavior given an actor tree. If we need to use threads or processes that aren't actors
they must be cleaned up by a parent actor so that `pykka.ActorRegistry.stop_all()` completely cleans up all 
execution.
