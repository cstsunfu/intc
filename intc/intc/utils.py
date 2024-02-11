# Copyright the author(s) of intc.
#
# This source code is licensed under the Apache license found in the
# LICENSE file in the root directory of this source tree.

# FIXME: fix_trace only for segment error, and add the submodule index
import copy
import inspect
import re
from typing import Any, Callable, Dict, List, Tuple, Type, Union

from intc.exceptions import KeyNotFoundError, NameError, ValueMissingError

_module_name_pattern = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*-?[a-zA-Z0-9_]*$")


def get_meta_rep(metadata):
    rep = ""
    help = ""
    for key in metadata:
        if key != "description":
            rep += f"{key}: {metadata[key]}. "
        else:
            help = metadata[key]
    if help:
        rep += f"help: {help}"

    return rep


def split_trace(trace_str: str) -> List[str]:
    """
    split the trace path to list, especially for the '.global'/'.base'/etc.
    `a.b.c` -> `['a', 'b', 'c']`
    `a.b.c..base` -> `['a', 'b', 'c', '.base']`

    Args:
        trace_str: the trace path like `a.b.c`

    Returns:
        trace list

    """
    result = []
    sub_trace = ""
    for c in trace_str:
        if c == "." and sub_trace:
            result.append(sub_trace)
            sub_trace = ""
        else:
            sub_trace += c
    if sub_trace:
        result.append(sub_trace)
    return result


def get_position():
    """get the parameter definition position
    Returns:
        position
    """
    frame = inspect.currentframe().f_back.f_back
    line_no = inspect.getlineno(frame)
    file_path = inspect.getabsfile(frame)
    return {"file_path": file_path, "line_no": line_no}


def module_name_check(name):
    """check the module name is valid

    Args:
        name: module name

    Returns:
        None
    Raises:
        NameError: if the name is invalid
    """
    if not _module_name_pattern.match(name):
        raise NameError(f"Module name '{name}' is invalid")


def _inplace_update_dict(_base: Dict, _new: Dict):
    """use the _new dict inplace update the _base dict, recursively

    if the _base['_name'] != _new["_name"], we will use _new cover the _base and logger a warning
    otherwise, use _new update the _base recursively

    Args:
        _base: will be updated dict
        _new: use _new update _base

    Returns:
        None

    """
    for item in _new:
        if (item not in _base) or (not isinstance(_base[item], Dict)):
            _base[item] = _new[item]
        elif isinstance(_base[item], Dict) and isinstance(_new[item], Dict):
            _inplace_update_dict(_base[item], _new[item])
        else:
            raise AttributeError(
                "The base config and update config is not match. base: {}, new: {}. ".format(
                    _base, _new
                )
            )


def do_update_config(config: dict, update_config: dict) -> Dict:
    """use the update_config dict update the config dict, recursively

    see ConfigTool._inplace_update_dict

    Args:
        config: will be updated dict
        update_confg: config: use _new update _base

    Returns:
        updated_config

    """
    if not update_config:
        update_config = {}
    config = copy.deepcopy(config)
    _inplace_update_dict(config, update_config)
    return config


def fix_trace(trace: str, root_config: Dict):
    """get the value of trace in config"""
    trace_config = root_config

    trace_list = split_trace(trace)
    new_trace_list = []
    try:
        for s in trace_list:
            if isinstance(trace_config, list):
                assert (s[0] == "-" and str.isdigit(s[1:])) or str.isdigit(
                    s
                ), "list index must be int"
                s = int(s)
            else:
                assert isinstance(trace_config, dict), f"trace {trace} is invalid"
                s = UniModuleName(trace_config.keys())[s]
            trace_config = trace_config[s]
            new_trace_list.append(str(s))
    except KeyNotFoundError as e:
        raise e
    except Exception as e:
        raise KeyError(f"Can not find the link trace '{trace}' in config, {e}")
    return ".".join(new_trace_list)


