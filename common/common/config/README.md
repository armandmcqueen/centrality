# `CentralityConfig`

A wrapper around `Pydantic` to provide generic config features like loading to/from yaml, 
overriding via environment variables and CLI option.

## Features
- Convert to and from YAML or JSON
- Validation against schema (thanks to Pydantic)
- Default values for missing fields (thanks to Pydantic)
- Overridable via environment variables
- Overridable via function arguments
- Full config can be saved and loaded via an environment variable
- TODO: Generate a full example YAML file, including all default values and comments

## Overriding Values

Order of precedence is:
1. Default values
2. CentralityConfig init kwargs (which will typically come from the YAML/JSON)
3. Environment variable overrides
4. argument overrides (`config_overrides`)

This is designed around a CLI experience.

Users have a YAML file that is as minimal as possible, hence the defaults. Environment variables can
be set to enforce behavior for all users (e.g. entire company). Then CLI arguments can be passed in
to specify very specific behavior such as for testing. I don't expect envvars and CLI arguments to be
used together much, but we have to define a precedence order, so this is the logic.




### Environment Variable Overrides
Environment variables overrides can be specified in the format `CENTRALITY_CLASSNAME_FIELDNAME_NESTEDFIELDNAE`.
Note that periods are not valid in envvar names. CentralityConfig envvars are case insensitive and the
underscores are ignored. Therefore there are many valid ways to name an envvar. If you get the correct 
letters in the correct order, it will work.

Here is an example nested CentralityConfig class:
```python
from pydantic import Field

class Subconfig(CentralityConfig):
    field_name: str

class ExampleConfig(CentralityConfig):
    subconfig: Subconfig = Field(default_factory=Subconfig)

example_config = ExampleConfig()
```
The flattened notation or dot notation is `example_config.subconfig.field_name`. The following are
all valid envvar overrides:
- `CENTRALITY_EXAMPLECONFIG_SUBCONFIG_FIELDNAME`
- `CENTRALITY_EXAMPLECONFIG_SUBCONFIG_FIELD_NAME`
- `centrality_exampleconfig_subconfig_fieldname`
- `CENTRALITY_exampleconfig_SUBCONFIG_fieldNAME`

and even `centralityexampleconfigsubconfigfieldname` (although this is not recommended)


### Argument Overrides
argument overrides (`config_overrides`) can be provided in two forms:
nested

```json
{
  "datastore": {
    "host": "anotherhost"
  }
}
```

or flattened

```json
{"datastore.host": "anotherhost"}
```

# Development Notes

## Naming limitation
Not all field name combinations are valid. This is to make envvars work better. If you run into this,
(CentralityConfigNameConflictError) rename a field to avoid the conflict. Details below.

envvars cannot contain dots. This makes it hard to set fields in nested configs via envvars. We could
require some weird solution like using flattened dot notation and replacing dots with two underscores,
but that is hard to remember and error prone. Instead, we will be extremely lenient with envvars. We
know the field tree, so given an input that is case-insensitive and may or may not have underscores, we
can intelligently predict which leaf node matches. This can be done 100% perfectly as long as there are
some naming restrictions. In this case, we give each leaf field a "slug" and enforce that it is unique.
This puts a small burden on the developer, but it is a one-time burden and it makes the user experience
much better.

A slug is the dot notation path with all dots removed, all of the underscores removed, and all lowercase.
For example, the slug for `subconfig.field_Name` is `subconfigfieldname`. 
