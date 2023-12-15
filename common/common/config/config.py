import os

import pydantic
from pydantic import BaseModel
from common.config.dict_utils import flatten_dict, merge_flattened_into_nested
from pathlib import Path
import yaml
import json


class CentralityConfigEnvvarUnsetError(Exception):
    pass

class CentralityConfigInvalidEnvvarError(Exception):
    pass


def to_slug(s: str) -> str:
    """
    Convert a dot notation string to a slug notation string.
    """
    return s.lower().replace(".", "").replace("_", "")


class CentralityConfigNameConflictError(Exception):
    def __init__(self, config_type: type["CentralityConfig"], conflict_1: str, conflict_2: str):
        self.config_type = config_type.__name__
        self.conflict_1 = conflict_1
        self.conflict_2 = conflict_2

    def __str__(self) -> str:
        slug = to_slug(self.conflict_1)
        return (f"Invalid CentralityConfig: {self.config_type}\n"
                f"There is a naming conflict in the config field names. See CentralityConfig docstring for why this exists.\n"
                f"Details: {self.conflict_1} and {self.conflict_2} both have the same slug: {slug}")



class CentralityConfig(BaseModel):
    """
    Overridable config for use in Centrality.

    # Features
    - Convert to and from YAML or JSON
    - Validation against schema (thanks to Pydantic)
    - Default values for missing fields (thanks to Pydantic)
    - Overridable via environment variables
    - Overridable via function arguments
    - Full config can be saved and loaded via an environment variable
    - TODO: Generate a full example YAML file, including all default values and comments

    # OVERRIDING VALUES

    Order of precedence is:
    1. Default values
    2. kwargs (which will typically come from the YAML/JSON)
    3. Environment variable overrides
    4. argument overrides (`config_overrides`)

    This is designed around a CLI experience.

    Users have a YAML file that is as minimal as possible, hence the defaults. Environment variables can
    be set to enforce behavior for all users (e.g. entire company). Then CLI arguments can be passed in
    to specify very specific behavior such as for testing. I don't expect envvars and CLI arguments to be
    used together much, but we have to define a precedence order, so this is the logic.


    # Naming limitation
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
    For example, the slug for


    # ENVVAR OVERRIDES:
    Environment variables overrides can be specified in the format `CENTRALITY_CLASSNAME_FIELDNAME_NESTEDFIELDNAE`.
    Note that periods are not valid in envvar names. CentralityConfig envvars are case insensitive and the
    underscores are ignored. Therefore there are many valid ways to name an envvar. The easiest way to
    remember is that if you get the correct letters in the correct order, it will work.

    Here is an example nested CentralityConfig class:
    ```python
    class Subconfig(CentralityConfig):
        field_name: str

    class ExampleConfig(CentralityConfig):
        subconfig: Subconfig = Subconfig()

    example_config = ExampleConfig()
    ```
    The flattened notation or dot notation is `example_config.subconfig.field_name`. The following are
    all valid envvar overrides:
    - CENTRALITY_EXAMPLECONFIG_SUBCONFIG_FIELDNAME
    - CENTRALITY_EXAMPLECONFIG_SUBCONFIG_FIELD_NAME
    - centrality_exampleconfig_subconfig_fieldname
    - CENTRALITY_exampleconfig_SUBCONFIG_fieldNAME
    and even
    - centralityexampleconfigsubconfigfieldname


    # ARGUMENT OVERRIDES
    argument overrides (`config_overrides`) can be provided two ways:
    nested
    ```
        {
            "datastore": {
                "host": "anotherhost"
            }
        }
    ```
    or flattened
    ```
        {
            "datastore.host": "anotherhost"
        }
    ```
    """
    def __init__(self, config_overrides: dict | None = None, **kwargs):

        # Override via envvars
        flattened_envvars = self.find_envvars()
        if flattened_envvars:
            kwargs = merge_flattened_into_nested(flattened_envvars, kwargs)

        # Override via function arguments
        if config_overrides:
            flattened_overrides = flatten_dict(config_overrides)
            kwargs = merge_flattened_into_nested(flattened_overrides, kwargs)

        super().__init__(**kwargs)
        self._validate_implementation()

    @classmethod
    def _build_field_tree(cls) -> list[str]:
        """
        Build a tree of all field names in dot notation. This is used to check for naming conflicts.
        """
        tree = []

        # Had issues before, leaving this in case:
        for field_name in list(cls.model_json_schema(False).get("properties")):
            field_info = cls.model_fields[field_name]
        # for field_name, field_info in cls.model_fields.items():
            if issubclass(field_info.annotation, CentralityConfig):
                sub_tree = field_info.annotation._build_field_tree()
                for sub_field_name in sub_tree:
                    tree.append(f"{field_name}.{sub_field_name}")
            else:
                tree.append(field_name)
        return tree

    @classmethod
    def _validate_implementation(cls) -> None:
        """
        Validate that a config override is valid. This is a helper function for `from_envvar`.
        """
        field_tree = cls._build_field_tree()
        undeduped_slugs = [(to_slug(dot), dot) for dot in field_tree]
        existing_slugs = {}  # slug: dot
        for new_slug, new_dot in undeduped_slugs:
            if new_slug in existing_slugs:
                existing_dot = existing_slugs[new_slug]
                raise CentralityConfigNameConflictError(cls, existing_dot, new_dot)
            existing_slugs[new_slug] = new_dot


    @classmethod
    def find_envvars(cls) -> dict | None:
        """
        Find all environment variables that match the config schema and return ovverrides in
        flattened dict format.
        """
        fields = {to_slug(dot): dot for dot in cls._build_field_tree()}
        prefix_slug = to_slug(f"CENTRALITY_{cls.__name__}_")

        # find matching envvars
        envvars = {}
        for k, v in os.environ.items():
            envvar_name_slug = to_slug(k)
            if envvar_name_slug.startswith(prefix_slug):
                field_slug = envvar_name_slug[len(prefix_slug):]
                if field_slug not in fields:
                    raise CentralityConfigInvalidEnvvarError(f"Environment variable {k} does not match any config fields")
                field_dot = fields[field_slug]
                envvars[field_dot] = v
        return envvars if len(envvars) > 0 else None

    @classmethod
    def from_yaml_file(cls, yaml_path: Path | str) -> 'CentralityConfig':
        """
        Load a YAML file and return a config object.
        """
        # TODO: Allow loading from a URL
        if isinstance(yaml_path, str):
            yaml_path = Path(yaml_path)
        with open(yaml_path, 'r') as f:
            yaml_dict = yaml.safe_load(f)
        return cls.from_dict(yaml_dict)

    def write_yaml(self, yaml_path: Path) -> None:
        """
        Save the config to a YAML file.
        """
        with open(yaml_path, 'w') as f:
            yaml.dump(self.as_dict(), f)

    @classmethod
    def from_json_file(cls, json_path: Path | str) -> 'CentralityConfig':
        """
        Load a JSON file and return a config object.
        """
        # TODO: Allow loading from a URL
        if isinstance(json_path, str):
            json_path = Path(json_path)
        with open(json_path, 'r') as f:
            json_dict = json.load(f)
        return cls.from_dict(json_dict)

    def write_json(self, json_path: Path) -> None:
        """
        Save the config to a JSON file.
        """
        with open(json_path, 'w') as f:
            json.dump(self.as_dict(), f)

    @classmethod
    def from_dict(cls, d: dict) -> 'CentralityConfig':
        """
        Load a dict and return a config object. Just for code clarity.
        """
        return cls(**d)

    def as_dict(self) -> dict:
        """
        Return the config as a dict. Just for code clarity.
        """
        return self.model_dump()

    @classmethod
    def envvar_name(cls):
        """
        Return the environment variable name for this config.
        """
        return f"CENTRALITY_{cls.__class__.__name__}".upper()

    @classmethod
    def from_envvar(cls) -> 'CentralityConfig':
        """
        Load the config from an environment variable.
        """
        envvar_name = cls.envvar_name()
        envvar_value = os.environ.get(envvar_name, None)
        if envvar_value is None:
            raise CentralityConfigEnvvarUnsetError(f"Environment variable {envvar_name} not set")
        json_dict = json.loads(envvar_value)
        return cls.from_dict(json_dict)

    def save_as_envvar(self) -> None:
        """
        Save the config as an environment variable. This is useful for passing the config to subprocesses.
        """
        os.environ[self.envvar_name()] = self.model_dump_json()

    def pretty_print_yaml(self) -> None:
        """
        Print the config as a YAML string.
        """
        print(yaml.dump(self.as_dict()))

    def pretty_print_json(self) -> None:
        """
        Print the config as a JSON string.
        """
        print(json.dumps(self.as_dict(), indent=4))




