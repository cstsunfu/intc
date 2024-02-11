# Copyright the author(s) of intc.
#
# This source code is licensed under the Apache license found in the
# LICENSE file in the root directory of this source tree.

import copy
import json
from typing import Any, Callable, Dict, List, Type, TypeVar, Union

import intc.share as G
from intc.config import Base, DataClassType, init_config
from intc.exceptions import KeyNotFoundError, ParserConfigRepeatError, ValueError
from intc.loader import load_submodule
from intc.register import cregister, ic_repo
from intc.share import MISSING
from intc.utils import (
    do_update_config,
    fix_trace,
    parser_lambda_key_value_pair,
    search_lambda_eval,
    split_trace,
)


class Parser(object):
    reserved = {"_name", "_search", "_anchor", "submodule"}
    """BaseConfigParser
    The config parser order is: inherit -> search -> reference

    If some config is marked as $MISSING, this means the para has not default value, you must covered it(like 'label_nums', etc.).

    """

    def __init__(self, raw_config: Dict, module_type: str = "__root__"):
        super(Parser, self).__init__()
        if not G.LOAD_SUBMODULE_DONE:
            load_submodule()
        self.search = {}
        self.root = False
        self.module_type = module_type
        if module_type == "_G":
            self.raw_config = copy.deepcopy(raw_config)
            return

        if module_type == "__root__":
            self.root = True
            _G = raw_config.pop("_G", {})
            if not _G:
                _G = {"__hold__": None}
            raw_config = {"@__root__init__": raw_config, "_G": _G}
        # if the module_type is like "@module_type@module_name#..." and "_base" is not in config, set the base as "module_name"
        elif "@" in module_type and "_base" not in raw_config:
            _module_type_name = module_type.lstrip("@").split("@")
            assert len(_module_type_name) == 2
            raw_config["_base"] = _module_type_name[1].split("#")[0]
        self.raw_config = copy.deepcopy(raw_config)

        if not self.root and "_G" in self.raw_config:
            raise ValueError("the '_G' key only support in root module")
        if "submodule" in self.raw_config:
            raise ValueError("the 'submodule' key is reserved")

        # get base config
        if self.raw_config.get("_base", ""):
            self.base_config = self.get_base_config(
                module_type, self.raw_config["_base"]
            )
        elif self.raw_config.get("_name", ""):
            self.base_config = self.get_base_config(
                module_type, self.raw_config["_name"]
            )
        elif not self.root:
            self.base_config = self.get_base_config(module_type, "")
        else:
            self.base_config = {}

        self.raw_config.pop("_base", {})

        # get the module _anchor
        ref_anchor = self.base_config.pop("_anchor", "$")
        assert (
            ref_anchor == "$"
        ), f"the _anchor of only support for the final config(which should not be inherited)"
        raw_ref_anchor = self.raw_config.pop("_anchor", "$")
        assert isinstance(
            raw_ref_anchor, str
        ), f"_anchor must be str, but got {raw_ref_anchor}"
        assert (
            "." not in raw_ref_anchor
        ), f"_anchor '{raw_ref_anchor}' can not contain '.'."
        assert raw_ref_anchor not in {
            "~",
            "_G",
        }, f"'{raw_ref_anchor}' is the reserved global anchor."
        self.raw_config["_anchor"] = raw_ref_anchor

        # restructure the submodule
        if "submodule" in self.raw_config:
            submodule = self.raw_config.pop("submodule")
            for key, value in submodule.items():
                self.raw_config[f"@{key}"] = value

        self.raw_config = do_update_config(self.base_config, self.raw_config)

        # search only for module level
        self.search = self.raw_config.pop("_search", {})

    def parser_init(self, DataClass: Type[DataClassType] = Base) -> List[DataClassType]:
        """parser the config and check the config is valid

        Args:
            parser_ref: whether parser the reference

        Returns: all valided init config(if the DataClass is not None or False)

        """
        configs = self.parser(parser_ref=True)
        self.check_config(configs)

        if not DataClass:
            return configs

        return [init_config(config, DataClass) for config in configs]

    def parser(self, parser_ref=True) -> List:
        """parser the config

        Args:
            parser_ref: whether parser the links

        Returns: all valided configs

        """
        # parser submodules get submodules config
        modules_config = {}
        for module_type in self.raw_config:
            modules_config[module_type] = self.get_kind_module_base_config(
                self.raw_config[module_type], module_type
            )

        # expand all submodules to combine a set of module configs
        possible_config_list = self.get_named_list_cartesian_prod(modules_config)

        # flat all search paras
        all_possible_config_list = []
        for possible_config in possible_config_list:
            fix_search_para = {}
            for key, value in self.search.items():
                fix_search_para[fix_trace(key, possible_config)] = value
            search = search_lambda_eval(fix_search_para)
            all_possible_config_list.extend(
                self.flat_search(search, possible_config, self.module_type)
            )

        # link paras
        if parser_ref:
            ref_anchor_maps = {}
            if self.root:
                ref_anchor_maps = {"~": "_G", "_G": "_G"}
            _all_possible_config_list = []
            for possible_config in all_possible_config_list:
                current_ref_anchor_maps = copy.deepcopy(ref_anchor_maps)
                self.collect_global_anchors(
                    possible_config,
                    ref_anchor_maps=current_ref_anchor_maps,
                    trace="",
                    root=True,
                )
                all_refs = self.collect_refs(
                    possible_config,
                    possible_config,
                    refs=[],
                    ref_anchor_maps=current_ref_anchor_maps,
                    trace="",
                    root=True,
                )
                possible_config = self.do_parser_refs(all_refs, possible_config)
                _all_possible_config_list.append(possible_config)
            all_possible_config_list = _all_possible_config_list

        return_list = copy.deepcopy(all_possible_config_list)

        if self.is_rep_config(return_list):
            for i, config in enumerate(return_list):
                print(f"Found Repeat Configs")
                print(f"The {i}th Configure is:")
                print(json.dumps(config, indent=2, ensure_ascii=False))
            raise ParserConfigRepeatError("REPEAT CONFIG")

        if not self.root:
            return return_list
        drop_root_return_list = []
        for config in return_list:
            drop_root_config = config.pop("@__root__init__", {})
            drop_root_return_list.append(drop_root_config)
        return drop_root_return_list

    @classmethod
    def get_base_config(cls, module_type: str, module_name: str = "") -> Dict:
        """get the base config use the module_type

        Args:
            module_type: the config name

        Returns:
            config of the module_type
        """
        module_type = module_type.split("#")[0].split("@")[0]
        config = ic_repo.get((module_type, module_name), {})
        if config.get("_base", "") == "":
            return config
        base_config = cls(raw_config=config, module_type=module_type).parser(
            parser_ref=False
        )
        if len(base_config) > 1:
            raise PermissionError("The base config don't support para_search now.")
        if base_config:
            return base_config[0]
        return {}

    @staticmethod
    def do_parser_refs(refs: List, config: Dict):
        """inplace parser ref on config

        Args:
            refs:
                [
                    {
                        "key": 'root.module.module.config.key',
                        "paras": ["root.module.module.config.key2"],
                        "lambda": f"lambda x: x",
                    },
                    {
                        "key": key,
                        "paras": ["_"],
                        "lambda": f"lambda {lambda_value}",
                    }
                ]
            config: will linked base config

        Returns:
            None

        """
        if not refs:
            return config
        if not config:
            assert len(refs) == 0, f"the config is empty, but the refs is {refs}."
            return config
        # TOPSORT
        nodes = {}
        for ref in refs:
            if ref["key"] not in nodes:
                nodes[ref["key"]] = {
                    "parents": set(),
                    "children": set(),
                    "value": {"paras": ref["paras"], "lambda": ref["lambda"]},
                }
            else:
                assert nodes[ref["key"]]["value"] == None
                nodes[ref["key"]]["value"] = {
                    "paras": ref["paras"],
                    "lambda": ref["lambda"],
                }
            for para in ref["paras"]:
                if para not in nodes:
                    nodes[para] = {"parents": set(), "children": set(), "value": None}
                nodes[ref["key"]]["parents"].add(para)
                nodes[para]["children"].add(ref["key"])

        def _get_trace_value(trace: str):
            """get the value of trace in config"""
            trace_config = config
            if trace.strip() == "_":
                return None
            trace_list = split_trace(trace)
            try:
                for s in trace_list:
                    if isinstance(trace_config, list):
                        assert (s[0] == "-" and str.isdigit(s[1:])) or str.isdigit(
                            s
                        ), "list index must be int"
                        s = int(s)
                    else:
                        assert isinstance(
                            trace_config, dict
                        ), f"trace {trace} is invalid"
                        assert isinstance(s, str)
                    trace_config = trace_config[s]
            except:
                raise KeyError(f"Can not find the link trace '{trace}' in config")
            return trace_config

        def _get_lambda_value(lambda_config, _node_value_map):
            """get the value of lambda_config"""
            _lambda_keys = lambda_config["paras"]
            _lambda_paras = [_node_value_map[key] for key in _lambda_keys]
            return eval(lambda_config["lambda"])(*(_lambda_paras))

        node_value_map = {}

        while nodes:
            circle_flag = True
            for key, node in nodes.items():
                if not node["parents"]:
                    if not node["value"]:
                        node_value_map[key] = _get_trace_value(key)
                    else:
                        node_value_map[key] = _get_lambda_value(
                            node["value"], node_value_map
                        )
                    for child in node["children"]:
                        nodes[child]["parents"].remove(key)
                    nodes.pop(key)
                    circle_flag = False
                    break
            if circle_flag:
                raise PermissionError(
                    f"The config link has circle, please check:\n{json.dumps(refs, indent=4)}"
                )

        def _set_trace_value(trace: str, value):
            """set the value of trace in config"""
            trace_config: Dict = config
            trace_list = split_trace(trace)
            trace_last: Union[str, int] = trace_list[-1]
            try:
                for s in trace_list[:-1]:
                    if isinstance(trace_config, list):
                        assert (s[0] == "-" and str.isdigit(s[1:])) or str.isdigit(
                            s
                        ), "list index must be int"
                        s = int(s)
                        trace_config = trace_config[s]
                    else:  # ..........just for drop the typing error.
                        trace_config = trace_config[s]
            except:
                raise KeyError(f"Can not find the link trace '{trace}' in config")
            if isinstance(trace_config, list):
                assert (
                    trace_list[-1][0] == "-" and str.isdigit(trace_list[-1][1:])
                ) or str.isdigit(trace_list[-1]), "list index must be int"
                trace_last = int(trace_list[-1])
                trace_config[trace_last] = value
            else:  # for trace_config is dict
                trace_config[trace_last] = value

        node_value_map.pop("_", {})
        for key, value in node_value_map.items():
            _set_trace_value(key, value)
        return config

    @classmethod
    def collect_global_anchors(
        cls,
        cur_config: Dict,
        ref_anchor_maps: Dict,
        trace: str = "",
        key=None,
        root=False,
    ):
        """collect move all links in cur_config to top

        only do in the top level of cur_config, collect all level links and return the links with level

        Args:
            cur_config:
                >>> {
                >>>     "_anchor": "anchor1",
                >>>     "arg1": {
                >>>         "arg11": 2,
                >>>         "arg12": "@anchor1.arg1.arg11 @lambda x: x+1"
                >>>     }
                >>> }
            ref_anchor_maps:
                collected global anchor abs path map
            trace:
                the trace from root to current node
            key:
                the key of current node

        Returns:
            None

        """
        if isinstance(cur_config, list):
            for i, config_i in enumerate(cur_config):
                cls.collect_global_anchors(
                    cur_config=config_i,
                    ref_anchor_maps=ref_anchor_maps,
                    trace=f"{trace}.{i}",
                )
        elif isinstance(cur_config, dict):
            if key and isinstance(key, str) and key.startswith("@"):
                anchor_addable = True
            else:
                anchor_addable = False or root
            if "_anchor" in cur_config:
                assert (
                    anchor_addable
                ), f"_anchor is not addable in {trace}, the anchor only support add to the module config level."
                _anchor = cur_config["_anchor"]
                if _anchor != "$":
                    assert (
                        _anchor not in ref_anchor_maps
                    ), f"the anchor '{_anchor}' is repeated defined, please check."
                    ref_anchor_maps[_anchor] = trace
            for submodule_name, submodule_config in cur_config.items():
                if submodule_name == "_anchor":
                    continue
                assert isinstance(submodule_name, str)
                cur_trace = trace + "." + submodule_name if trace else submodule_name
                cls.collect_global_anchors(
                    cur_config=submodule_config,
                    ref_anchor_maps=ref_anchor_maps,
                    trace=cur_trace,
                    key=submodule_name,
                )

    @classmethod
    def collect_refs(
        cls,
        cur_config: Dict,
        root_config: Dict,
        refs: List,
        ref_anchor_maps: Dict,
        trace: str = "",
        key=None,
        root=False,
        deep=0,
    ):
        """collect move all links in cur_config to top

        only do in the top level of cur_config, collect all level links and return the links with level

        Args:
            cur_config:
                >>> {
                >>>     "_anchor": "anchor1",
                >>>     "arg1": {
                >>>         "arg11": 2,
                >>>         "arg12": "@anchor1.arg1.arg11 @lambda x: x+1"
                >>>     }
                >>> }
            ref_anchor_maps:
                global anchor path map and the relative anchor path map
            trace:
                the trace from root to current node
            key:
                the key of current node

        Returns:
            [
                {
                    "key": 'root.module.module.config.key',
                    "paras": ["root.module.module.config.key2"],
                    "lambda": "lambda x: x",
                },
                ...
            ]

        """
        if isinstance(cur_config, str):
            try:
                lambda_info = parser_lambda_key_value_pair(
                    trace, cur_config, ref_anchor_maps, root_config
                )
            except KeyNotFoundError as e:
                raise KeyNotFoundError(f"When parser {cur_config}, {e}")
            except Exception as e:
                raise ValueError(e)
            if lambda_info:
                refs.append(lambda_info)
            return refs
        elif isinstance(cur_config, list):
            for i, config_i in enumerate(cur_config):
                refs = cls.collect_refs(
                    cur_config=config_i,
                    root_config=root_config,
                    refs=refs,
                    ref_anchor_maps=copy.deepcopy(ref_anchor_maps),
                    trace=f"{trace}.{i}",
                    deep=deep,
                )
            return refs
        elif isinstance(cur_config, dict):
            if key and isinstance(key, str) and key.startswith("@"):
                anchor_addable = True
            else:
                anchor_addable = False or root
            if "_anchor" in cur_config:
                assert anchor_addable, f"{key} is not a module, but found .name in it."
                for d in range(deep, 0, -1):
                    if "$" * d in ref_anchor_maps:
                        ref_anchor_maps["$" * (d + 1)] = ref_anchor_maps["$" * d]
                if trace:
                    ref_anchor_maps["$"] = trace
                cur_config.pop("_anchor", {})
            for submodule_name, submodule_config in cur_config.items():
                if submodule_name == "_anchor":
                    continue
                assert isinstance(submodule_name, str)
                cur_trace = trace + "." + submodule_name if trace else submodule_name
                refs = cls.collect_refs(
                    cur_config=submodule_config,
                    root_config=root_config,
                    refs=refs,
                    ref_anchor_maps=copy.deepcopy(ref_anchor_maps),
                    trace=cur_trace,
                    key=submodule_name,
                    deep=deep + 1,
                )
            return refs
        else:
            return refs

    @classmethod
    def _collect_all_relative_refs(
        cls,
        cur_config: Dict,
        root_config: Dict,
        refs: List,
        ref_anchor_maps: Dict,
        trace: str = "",
        anchor_addable=True,
        deep: int = 0,
    ):
        """collect move all links in cur_config to top,
        NOTE: deprecated

        only do in the top level of cur_config, collect all level links and return the links with level

        Args:
            cur_config:
                >>> {
                >>>     "_anchor": "anchor1",
                >>>     "arg1": {
                >>>         "arg11": 2,
                >>>         "arg12": "@anchor1.arg1.arg11 @lambda x: x+1"
                >>>     }
                >>> }
            all_level_links:
                collected global all level links
            level:
                current level

        Returns:
            [
                {
                    "key": 'root.module.module.config.key',
                    "paras": ["root.module.module.config.key2"],
                    "lambda": "lambda x: x",
                },
                ...
            ]

        """
        if isinstance(cur_config, str):
            lambda_info = parser_lambda_key_value_pair(
                trace, cur_config, ref_anchor_maps, root_config
            )
            if lambda_info:
                refs.append(lambda_info)
            return refs
        elif isinstance(cur_config, list):
            for i, config_i in enumerate(cur_config):
                refs = cls._collect_all_relative_refs(
                    cur_config=config_i,
                    root_config=root_config,
                    refs=refs,
                    ref_anchor_maps=copy.deepcopy(ref_anchor_maps),
                    trace=f"{trace}.{i}",
                    anchor_addable=False,
                    deep=deep,
                )
            return refs
        elif isinstance(cur_config, dict):
            assert (
                anchor_addable or "_anchor" not in cur_config
            ), f"_anchor is not addable in {trace}"
            if anchor_addable and "_anchor" in cur_config:
                _anchor = cur_config["_anchor"]
                if _anchor != "$":
                    ref_anchor_maps[_anchor] = trace
                for d in range(deep):
                    if "$" * (d + 1) in ref_anchor_maps:
                        ref_anchor_maps["$" * (d + 2)] = ref_anchor_maps["$" * (d + 1)]
                ref_anchor_maps["$"] = trace
                cur_config.pop("_anchor", {})
            for submodule_name, submodule_config in cur_config.items():
                assert isinstance(submodule_name, str)
                submodule_name = (
                    trace + "." + submodule_name if trace else submodule_name
                )
                refs = cls._collect_all_relative_refs(
                    cur_config=submodule_config,
                    root_config=root_config,
                    refs=refs,
                    ref_anchor_maps=copy.deepcopy(ref_anchor_maps),
                    trace=submodule_name,
                    anchor_addable=anchor_addable,
                    deep=deep + 1,
                )
            return refs
        else:
            return refs

    def get_kind_module_base_config(
        self, abstract_config: Union[dict, str], module_type: str = ""
    ) -> List:
        """get the whole config of 'module_type' by given abstract_config

        Args:
            abstract_config: will expanded config
            module_type: the module kind, like 'embedding', 'subprocessor', which registered in config_parser_register

        Returns: parserd config (whole config) of abstract_config

        """
        if module_type in self.reserved:
            return [abstract_config]
        if module_type.startswith("@") or module_type == "_G" or self.root:
            module_type = module_type.lstrip("@")

            if isinstance(abstract_config, str):
                if abstract_config == MISSING:
                    return [MISSING]
                return Parser(
                    raw_config={"_base": abstract_config}, module_type=module_type
                ).parser(parser_ref=False)
            if isinstance(abstract_config, dict):
                return Parser(
                    raw_config=abstract_config, module_type=module_type
                ).parser(parser_ref=False)
            else:
                raise ValueError(
                    f"module {module_type} should be a dict, but got {abstract_config}"
                )
        else:
            return [abstract_config]

    @classmethod
    def flat_search(cls, search, config: dict, module_type) -> List[dict]:
        """flat all the para_search paras to list

        support recursive parser para_search now, this means you can add para_search/para_link/base paras in para_search paras
        but you should only search currently level paras

        Args:
            search: search paras, {"para1": [1,2,3], 'para2': 'list(range(10))'}
            config: base config

        Returns: list of possible config

        """
        result = []
        module_search_para = search
        if not module_search_para:
            result.append(config)
        else:
            search_para_list = cls.get_named_list_cartesian_prod(module_search_para)
            for search_para in search_para_list:
                base_config = copy.deepcopy(config)
                keys = list(search_para.keys())
                keys.sort()
                for key in keys:
                    current = base_config
                    for sub_key in split_trace(key)[:-1]:
                        current = base_config[sub_key]
                    current[split_trace(key)[-1]] = search_para[key]
                extend_config = cls(base_config, module_type).parser(parser_ref=False)
                result.extend(extend_config)
        return result

    def get_cartesian_prod(
        self, list_of_list_of_dict: List[List[Dict]]
    ) -> List[List[Dict]]:
        """get catesian prod from two lists

        Args:
            list_of_list_of_dict: [[config_a1, config_a2], [config_b1, config_b2]]

        Returns:
            [[config_a1, config_b1], [config_a1, config_b2], [config_a2, config_b1], [config_a2, config_b2]]

        """
        if len(list_of_list_of_dict) <= 1:
            return [copy.deepcopy(dic) for dic in list_of_list_of_dict]
        cur_result = list_of_list_of_dict[0]
        reserve_result = self.get_cartesian_prod(list_of_list_of_dict[1:])
        result = []
        for cur_config in cur_result:
            for reserve in reserve_result:
                result.append([copy.deepcopy(cur_config)] + copy.deepcopy(reserve))
        return result

    @staticmethod
    def check_config(configs: Union[Dict, List[Dict]]) -> None:
        """check all config is valid.

        check all $MISSING is replaced to correct value.
        Args:
            configs:
                will be checked config

        Returns:
            None

        Raises:
            ValueError

        """

        def _check(config):
            """check the $MISSING is in config or not"""
            for key in config:
                if isinstance(config[key], dict):
                    _check(config[key])
                if config[key] == MISSING:
                    raise ValueError(
                        f'In Config: \n {json.dumps(config, indent=4, ensure_ascii=False)}\n The must be provided key "{key}" marked with $MISSING is not provided.'
                    )

        if isinstance(configs, list):
            for config in configs:
                _check(config)
        else:
            _check(configs)

    @staticmethod
    def get_named_list_cartesian_prod(dict_of_list: Dict[str, List]) -> List[Dict]:
        """get catesian prod from named lists

        Args:
            dict_of_list: {'name1': [1,2,3], 'name2': [1,2,3,4]}

        Returns:
            [{'name1': 1, 'name2': 1}, {'name1': 1, 'name2': 2}, {'name1': 1, 'name2': 3}, ...]

        """
        if not dict_of_list:
            dict_of_list = {}
        if len(dict_of_list) == 0:
            return []
        dict_of_list = copy.deepcopy(dict_of_list)
        cur_name, cur_paras = dict_of_list.popitem()
        cur_para_search_list = []
        assert isinstance(
            cur_paras, list
        ), f"The search candidates must be list, but you provide {cur_paras}({type(cur_paras)})"
        for para in cur_paras:
            cur_para_search_list.append({cur_name: para})
        if len(dict_of_list) == 0:
            return cur_para_search_list
        reserve_para_list = Parser.get_named_list_cartesian_prod(dict_of_list)
        all_config_list = []
        for cur_config in cur_para_search_list:
            for reserve_config in reserve_para_list:
                _cur_config = copy.deepcopy(cur_config)
                _cur_config.update(copy.deepcopy(reserve_config))
                all_config_list.append(_cur_config)
        return all_config_list

    def is_rep_config(self, list_of_dict: List[dict]) -> bool:
        """check is there a repeat config in list

        Args:
            list_of_dict: a list of dict

        Returns:
            has repeat or not

        """
        # using json.dumps + sort_keys to guarantee the same dict to the same string represatation
        list_of_str = [
            json.dumps(dic, sort_keys=True, ensure_ascii=False) for dic in list_of_dict
        ]
        if len(list_of_dict) == len(set(list_of_str)):
            return False
        else:
            return True
