# Copyright the author(s) of intc.
#
# This source code is licensed under the Apache license found in the
# LICENSE file in the root directory of this source tree.

import logging

logger = logging.getLogger("intc_lsp")


def position_is_in_range(position_range: tuple, position: tuple) -> bool:
    """Check if a given position is within a specified range.

    Args:
        position_range: A tuple representing the start and end positions of a range.
        position: A tuple representing the position (row, col)

    Returns:
        bool: True if the position is within the range, False otherwise.
    """
    range_start = position_range[0][0] * 1e8 + position_range[0][1]
    range_end = position_range[1][0] * 1e8 + position_range[1][1]
    position = position[0] * 1e8 + position[1]
    return position >= range_start and position < range_end


def root_trace(result, position, trace="") -> tuple:
    """Trace the root of a tree structure based on a given position.

    Args:
        result: The result of the tracing process.
        position: The position to trace.

    Returns:
        tuple: A tuple containing the semantic trace, lexical trace, trace value, a flag indicating if the position matches the key or value, anchor dictionary, and additional information.
    """
    anchor_dict = {}
    additional = {}
    if not result:
        return None, None, None, None, anchor_dict, additional
    for node in result:
        semantic_trace, lex_trace, trace_result, is_key_or_none = node_trace(
            node, position, anchor_dict, additional, trace
        )
        if is_key_or_none is not None:
            return (
                semantic_trace,
                lex_trace,
                trace_result,
                is_key_or_none,
                anchor_dict,
                additional,
            )
    return None, None, None, None, anchor_dict, additional


def node_trace_document(
    node, position, anchor_dict: dict, additional: dict, trace: str = ""
):
    """Trace a document node in a tree structure based on a given position.

    Args:
        node: The document node to trace.
        position: The position to trace.
        anchor_dict: A dictionary to store anchor names and their corresponding traces.
        additional: Additional information to be passed along during the tracing process.
        trace: The current trace string. Defaults to an empty string.

    Returns:
        tuple: A tuple containing the semantic trace, lexical trace, trace value, and a flag indicating if the position matches the key or value.
    """
    if not position_is_in_range(node["__range"], position):
        return None, None, None, None
    if trace:
        node["__type"] = "pair"
        node["__key"] = {
            "__type": "string",
            "__value": f"@{trace.lstrip('@')}",
            "__range": ((-1, -1), (-1, -1)),
        }
        return node_trace_pair(node, position, anchor_dict, additional, trace)
    for value in node["__value"]:
        value_result = node_trace(value, position, anchor_dict, additional, trace)
        if value_result[3] is not None:
            return value_result
    return None, None, None, None


def node_trace(
    node, position, anchor_dict: dict, additional: dict, trace: str = ""
) -> tuple:
    """Trace a node in a tree structure based on a given position.

    Args:
        node: The node to trace.
        position: The position to trace.
        anchor_dict: A dictionary to store anchor names and their corresponding traces.
        additional: Additional information to be passed along during the tracing process.
        trace: The current trace string. Defaults to an empty string.

    Returns:
        tuple: A tuple containing the semantic trace, lexical trace, trace value, and a flag indicating if the position matches the key or value.
    """
    if node.get("__type", None) == "pair":
        return node_trace_pair(node, position, anchor_dict, additional, trace)
    elif node.get("__type", None) == "document":
        return node_trace_document(node, position, anchor_dict, additional, trace)
    elif node.get("__type", None) == "array":
        return node_trace_array(node, position, anchor_dict, additional, trace)
    else:
        return node_trace_other(node, position, anchor_dict, additional, trace)


def node_trace_other(
    node, position, anchor_dict: dict, additional: dict, trace: str = ""
) -> tuple:
    """Trace a node of type other in a tree structure based on a given position.

    Args:
        node: The node to trace.
        position: The position to trace.
        anchor_dict: A dictionary to store anchor names and their corresponding traces.
        additional: Additional information to be passed along during the tracing process.
        trace: The current trace string. Defaults to an empty string.

    Returns:
        tuple: A tuple containing the semantic trace, lexical trace, trace value, and a flag indicating if the position matches the key or value.
    """
    if not position_is_in_range(node["__range"], position):
        return None, None, None, None
    return "", "", node.get("__value", None), False


