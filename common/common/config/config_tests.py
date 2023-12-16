from common.config.config import (
    CentralityConfig,
    CentralityConfigNameConflictError,
    CentralityConfigInvalidEnvvarOverrideError,
    CentralityConfigEnvvarUnsetError,
)
import os
import pytest
import pydantic
from pathlib import Path

"""
Tests to run:

- Test basic config with defaults
- Test that config without default breaks if argument not passed in
- Test that config without default works if argument passed in
- Test nested config
- Test argument overrides
- Test envvar overrides
- Test non-matching envvar override
- Test overrides to nested configs
- Test config with naming conflict
- Test loading from yaml
- Test loading from json
- Test saving and loading from envvar
"""

INT_VAL_1 = 10
INT_VAL_2 = 20
STRING_VAL_1 = "string_val_1"
STRING_VAL_2 = "string_val_2"


class BasicConfigWithDefaults(CentralityConfig):
    int_field_with_default: int = INT_VAL_1


class BasicConfigWithoutDefaults(CentralityConfig):
    int_field_no_default: int


class BasicNestedConfigParent(CentralityConfig):
    subconfig: BasicConfigWithDefaults = pydantic.Field(
        default_factory=BasicConfigWithDefaults
    )


class Subconfig(CentralityConfig):
    string_field_with_default: str = STRING_VAL_1
    string_field_without_default: str


class ParentConfig(CentralityConfig):
    subconfig: Subconfig = pydantic.Field(default_factory=Subconfig)


class NameConflictChildOneConfig(CentralityConfig):
    on_start: str = STRING_VAL_1


class NameConflictChildTwoConfig(CentralityConfig):
    start: str = STRING_VAL_2


class NameConflictParentConfig(CentralityConfig):
    child: NameConflictChildOneConfig = pydantic.Field(
        default_factory=NameConflictChildOneConfig
    )
    child_on: NameConflictChildTwoConfig = pydantic.Field(
        default_factory=NameConflictChildTwoConfig
    )


def test_basic_config_with_defaults():
    config = BasicConfigWithDefaults()
    assert config.int_field_with_default == INT_VAL_1


def test_basic_config_without_default_errors():
    with pytest.raises(pydantic.ValidationError):
        _ = BasicConfigWithoutDefaults()


def test_basic_config_without_default_works_when_value_set():
    config = BasicConfigWithoutDefaults(int_field_no_default=INT_VAL_1)
    assert config.int_field_no_default == INT_VAL_1


def test_nested_config():
    config = BasicNestedConfigParent()
    assert isinstance(config.subconfig, BasicConfigWithDefaults)
    assert config.subconfig.int_field_with_default == INT_VAL_1


def test_argument_overrides():
    config = BasicConfigWithoutDefaults(
        config_overrides=dict(int_field_no_default=INT_VAL_1)
    )
    assert config.int_field_no_default == INT_VAL_1


def test_envvar_override():
    os.environ["CENTRALITY_BASICCONFIGWITHOUTDEFAULTS_INT_FIELD_NO_DEFAULT"] = str(
        INT_VAL_1
    )
    config = BasicConfigWithoutDefaults()
    assert config.int_field_no_default == INT_VAL_1
    del os.environ["CENTRALITY_BASICCONFIGWITHOUTDEFAULTS_INT_FIELD_NO_DEFAULT"]


def test_invalid_envvar_override():
    with pytest.raises(CentralityConfigInvalidEnvvarOverrideError):
        os.environ[
            "CENTRALITY_BASICCONFIGWITHOUTDEFAULTS_INT_FIELD_NO_DEFAULTSSS"
        ] = str(INT_VAL_1)
        config = BasicConfigWithoutDefaults()
        assert config.int_field_no_default == INT_VAL_1
        del os.environ["CENTRALITY_BASICCONFIGWITHOUTDEFAULTS_INT_FIELD_NO_DEFAULTSSS"]


def test_nested_config_override():
    config = ParentConfig(
        config_overrides={"subconfig.string_field_without_default": STRING_VAL_2}
    )
    assert config.subconfig.string_field_with_default == STRING_VAL_1
    assert config.subconfig.string_field_without_default == STRING_VAL_2


def test_naming_conflict():
    with pytest.raises(CentralityConfigNameConflictError):
        _ = NameConflictParentConfig()


def test_to_from_yaml():
    yaml_path = Path(__file__).parent / "test.yaml"
    if yaml_path.exists():
        raise RuntimeError("Temp file yaml path already exists")
    config1 = BasicNestedConfigParent()
    config1.write_yaml(yaml_path)

    config2 = BasicNestedConfigParent.from_yaml_file(yaml_path)
    assert config2.subconfig.int_field_with_default == INT_VAL_1
    assert config2 == config1

    # Cleanup
    os.remove(yaml_path)


def test_to_from_json():
    json_path = Path(__file__).parent / "test.json"
    if json_path.exists():
        raise RuntimeError("Temp file json path already exists")
    config1 = BasicNestedConfigParent()
    config1.write_json(json_path)

    config2 = BasicNestedConfigParent.from_json_file(json_path)

    assert config2.subconfig.int_field_with_default == INT_VAL_1
    assert config2 == config1

    # Cleanup
    os.remove(json_path)


def test_to_from_envvar():
    if BasicNestedConfigParent.envvar_name() in os.environ:
        raise RuntimeError("Environment Variable already set")

    config1 = BasicNestedConfigParent()
    config1.save_to_envvar()
    assert BasicNestedConfigParent.envvar_name() in os.environ
    config2 = BasicNestedConfigParent.from_envvar()
    assert config2.subconfig.int_field_with_default == INT_VAL_1
    assert config2 == config1

    # Cleanup
    del os.environ[BasicNestedConfigParent.envvar_name()]


def test_from_unset_envvar_errors():
    with pytest.raises(CentralityConfigEnvvarUnsetError):
        _ = BasicNestedConfigParent.from_envvar()


if __name__ == "__main__":
    test_basic_config_with_defaults()
    test_basic_config_without_default_errors()
    test_basic_config_without_default_works_when_value_set()
    test_nested_config()
    test_argument_overrides()
    test_envvar_override()
    test_invalid_envvar_override()
    test_nested_config_override()
    test_naming_conflict()
    test_to_from_yaml()
    test_to_from_json()
    test_to_from_envvar()
    test_from_unset_envvar_errors()