class UniModuleName(object):
    """Unique submodule names"""

    def __init__(self, keys):
        super(UniModuleName, self).__init__()
        self.origin_keys = list(keys)
        self.keys = self.update_uni_keys(keys)

    def update_uni_keys(self, keys: List[str]) -> Dict[str, str]:
        """add the clear key which could represent the origin key to the uni_keys
        case 1: the original keys are {"@A#a", "@B#a", "@B#c", "@CD#a"}, we can use "@A" represent "@A#a", "#c" represent "@B#c" and "@CD" represent "@CD#a" without ambiguous, but "#a" is ambiguous for "@A#a" and "@CD#a", "@B" is ambiguous for "@B#a" and "@B#c", so we can not use them to represent the origin key. The final update keys are {"@A#a", "@B#a", "@B#c", "@C#a", "@A", "#c", "@CD"}.
        case 2: the original keys are {"@A@B#c"}, we can use "@A", "@A@B", "#c" represent the "@A@B#c", we can also omit the "A" or "B", only use the "@@B", "@@B#c", "@A@#c", "@@#c" to represent the "@A@B#c", so the final update keys are {"@A@B#c", "@A", "@B", "@A@B", "@@B", "#c", "@A@#c", "@@#c"}.

        Args:
            keys: origin keys

        Returns:
            update keys those are no conflict
        """
        uni_key_map = {}
        extend_key_count = {}
        reserved_keys = set(keys)
        for key in keys:
            uni_key_map[key] = key
        for key in keys:
            if key.startswith("@"):
                prefixes = {""}
                cur = ""
                for c in key:
                    if c in {"@", "#"}:
                        if cur:
                            assert cur[0] in {"@", "#"}
                            update = set()
                            for prefix in prefixes:
                                update.add(f"{prefix}{cur}")
                                update.add(f"{prefix}{cur[0]}")
                            prefixes.update(update)
                        cur = c
                    else:
                        cur = f"{cur}{c}"
                if cur:
                    update = set()
                    for prefix in prefixes:
                        update.add(f"{prefix}{cur}")
                        update.add(f"{prefix}{cur[0]}")
                    prefixes.update(update)
                for prefix in prefixes:
                    if prefix in reserved_keys:
                        continue
                    cset = set(prefix)
                    cset.discard("@")
                    cset.discard("#")
                    if not cset:
                        continue
                    if prefix[-1] in {"@", "#"}:
                        continue
                    extend_key_count[prefix] = extend_key_count.get(prefix, 0) + 1
                    if extend_key_count[prefix] > 1:
                        uni_key_map.pop(prefix, "")
                    else:
                        uni_key_map[prefix] = key

        return uni_key_map

    def __getitem__(self, key):
        if key in self.keys:
            return self.keys[key]
        raise KeyNotFoundError(f"Key {key} is ambiguous in {self.origin_keys}")


def search_lambda_eval(search_para: Any) -> Any:
    """eval the lambda function in config

    Args:
        search_para:
            the value of search_para or the whole(dict) config
            search lambda only support @lambda _: eval rep
    Returns:
        processed search_para
    """
    if isinstance(search_para, dict):
        return {k: search_lambda_eval(v) for k, v in search_para.items()}
    elif isinstance(search_para, list):
        return [search_lambda_eval(v) for v in search_para]
    elif isinstance(search_para, str):
        if search_para.startswith("@lambda"):
            return eval(f"lambda _:{':'.join(search_para.split(':')[1:])}")(0)
        else:
            return search_para
    else:
        return search_para


def parser_lambda_key_value_pair(
    key: str, lambda_value: str, ref_anchor_maps: Dict, root_config: Dict
) -> Dict:
    """parser the lambda representation to key, paras, lambda
    Args:
        lambda_key:
            the key of a dict, just a string
        lambda_value: like
             1. "value" for the vanailla value
             2. "@lambda _: list(range(4))" for the eval value
             3. "@anchor1.key1.value1, @anchor2.key2.value2 @lambda x, y: x+y" for the lambda value
             4. "@lambda @anchor.value" for just reference

        ref_anchor_maps:
            the anchor maps like
            {
                "global": "root.global",
                "$": "root.module.module",
                "module_root": "root.module",
            }
    Returns:
        the parser result(Dict)
    """

    def anchor_parser(para):
        if para.strip() == "_":
            return "_"
        assert para.startswith(
            "@"
        ), f"the reference {para} is invalid, the reference must be like '@anchor.key.value'"
        para_split = split_trace(para[1:])

        assert (
            len(para_split) >= 2
        ), f"the reference {para} is invalid, the reference must be like '@anchor.key.value'"
        para_split[0] = ref_anchor_maps[para_split[0]]
        return fix_trace(".".join(para_split), root_config)

    paras = []
    lambda_fun = "lambda x: x"
    lambda_value = lambda_value.strip()
    if lambda_value.startswith("@lambda"):
        lambda_value = lambda_value.lstrip("@lambda").strip()
        assert (
            len(lambda_value.split(":")) == 2
            and (lambda_value.split(":")[0].strip() == "_")
        ) or (
            ":" not in lambda_value and "," not in lambda_value
        ), f"the lambda value 'lambda {lambda_value}' is invalid, only support 'lambda _: evaluable_expr' for evaluation value or 'lambda @anchor.key.value' for reference value."
        if lambda_value.split(":")[0].strip() == "_":
            return {
                "key": key,
                "paras": ["_"],
                "lambda": f"lambda {lambda_value}",
            }
        else:
            return {
                "key": key,
                "paras": [anchor_parser(lambda_value.strip())],
                "lambda": "lambda x: x",
            }
    elif "@lambda" in lambda_value:
        value_splits = lambda_value.split("@lambda")
        assert (
            len(value_splits) == 2
        ), f"the lambda value {lambda_value} is invalid, the lambda value must be like '@anchor.value @lambda x: x+1'"
        _paras, lambda_fun = value_splits
        for para in _paras.split(","):
            paras.append(anchor_parser(para.strip()))
        lambda_fun = f"lambda {lambda_fun.strip()}"
        return {
            "key": key,
            "paras": paras,
            "lambda": lambda_fun,
        }
    else:
        return {}
