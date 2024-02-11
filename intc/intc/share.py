# Copyright the author(s) of intc.
#
# This source code is licensed under the Apache license found in the
# LICENSE file in the root directory of this source tree.

from typing import Any, Callable, Dict, Type, Union

from intc.exceptions import NoModuleFoundError

registry: Dict[str, Any] = {}


MISSING = "???"
LOAD_SUBMODULE_DONE = False


def get_registed_instance(
    type_name: str, name: str = "", get_class=False
) -> Union[Type, Callable]:
    """get the module by name

    Args:
        type_name: the module type name
        name: the module name
        get_class: return the module class if True, else return the module class's _from_dict method

    Returns:
        registered module

    """
    if type_name not in registry:
        raise NoModuleFoundError(f"There is not a registerd type named '{type_name}'")
    if name not in registry[type_name]:
        raise NoModuleFoundError(
            f"In '{type_name}' register, there is not a entry named '{name}'"
        )
    if get_class:
        return registry[type_name][name]
    return registry[type_name][name]._from_dict
