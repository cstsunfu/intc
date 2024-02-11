# Copyright cstsunfu.
#
# This source code is licensed under the Apache license found in the
# LICENSE file in the root directory of this source tree.

import json
import os
import sys

import pytest

from intc import (
    FloatField,
    ListField,
    NestField,
    StrField,
    SubModule,
    cregister,
    ic_repo,
)
from intc.exceptions import ValueOutOfRangeError


@pytest.fixture(scope="module", autouse=True)
def ChildConfigForTestConfig():
    @cregister("child_module_for_test_config", "child_a")
    class ChildConfigForTestConfig:
        """child_a config"""

        i_am_child = StrField(value="child value", help="child value")

    yield ChildConfigForTestConfig
    cregister.registry.clear()
    ic_repo.clear()


@pytest.fixture(scope="module", autouse=True)
def ConfigAForTestConfig():
    @cregister("module_for_test_config", "config_a")
    class ConfigAForTestConfig:
        """config_a config"""

        epsilon = FloatField(value=1.0, minimum=0.0, additions=[-2.0], help="epsilon")
        submodule = SubModule(
            {
                "child_module_for_test_config#1": {
                    "i_am_child": "child value1",
                    "_base": "child_a",
                },
                "child_module_for_test_config#2": {
                    "i_am_child": "child value2",
                    "_base": "child_a",
                },
            }
        )

        class NestedConfig:
            nest_key = StrField(value="nest value", help="nest value")

        nested = NestField(NestedConfig)

    yield ConfigAForTestConfig
    cregister.registry.clear()
    ic_repo.clear()


@pytest.fixture(scope="module", autouse=True)
def ConfigA1ForTestConfig(ConfigAForTestConfig):
    @cregister("module_for_test_config", "config_a_1")
    class ConfigA1ForTestConfig(ConfigAForTestConfig):
        epsilon = FloatField(value=2.0, minimum=-10, help="epsilon")
        list_test = ListField(value=["name"], help="list checker")

    yield ConfigA1ForTestConfig


@pytest.fixture(scope="module", autouse=True)
def config_dict():
    config_a_1_for_test_dict = {
        "_name": "config_a_1",
        "nested": {"nest_key": "nest value"},
        "epsilon": 2.0,
        "list_test": ["name"],
        "@child_module_for_test_config#1": {
            "_name": "child_a",
            "i_am_child": "child value1",
        },
        "@child_module_for_test_config#2": {
            "_name": "child_a",
            "i_am_child": "child value2",
        },
    }

    yield config_a_1_for_test_dict


# Test module registration and retrieval
def test_module_registration_and_retrieval(ChildConfigForTestConfig):
    assert (
        cregister.get("child_module_for_test_config", "child_a")
        == ChildConfigForTestConfig._from_dict
    )


# Test module registration and retrieval
def test_config_dumps(ConfigA1ForTestConfig, config_dict):
    config = ConfigA1ForTestConfig()
    print(json.dumps(config._to_dict(), indent=4))

    assert json.dumps(config._to_dict(), sort_keys=True) == json.dumps(
        config_dict, sort_keys=True
    )


# Test config object equality
def test_config_equality(ConfigA1ForTestConfig):
    config1 = ConfigA1ForTestConfig()
    config2 = ConfigA1ForTestConfig._from_dict(config1._to_dict())
    assert config1 == config2


# Test config object equality
def test_float_check(ConfigAForTestConfig, ConfigA1ForTestConfig):
    config = ConfigAForTestConfig._from_dict({"epsilon": 2.0})
    assert config.epsilon == 2.0

    config = ConfigAForTestConfig._from_dict({"epsilon": -2.0})
    assert config.epsilon == -2.0

    with pytest.raises(ValueOutOfRangeError) as exc_info:
        ConfigAForTestConfig._from_dict({"epsilon": -3.0})
    # Check the error message
    assert "Value -3.0 is not in range [0.0" in str(exc_info.value)
    config = ConfigA1ForTestConfig._from_dict({"epsilon": -3.0})
    # Check the error message
    assert config.epsilon == -3.0


# Test field values of config objects
def test_config_field_values(ConfigAForTestConfig, ConfigA1ForTestConfig):
    config = ConfigAForTestConfig()
    assert config.epsilon == 1.0
    config = ConfigA1ForTestConfig()
    assert config.list_test == ["name"]
    assert config.epsilon == 2.0


# Test nested config objects
def test_nested_config(ConfigAForTestConfig):
    config = ConfigAForTestConfig()
    assert config.nested.nest_key == "nest value"


# Test children field of config objects
def test_children_field(ConfigAForTestConfig, ChildConfigForTestConfig):
    config = ConfigAForTestConfig()
    # assert isinstance(config.submodule, dict)
    assert isinstance(
        config.submodule["child_module_for_test_config#1"], ChildConfigForTestConfig
    )
    assert config["@child_module_for_test_config#1"].i_am_child == "child value1"
    assert (
        config.submodule["child_module_for_test_config#1"].i_am_child == "child value1"
    )


# Run the tests
if __name__ == "__main__":
    pytest.main()
