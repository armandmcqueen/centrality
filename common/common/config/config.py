import json
import os
from pathlib import Path
from typing import Any, TypeVar, Type

import pydantic
import yaml
from common.config.dict_utils import flatten_dict, merge_flattened_into_nested

Dict = dict[str, Any]


class CentralityConfigEnvvarUnsetError(Exception):
    """When CentralityConfig.from_envvar() is run, but the envvar is not set"""
    pass


class CentralityConfigInvalidEnvvarOverrideError(Exception):
    """
    When an envvar override is found for this config, but doesn't match any fields.
    To help users catch typos
    """
    pass


class CentralityConfigNameConflictError(Exception):
    """If a CentralityConfig has conflicting slugs. See README.md for more details."""

    def __init__(
        self, config_type: type["CentralityConfig"], conflict_1: str, conflict_2: str
    ):
        self.config_type = config_type.__name__
        self.conflict_1 = conflict_1
        self.conflict_2 = conflict_2

    def __str__(self) -> str:
        slug = to_slug(self.conflict_1)
        return (
            f"Invalid CentralityConfig: {self.config_type}\n"
            f"There is a naming conflict in the config field names. See CentralityConfig "
            f"docstring for why this exists.\n"
            f"Details: {self.conflict_1} and {self.conflict_2} both have the same slug: {slug}"
        )


def to_slug(s: str) -> str:
    """Convert a dot notation string to a slug notation string"""
    return s.lower().replace(".", "").replace("_", "")


T = TypeVar('T', bound='CentralityConfig')


