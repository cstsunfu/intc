# Copyright the author(s) of intc.
#
# This source code is licensed under the Apache license found in the
# LICENSE file in the root directory of this source tree.

import inspect
from typing import Any, Callable, Dict, Type, TypeVar

from attrs import asdict, define, field, fields, fields_dict

from intc.config import Base
from intc.exceptions import (
    InConsistentNameError,
    NameError,
    NoModuleFoundError,
    RepeatRegisterError,
)
from intc.share import get_registed_instance, registry
from intc.utils import module_name_check

ic_repo = {}
ic_help = {}
type_module_map = {}

SpecificConfig = TypeVar("SpecificConfig")


class Register(object):
    """Register"""

    registry = registry

    def __init__(self):
        self.built_in_field = {
            "_base": {
                "description": "The inherit base module name",
                "type_name": "BaseField",
                "type": "string",
            },
            "_G": {
                "description": "The global parameters\nYou can reference them anywhere start with `~` or `_G` ",
                "type": "object",
                "type_name": "Global",
            },
            "_anchor": {
                "description": "The reference anchor.",
                "type_name": "Anchor",
                "type": "object",
            },
            "_search": {
                "description": "Search the parameters(cartesian product).",
                "type_name": "Search",
                "type": "object",
            },
        }

    def register(self, type_name: str = "", name: str = "") -> Callable:
        """register the named module, you can only provide the type name, or type name and module name

        Args:
            type_name: the type name
            name: the specific module name in the type

        Returns:
            the module

        """
        skip_regist = False  # if the type_name is not provided, we will skip register the module to the registry
        if not type_name:
            assert (
                not name
            ), "You must provide the type name if you want to register a module"
            skip_regist = True
        if not skip_regist:
            module_name_check(type_name)
            if name:
                module_name_check(name)

        def get_help(wrap_module, is_nest=False):
            help_dict = {}
            lines, line_no = inspect.getsourcelines(wrap_module)
            source_file = inspect.getabsfile(wrap_module)
            help_dict["position"] = {
                "file_path": source_file,
                "line_no": line_no,
            }
            help_dict["lines"] = lines
            help_dict["properties"] = {}

            for key in fields(wrap_module):
                if (not is_nest) and key.name == "submodule":
                    assert key.metadata["type_name"] == "SubModule"
                    module_types = []

                    if key.metadata.get("suggestions", None):
                        module_types = key.metadata["suggestions"]
                    if key.default and isinstance(key.default, dict):
                        for module_type in key.default:
                            module_types.append(module_type)
                    module_types = [
                        module_type.lstrip("@") for module_type in module_types
                    ]
                    for child in module_types:
                        help_dict["properties"][f"@{child}"] = {
                            "type": "object",
                            "type_name": "SubModule",
                            "properties": {},
                            "default": {},
                        }
                        if (
                            isinstance(key.default, dict)
                            and child in key.default
                            and isinstance(key.default[child], dict)
                            and (
                                "_base" in key.default[child]
                                or "_name" in key.default[child]
                            )
                        ):
                            base = key.default[child].get("_base", "") or key.default[
                                child
                            ].get("_name", "")
                            help_dict["properties"][f"@{child}"]["default"] = {
                                "_base": base
                            }
                elif key.metadata["type_name"] == "NestField":
                    nest_help = get_help(
                        define(key.metadata["object_type"]), is_nest=True
                    ).get("properties", {})
                    metadata_dict = dict(key.metadata)
                    metadata_dict.pop("object_type")
                    help_dict["properties"][key.name] = metadata_dict
                    help_dict["properties"][key.name]["properties"] = nest_help
                else:
                    help_dict["properties"][key.name] = {
                        k: key.metadata[k]
                        for k in key.metadata
                        if k not in {"object_type"}
                    }
            return help_dict

        def decorator(module) -> Base:
            if not skip_regist and type_name not in registry:
                registry[type_name] = {}
            if not skip_regist and name in registry[type_name]:
                raise RepeatRegisterError(
                    f"The {name} is already registered in {type_name}. Registed: {registry[type_name][name]}"
                )

            module_doc = module.__doc__
            if module.__bases__ == (object,):
                module = type(module.__name__, (Base,), dict(module.__dict__))
            wrap_module = define(module)

            field_help = get_help(wrap_module)
            field_help["properties"] = field_help.get("properties", {})
            for built_in in self.built_in_field:
                field_help["properties"][built_in] = self.built_in_field[built_in]
            field_help["_name"] = name
            field_help["description"] = (
                module_doc if module_doc else "No Module Document"
            )
            wrap_module.__meta__ = field_help
            if not skip_regist:
                registry[type_name][name] = wrap_module
                ic_help[(type_name, name)] = field_help
                type_modules = type_module_map.get(type_name, set())
                type_modules.add(name)
                type_module_map[type_name] = type_modules
                ic_repo[(type_name, name)] = wrap_module()._to_dict(lazy=True)
            return wrap_module

        return decorator

    def get(self, type_name: str, name: str = "", get_class=False) -> Any:
        """get the module by name

        Args:
            type_name: the module type name
            name: the module name
            get_class: return the module class if True, else return the module class's _from_dict method

        Returns:
            registered module

        """
        return get_registed_instance(type_name, name, get_class)

    def __call__(
        self, type_name: str = "", name: str = ""
    ) -> Callable[[Type[SpecificConfig]], Type[SpecificConfig]]:
        """you can directly call the object, the behavior is the same as object.register(name)"""

        return self.register(type_name, name)

    def __getitem__(self, type_and_name: tuple) -> Any:
        """wrap for object.get(name)"""
        type_name, name = type_and_name
        return get_registed_instance(type_name, name)


cregister = Register()
dataclass = cregister.register()