# Example Config, before addition of CentralityConfig


# class DatastoreConfig(BaseModel):
#     host: str = "localhost"
#     port: int = 5432
#     username: str = "postgres"
#     password: str = "postgres"
#
# class ControlPlaneRestConfig(BaseModel):
#     port: int
#     startup_healthcheck_timeout: int
#     startup_healthcheck_poll_interval: float = 0.5
#
#
#
# class ControlPlaneConfig(BaseModel):
#     datastore: DatastoreConfig = DatastoreConfig()
#     rest: ControlPlaneRestConfig = ControlPlaneRestConfig()



class DatastoreConfig(CentralityConfig):
    host: str = "localhost"
    port: int = 5432
    username: str = "postgres"
    password: str = "postgres"

class ControlPlaneRestConfig(CentralityConfig):
    port: int
    startup_healthcheck_timeout: int
    startup_healthcheck_poll_interval: float = 0.5


class ControlPlaneConfig(CentralityConfig):
    datastore: DatastoreConfig
    rest: ControlPlaneRestConfig

def test_defaults():
    ds_config = DatastoreConfig()
    assert ds_config.host == "localhost"
    assert ds_config.port == 5432
    assert ds_config.username == "postgres"
    assert ds_config.password == "postgres"


def test_required_fields():
    try:
        ControlPlaneRestConfig()
        assert False
    except pydantic.ValidationError:
        assert True

