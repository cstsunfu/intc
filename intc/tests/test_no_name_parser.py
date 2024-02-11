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
    Parser,
    StrField,
    SubModule,
    cregister,
    ic_repo,
    init_config,
)
from intc.exceptions import ValueOutOfRangeError


@pytest.fixture(scope="module", autouse=True)
def ChildConfigForTestParser():
    @cregister("child_module_for_test_parser")
    class ChildConfigForTestParser:
        """child config"""

        i_am_child = StrField(value="child value", help="child value")
        i_am_float_child = FloatField(value=0, help="child value")

    yield ChildConfigForTestParser
    cregister.registry.clear()
    ic_repo.clear()


@pytest.fixture(scope="module", autouse=True)
def ConfigAForTestParser():
    @cregister("module_for_test_parser")
    class ConfigAForTestParser:
        """module_for_test_parser"""

        epsilon = FloatField(value=1.0, minimum=0.0, additions=[-2], help="epsilon")
        list_test = ListField(value=["name"], help="list checker")
        submodule = SubModule(
            {
                "child_module_for_test_parser#1": {"i_am_child": "child value1"},
                "child_module_for_test_parser#2": {"i_am_child": "child value2"},
            }
        )

        class NestedConfig:
            nest_key = StrField(value="nest value", help="nest value")
            nest_key2 = FloatField(value=0, help="nest value2")

        nested = NestField(NestedConfig)

    yield ConfigAForTestParser
    cregister.registry.clear()
    ic_repo.clear()


# Test simple config
def test_simple_parser(ChildConfigForTestParser):
    # assert cregister.get('child_a', 'child_module') == ChildConfigForTestParser._from_dict
    config = {
        "@module_for_test_parser": {
            "epsilon": 8.0,
        }
    }
    config = init_config(Parser(config).parser()[0])
    assert config["@module_for_test_parser"].epsilon == 8.0


def test_reference_parser(ConfigAForTestParser, ChildConfigForTestParser):
    assert (
        cregister.get("child_module_for_test_parser")
        == ChildConfigForTestParser._from_dict
    )
    config = {
        "@module_for_test_parser": {
            "_anchor": "module",
            # "epsilon": 8.0,
            "nested": {
                "nest_key": "@$.#2.i_am_child, @$.#new.i_am_child @lambda x, y: x+y",
            },
            "@child_module_for_test_parser#1": {
                "i_am_float_child": "@module.epsilon @lambda x: x+1"
            },
            "@child_module_for_test_parser#new": {"i_am_child": "new child value"},
        },
        "_search": {
            "@module_for_test_parser.epsilon": [3, 4, 8.0],
        },
    }
    configs = Parser(config).parser()
    assert len(configs) == 3
    assert init_config(configs[0])["@module_for_test_parser"].epsilon == 3
    assert (
        init_config(configs[0])["@module_for_test_parser"].nested.nest_key
        == "child value2" + "new child value"
    )
    assert init_config(configs[1])["@module_for_test_parser"].epsilon == 4
    assert init_config(configs[2])["@module_for_test_parser"].epsilon == 8


# Run the tests
if __name__ == "__main__":
    pytest.main()