def node_trace_array(
    node, position, anchor_dict: dict, additional: dict, trace: str = ""
):
    """Trace an array node in a tree structure based on a given position.

    Args:
        node: The array node to trace.
        position: The position to trace.
        anchor_dict: A dictionary to store anchor names and their corresponding traces.
        additional: Additional information to be passed along during the tracing process.
        trace: The current trace string. Defaults to an empty string.

    Returns:
        tuple: A tuple containing the semantic trace, lexical trace, trace value, and a flag indicating if the position matches the key or value.
    """
    if not position_is_in_range(node["__range"], position):
        return None, None, None, None
    for i, child in enumerate(node["__value"]):
        if not position_is_in_range(child["__range"], position):
            continue
        semantic_trace, lex_trace, trace_value, is_key_or_none = node_trace(
            child, position, anchor_dict, additional, trace + f".{i}"
        )
        if semantic_trace:
            return (
                f"{i}.{semantic_trace}",
                f"{i}.{lex_trace}",
                trace_value,
                is_key_or_none,
            )
    return None, None, None, None


def node_trace_pair(
    node, position, anchor_dict: dict, additional: dict, trace: str = ""
):
    """Trace a pair node in a tree structure based on a given position.

    Args:
        node: The pair node to trace.
        position: The position to trace.
        anchor_dict: A dictionary to store anchor names and their corresponding traces.
        additional: Additional information to be passed along during the tracing process.
        trace: The current trace string. Defaults to an empty string.

    Returns:
        tuple: A tuple containing the semantic trace, lexical trace, trace value, and a flag indicating if the position matches the key or value.
    """
    trace_value = None
    is_key_or_none = (
        None  # True or False means matching the key or value, None means not match
    )
    on_module_root = False
    semantic_trace = ""
    lex_trace = ""
    if not position_is_in_range(node["__range"], position):
        return None, None, None, None
    module_name = node["__key"]["__value"]
    semantic_module_name = module_name
    is_module = False
    if node.get("__key", {}).get("__value", "").startswith("@"):
        is_module = True

    if position_is_in_range(node["__key"]["__range"], position):
        if not is_module:
            return "", "", node.get("__key", {}).get("__value", ""), True
        else:
            on_module_root = True
            additional["on_semantic_module_name"] = module_name
            additional["on_module_name"] = module_name
            if (not isinstance(node.get("__value", None), list)) or (
                not node.get("__value", None)
            ):
                return "", "", node.get("__key", {}).get("__value", ""), True

    sub_modules = node.get("__value", [])
    if isinstance(sub_modules, dict):
        semantic_trace, lex_trace, trace_value, is_key_or_none = node_trace(
            sub_modules, position, anchor_dict, additional, trace + "." + module_name
        )
        if not on_module_root:
            if is_key_or_none is not None:
                return (
                    semantic_module_name
                    if not semantic_trace
                    else f"{semantic_module_name}.{semantic_trace}",
                    module_name if not lex_trace else f"{module_name}.{lex_trace}",
                    trace_value,
                    False,
                )
            return None, None, None, None
    assert isinstance(sub_modules, list), sub_modules
    for sub_module in sub_modules:
        if (
            is_module
            and sub_module.get("__type", None) == "pair"
            and (sub_module.get("__key", {}).get("__value", "") in {"_name", "_base"})
        ):
            base_name = sub_module.get("__value", {}).get("__value", "")
            if base_name and isinstance(base_name, str):
                semantic_module_name = f"{module_name.lstrip('@')}@{base_name}"
                if semantic_module_name:
                    semantic_module_name = f"@{semantic_module_name}"
                if on_module_root:
                    additional["on_semantic_module_name"] = semantic_module_name
                    additional["on_module_name"] = module_name

        elif (
            is_module
            and sub_module.get("__type", None) == "pair"
            and sub_module.get("__key", {}).get("__value", "") == "_anchor"
        ):
            anchor_name = sub_module.get("__value", {}).get("__value", "")
            if anchor_name and isinstance(anchor_name, str):
                anchor_dict[anchor_name] = (
                    trace + "." + module_name if trace else module_name
                )
        if position_is_in_range(sub_module["__range"], position):
            semantic_trace, lex_trace, trace_value, is_key_or_none = node_trace(
                sub_module, position, anchor_dict, additional, trace + "." + module_name
            )
    if not on_module_root:
        if is_key_or_none is not None:
            semantic_trace = (
                f"{semantic_module_name}.{semantic_trace}"
                if semantic_trace
                else semantic_module_name
            )
            lex_trace = f"{module_name}.{lex_trace}" if lex_trace else module_name
            return semantic_trace, lex_trace, trace_value, is_key_or_none
    else:
        return "", "", node.get("__key", {}).get("__value", ""), True
    return None, None, None, None


