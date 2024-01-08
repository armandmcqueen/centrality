# VM Metric Types

The code to handle metric streams has a ton of duplication. We use code generation to make this more manageable.

We generate three types of code:
- The types. This is the ORM and a pydantic model for each metric type. There is both a timeseries and a latest type.
- The datastore client. To add, query range, query latest, and delete, we generate the datastore client methods.
- The REST API endpoints. We generate the FastAPI route functions for each operation on each metric type.

## Details

Each metric type has a definition model in `controlplane/codegenvars`. This module has the information needed to hydrate
templates for each metric type.

The templates are in `.template` files. The template files are:
- `controlplane/datastore/client.template`: The datastore client methods. There methods are added to
  `controlplane/datastore/client.py`
- `controlplane/datastore/types/vmmetrics/types.template`: The ORM and pydantic models. Each metric generates 
   a complete file in `controlplane/datastore/types/vmmetrics/generated/`
- `controlplane/rest/rest.template`: The REST API endpoints. These are added to `controlplane/rest/api.py`

For the datastore client and REST API endpoints, we the code is generated an inserted into the existing files 
between `# BEGIN GENERATED CODE` and `# END GENERATED CODE` comments. Existing code between these comments is 
completely replaced.

The code generation logic is done in `controlplane/codegen.py`. The templating language is custom. It's mostly 
basic string replacement. Right now it is designed so the `.template` files can be valid python files. Currently,
the logic is super simple. but if it gets more complicated, this should be ported to a real templating language.