def assert_expected(control_plane_config: ControlPlaneConfig):
    assert control_plane_config.datastore.host == "notlocalhost"
    assert control_plane_config.datastore.port == 5432
    assert control_plane_config.datastore.username == "postgres"
    assert control_plane_config.datastore.password == "postgres"

    assert control_plane_config.rest.port == 8000
    assert control_plane_config.rest.startup_healthcheck_timeout == 60
    assert control_plane_config.rest.startup_healthcheck_poll_interval == 0.5

def test_nested_config_and_arg_ovverrids():
    control_plane_config = ControlPlaneConfig(config_overrides={
        "datastore.host": "notlocalhost",
        "rest.port": 8000,
        "rest.startup_healthcheck_timeout": 60,
    })
    assert_expected(control_plane_config)

def test_nested_config_and_envvar_ovverrids():
    os.environ["CENTRALITY_CONTROLPLANECONFIG_DATASTORE_HOST"] = "notlocalhost"
    os.environ["CENTRALITY_CONTROLPLANECONFIG_REST_PORT"] = "8000"
    os.environ["CENTRALITY_CONTROLPLANECONFIG_REST_STARTUP_HEALTHCHECK_TIMEOUT"] = "60"
    control_plane_config = ControlPlaneConfig()
    assert_expected(control_plane_config)



def main():
    # ds = DatastoreConfig()
    test_defaults()
    test_required_fields()
    test_nested_config_and_arg_ovverrids()
    test_nested_config_and_envvar_ovverrids()


# TODO: Write proper tests,
#  including invalid naming scheme implementation
#  varied envvar names
#  non-matching envvar name (prefix matched, but no field found)


if __name__ == '__main__':
    print("Running main")
    main()
    print("Done running main")