class CentralityConfig(pydantic.BaseModel):
    """
    Overridable config for use in Centrality. See README.md for more details.
    """

    def __init__(self, config_overrides: Dict | None = None, **kwargs: Any):
        # Apply envvar overrides
        flattened_envvars = self._find_envvars()
        if flattened_envvars:
            kwargs = merge_flattened_into_nested(flattened_envvars, kwargs)

        # Apply argument overrides
        if config_overrides:
            flattened_overrides = flatten_dict(config_overrides)
            kwargs = merge_flattened_into_nested(flattened_overrides, kwargs)
        super().__init__(**kwargs)
        self._validate_implementation()  # Hook to validate name conflicts

    @classmethod
    def _build_field_tree(cls) -> list[str]:
        """
        Build a tree of all field names in dot notation. This is used to check for naming conflicts.
        """
        # Note: This was tricky to get working, but was probably just my fault. I was creating a
        # nested CentralityConfig with a default instance instead of a default_factory. e.g.
        # ```python
        # class Subconfig(CentralityConfig):
        #     field_name: str  # note that there is no default value
        #
        # class ExampleConfig(CentralityConfig):
        #     subconfig: Subconfig = Subconfig()  # This is wrong
        # ```
        # This caused this function to fail due to pydantic trying to create an instance of Subconfig
        # without any arguments. I don't fully understand why pydantic was creating an instance there.
        # But in any case, it presented as an error in this function and the real solution was to use
        # default_factory, e.g. `subconfig: Subconfig = Field(default_factory=Subconfig)`
        tree = []

        # Had issues before, leaving this in case (probably don't need it, see note above)
        # for field_name, field_info in cls.model_fields.items():
        for field_name in list(cls.model_json_schema(False).get("properties", [])):
            field_info = cls.model_fields[field_name]
            if field_info.annotation is None:
                raise RuntimeError(f"Field {field_name} in {cls.__name__} has no annotation")
            annotation_type: type = field_info.annotation

            if issubclass(annotation_type, CentralityConfig):
                sub_tree = annotation_type._build_field_tree()
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
        existing_slugs: dict[str, str] = {}  # dict[slug, dot]
        for new_slug, new_dot in undeduped_slugs:
            if new_slug in existing_slugs:
                existing_dot = existing_slugs[new_slug]
                raise CentralityConfigNameConflictError(cls, existing_dot, new_dot)
            existing_slugs[new_slug] = new_dot

    @classmethod
    def _find_envvars(cls) -> dict[str, str]:
        """
        Find all environment variables that match the config schema and return ovverrides in
        flattened dict format.
        """
        fields = {to_slug(dot): dot for dot in cls._build_field_tree()}
        prefix_slug = to_slug(f"CENTRALITY_{cls.__name__}")

        envvars = {}
        for k, v in os.environ.items():
            envvar_name_slug = to_slug(k)
            if envvar_name_slug.startswith(prefix_slug):
                field_slug = envvar_name_slug[len(prefix_slug) :]
                if field_slug not in fields:
                    raise CentralityConfigInvalidEnvvarOverrideError(
                        f"Environment variable {k} does not match any config fields"
                    )
                field_dot = fields[field_slug]
                envvars[field_dot] = v
        return envvars

    @classmethod
    def from_yaml_file(
        cls: Type[T], yaml_path: Path | str, config_overrides: Dict | None = None
    ) -> T:
        """Load a YAML file and return a config object."""
        # TODO: Allow loading from a URL
        if isinstance(yaml_path, str):
            yaml_path = Path(yaml_path)
        with open(yaml_path, "r") as f:
            yaml_dict = yaml.safe_load(f)
        return cls.from_dict(yaml_dict, config_overrides=config_overrides)

    def write_yaml(self, yaml_path: Path | str) -> None:
        """Save the config to a YAML file."""
        if isinstance(yaml_path, str):
            yaml_path = Path(yaml_path)
        with open(yaml_path, "w") as f:
            yaml.dump(self.to_dict(), f)

    @classmethod
    def from_json_file(
        cls: Type[T], json_path: Path | str, config_overrides: Dict | None = None
    ) -> T:
        """Load a JSON file and return a config object."""
        # TODO: Allow loading from a URL
        if isinstance(json_path, str):
            json_path = Path(json_path)
        with open(json_path, "r") as f:
            json_dict = json.load(f)
        return cls.from_dict(json_dict, config_overrides=config_overrides)

    def write_json(self, json_path: Path | str) -> None:
        """Save the config to a JSON file."""
        if isinstance(json_path, str):
            json_path = Path(json_path)
        with open(json_path, "w") as f:
            json.dump(self.to_dict(), f)

    @classmethod
    def from_dict(
        cls: Type[T], d: Dict, config_overrides: Dict | None = None
    ) -> T:
        """
        Load a dict and return a config object. Exists for code clarity.
        """
        if config_overrides:
            return cls(**d, config_overrides=config_overrides)
        return cls(**d)

    def to_dict(self) -> Dict:
        """
        Return the config as a dict. Exists for code clarity.
        """
        return self.model_dump()

    def to_dict_str(self) -> str:
        """
        Return the config as a json str. Exists for code clarity.
        """
        return self.model_dump_json()

    @classmethod
    def envvar_name(cls) -> str:
        """Return the environment variable name for saving and loading this config."""
        # SAVELOAD ensures it doesn't conflict with ENVOVERRIDEs pattern
        return f"CENTRALITY_SAVELOAD_{cls.__name__}".upper()

    @classmethod
    def from_envvar(cls: Type[T]) -> T:
        """Load the config from the environment variable."""
        envvar_name = cls.envvar_name()
        envvar_value = os.environ.get(envvar_name, None)
        if envvar_value is None:
            raise CentralityConfigEnvvarUnsetError(
                f"Environment variable {envvar_name} not set"
            )
        json_dict = json.loads(envvar_value)
        return cls.from_dict(json_dict)

    def save_to_envvar(self) -> None:
        """
        Save the config as an environment variable. This is useful for passing the config to subprocesses.
        """
        os.environ[self.envvar_name()] = self.model_dump_json()

    def pretty_print_yaml(self) -> None:
        """Print the config as a YAML string."""
        output = yaml.dump(self.to_dict())
        print(output)

    def pretty_print_json(self) -> None:
        """Print the config as a JSON string."""
        output = json.dumps(self.to_dict(), indent=4)
        print(output)
