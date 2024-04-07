# Copyright the author(s) of intc.
#
# This source code is licensed under the Apache license found in the
# LICENSE file in the root directory of this source tree.

import os
import sys
from typing import Dict, List, Optional, Union

from tree_sitter import Language, Node, Parser

if sys.platform == "win32":
    sys_post_fix = "win"
elif sys.platform == "darwin":
    sys_post_fix = "mac"
else:
    sys_post_fix = "linux"


class JsonParser(object):
    """docstring for JsonParser"""

    def __init__(self):
        super(JsonParser, self).__init__()
        self._parser = Parser()
        dynamic_lib_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "lib",
            f"json_{sys_post_fix}_ts.so",
        )
        self._parser.set_language(Language(dynamic_lib_path, "json"))
        # self._parser.set_language(Language('../build/json_ts.so', 'json'))
        self.skip = {"comment", '"', "[", "]", "}", "{", ":"}

    def parser(self, doc: str) -> Optional[Union[Dict, List]]:
        """parser the json string to AST

        Args:
            doc: the source document

        Returns:
            the parser tree
        """
        return self.parser_object(self._parser.parse(bytes(doc, "utf8")).root_node)

    @staticmethod
    def print_parser_tree(node: Node, deep=0) -> None:
        for children in node.named_children:
            print(deep * "    " + children.type)
            JsonParser.print_parser_tree(children, deep + 1)

    def drop_quote(self, _text: bytes) -> str:
        text = _text.decode()
        if (
            len(text) >= 2
            and (text[0] == '"' and text[-1] == '"')
            or (text[0] == "'" and text[-1] == "'")
        ):
            return text[1:-1]
        return text

    def parser_pair(self, node: Node, deep: int) -> Dict:
        key = self.parser_object(node.named_children[0])

        if len(node.named_children) == 2:
            value = self.parser_object(node.named_children[1])
        else:
            value = None
        result = {}
        result["__type"] = "pair"
        result["__range"] = (node.start_point, node.end_point)
        result["__value"] = value
        result["__key"] = key
        return result

    def parser_string(self, node: Node, deep: int) -> Dict:
        return {
            "__type": "string",
            "__value": self.drop_quote(node.text),
            "__range": (node.start_point, node.end_point),
        }

    def parser_number(self, node: Node, deep: int) -> Dict:
        return {
            "__type": "number",
            "__value": eval(node.text.decode()),
            "__range": (node.start_point, node.end_point),
        }

    def parser_array(self, node: Node, deep: int) -> Dict:
        return {
            "__type": "array",
            "__value": [self.parser_object(child) for child in node.named_children],
            "__range": (node.start_point, node.end_point),
        }

    def parser_null_true_false(self, node: Node, deep: int):
        return {
            "__type": node.type,
            "__value": node.text.decode(),
            "__range": (node.start_point, node.end_point),
        }

    def parser_object(self, node, deep=0):
        if node.type in self.skip:
            return None
        if node.type == "pair":
            return self.parser_pair(node, deep + 1)
        if node.type == "string":
            return self.parser_string(node, deep + 1)

        if node.type == "number":
            return self.parser_number(node, deep + 1)

        if node.type == "array":
            return self.parser_array(node, deep + 1)

        if node.type in {"null", "bool"}:
            return self.parser_null_true_false(node, deep + 1)

        if node.type == "object":
            values = []
            for child in node.named_children:
                if child.type in self.skip:
                    continue
                value = self.parser_object(child)
                if value:
                    values.append(value)
            return values
        if node.type == "document":
            result = []
            for child in node.named_children:
                if child.type in self.skip:
                    continue
                result.append(
                    {
                        "__type": "document",
                        "__value": self.parser_object(child, deep + 1),
                        "__range": (child.start_point, child.end_point),
                    }
                )
            return result
        if node.type != "ERROR":
            result = []
            for child in node.named_children:
                if child.type in self.skip:
                    continue
                result.append(
                    {
                        "__type": "document",
                        "__value": self.parser_object(child, deep + 1),
                        "__range": (child.start_point, child.end_point),
                    }
                )
            return result
        return {
            "__type": "error",
            "__range": (node.start_point, node.end_point),
            "__meta": {"type": node.type, "text": node.text.decode()},
        }


if __name__ == "__main__":
    parser = JsonParser()
    print(
        parser.parser(
            """
{
    "_global_":{
        "insert_0": "insert_0",
    },
    "@module_for_test_parser@config_a": {
        "_name_": "config_b",
        "_anchor_": "config_a",
        "@child_module_for_test_parser@child_new": {
            "_name_": "child_module_for_test_parser@child_a",
            "i_am_float_child": 0.0,
            "i_am_child": "new child value"
        },
        "@child_module_for_test_parser@child_b#2": {
            "_name_": "child_module_for_test_parser@child_a",
            "i_am_float_child": 0.0,
            "i_am_child": "child value2"
        }
    }
}
                        """
        )
    )
