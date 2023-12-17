# Centrality


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

## Build Order

1. Generate OpenAPI spec for `controlplane` and save them to `common/sdks`. `cd controlplane && make gen-openapi-spec`
2. Generate Python client for each spec

# Conclib

We use the pykka actor model with `conclib` extensions for lots of the Python code. This is partially for the
good startup and cleanup behavior given an actor tree. If we need to use threads or processes that aren't actors
they must be cleaned up by a parent actor so that `pykka.ActorRegistry.stop_all()` completely cleans up all 
execution.