if __name__ == "__main__":
    result = [
        {
            "__type": "pair",
            "__value": [
                {
                    "__type": "pair",
                    "__range": ((1, 4), (1, 24)),
                    "__value": {
                        "__type": "string",
                        "__value": "config_a",
                        "__range": ((1, 14), (1, 24)),
                    },
                    "__key": {
                        "__type": "string",
                        "__value": "_base",
                        "__range": ((1, 4), (1, 12)),
                    },
                },
                {
                    "__type": "pair",
                    "__range": ((2, 4), (10, 5)),
                    "__value": [
                        {
                            "__type": "pair",
                            "__range": ((3, 8), (3, 27)),
                            "__value": {
                                "__type": "string",
                                "__value": "child_a",
                                "__range": ((3, 18), (3, 27)),
                            },
                            "__key": {
                                "__type": "string",
                                "__value": "_base",
                                "__range": ((3, 8), (3, 16)),
                            },
                        },
                        {
                            "__type": "pair",
                            "__range": ((4, 8), (4, 31)),
                            "__value": {
                                "__type": "number",
                                "__value": 0.0,
                                "__range": ((4, 28), (4, 31)),
                            },
                            "__key": {
                                "__type": "string",
                                "__value": "i_am_float_child",
                                "__range": ((4, 8), (4, 26)),
                            },
                        },
                        {
                            "__type": "pair",
                            "__range": ((5, 8), (5, 45)),
                            "__value": {
                                "__type": "string",
                                "__value": "new child value",
                                "__range": ((5, 28), (5, 45)),
                            },
                            "__key": {
                                "__type": "string",
                                "__value": "i_am_float_child",
                                "__range": ((5, 8), (5, 26)),
                            },
                        },
                        {
                            "__type": "pair",
                            "__range": ((6, 8), (9, 9)),
                            "__value": [
                                {
                                    "__type": "pair",
                                    "__range": ((7, 12), (7, 31)),
                                    "__value": {
                                        "__type": "string",
                                        "__value": "child_a",
                                        "__range": ((7, 22), (7, 31)),
                                    },
                                    "__key": {
                                        "__type": "string",
                                        "__value": "_base",
                                        "__range": ((7, 12), (7, 20)),
                                    },
                                },
                                {
                                    "__type": "pair",
                                    "__range": ((8, 12), (8, 22)),
                                    "__value": {
                                        "__type": "number",
                                        "__value": 1,
                                        "__range": ((8, 21), (8, 22)),
                                    },
                                    "__key": {
                                        "__type": "string",
                                        "__value": "hello",
                                        "__range": ((8, 12), (8, 19)),
                                    },
                                },
                            ],
                            "__key": {
                                "__type": "string",
                                "__value": "@child_module_for_test_parser",
                                "__range": ((6, 8), (6, 39)),
                            },
                        },
                    ],
                    "__key": {
                        "__type": "string",
                        "__value": "@child_module_for_test_parser",
                        "__range": ((2, 4), (2, 35)),
                    },
                },
                {
                    "__type": "pair",
                    "__range": ((12, 4), (16, 5)),
                    "__value": [
                        {
                            "__type": "error",
                            "__range": ((13, 8), (15, 21)),
                            "__meta": {
                                "type": "ERROR",
                                "text": '"_base": "child_a",\n        "i_am_float_child": \n        "i_am_child":',
                            },
                        },
                        {
                            "__type": "pair",
                            "__range": ((15, 22), (15, 36)),
                            "__value": None,
                            "__key": {
                                "__type": "string",
                                "__value": "child value2",
                                "__range": ((15, 22), (15, 36)),
                            },
                        },
                    ],
                    "__key": {
                        "__type": "string",
                        "__value": "@child_module_for_test_parser#2",
                        "__range": ((12, 4), (12, 37)),
                    },
                },
                {
                    "__type": "pair",
                    "__range": ((17, 4), (19, 5)),
                    "__value": [
                        {
                            "__type": "pair",
                            "__range": ((18, 8), (18, 36)),
                            "__value": {
                                "__type": "string",
                                "__value": "nest_new_value",
                                "__range": ((18, 20), (18, 36)),
                            },
                            "__key": {
                                "__type": "string",
                                "__value": "nest_key",
                                "__range": ((18, 8), (18, 18)),
                            },
                        }
                    ],
                    "__key": {
                        "__type": "string",
                        "__value": "nested",
                        "__range": ((17, 4), (17, 12)),
                    },
                },
            ],
            "__range": ((0, 0), (20, 1)),
            "__key": {
                "__type": "string",
                "__value": "@module_for_test_parser",
                "__range": ((-1, -1), (-1, -1)),
            },
        }
    ]
    print(root_trace(result, (14, 28)))
