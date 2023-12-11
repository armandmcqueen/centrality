# Centrality


## Development

Each of `common`, `controlplane`, and `vmagent` are developed as independent Python packages, with 
each of the others having a dependency on `common`. They are versioned together, so the monorepo 
essentially has a single version number.

This is developed for Python 3.11 and we embrace the newest features. I'm sure that won't be 
painful in the future as software that needs to run in users' environments! :).

The as-of-yet-uncreated `cli` package should be focused on portability - being able to run on 
older version of Python and with minimal dependencies. 

### Requirements

OpenAPI generator

```bash
brew install openapi-generator
```