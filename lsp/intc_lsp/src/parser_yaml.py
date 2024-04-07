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


class YamlParser(object):
    """docstring for ParserYAML"""

    def __init__(self):
        super(YamlParser, self).__init__()
        self._parser = Parser()
        dynamic_lib_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "lib",
            f"yaml_{sys_post_fix}_ts.so",
        )
        self._parser.set_language(Language(dynamic_lib_path, "yaml"))
        self.skip = {"comment"}

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
            YamlParser.print_parser_tree(children, deep + 1)

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
        key = self.parser_object(node.named_children[0], deep + 1)
        if len(node.named_children) == 2:
            value = self.parser_object(node.named_children[1], deep + 1)
        else:
            assert len(node.named_children) == 1
            value = None
        result = {}
        result["__type"] = "pair"
        result["__range"] = (node.start_point, node.end_point)
        result["__value"] = value
        result["__key"] = key
        return result

    def parser_flow_node(self, node: Node, deep: int):
        assert len(node.named_children) == 1, node.named_children
        return self.parser_object(node.named_children[0], deep + 1)

    def parser_plain_scalar(self, node: Node, deep: int):
        assert len(node.named_children) == 1, node.named_children
        return self.parser_object(node.named_children[0], deep + 1)

    def parser_string(self, node: Node, deep: int) -> Dict:
        assert len(node.named_children) == 0, node.named_children
        return {
            "__type": "string",
            "__value": self.drop_quote(node.text),
            "__range": (node.start_point, node.end_point),
        }

    def parser_number(self, node: Node, deep: int) -> Dict:
        assert len(node.named_children) == 0, node.named_children
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

    def parser_block_node(self, node: Node, deep: int):
        assert len(node.named_children) == 1, node.named_children
        return self.parser_object(node.named_children[0], deep + 1)

    def parser_null_true_false(self, node: Node, deep: int):
        type_map = {
            "null_scalar": "null",
            "boolean_scalar": "bool",
        }
        return {
            "__type": type_map[node.type],
            "__value": "null_or_bool",
            "__range": (node.start_point, node.end_point),
        }

    def parser_object(self, node: Node, deep: int = 0):
        if deep == 0 and node.type == "ERROR":
            parser_childs = [
                self.parser_object(child)
                for child in node.named_children
                if child.type not in self.skip
            ]
            return parser_childs
        if node.type in self.skip:
            return None
        if node.type == "block_mapping_pair":
            return self.parser_pair(node, deep + 1)

        if node.type == "flow_sequence":
            return self.parser_array(node, deep + 1)
        if node.type == "plain_scalar":
            return self.parser_plain_scalar(node, deep + 1)
        if node.type == "flow_node":
            return self.parser_flow_node(node, deep + 1)
        if node.type in {"string_scalar", "double_quote_scalar", "single_quote_scalar"}:
            return self.parser_string(node, deep + 1)

        if node.type in {"integer_scalar", "float_scalar"}:
            return self.parser_number(node, deep + 1)

        if node.type in {"boolean_scalar", "null_scalar"}:
            return self.parser_null_true_false(node, deep + 1)

        if node.type == "stream":
            for child in node.named_children:
                result = self.parser_object(child, deep + 1)
                if result is not None:
                    return result
            return {}

        if node.type == "block_node":
            return self.parser_block_node(node, deep + 1)
        if node.type == "block_mapping":
            values = []
            for child in node.named_children:
                if child.type in self.skip:
                    continue
                value = self.parser_object(child, deep + 1)
                if value:
                    values.append(value)
            return values

        if node.type == "block_sequence":
            return {
                "__type": "array",
                "__value": [
                    self.parser_object(child, deep) for child in node.named_children
                ],
                "__range": (node.start_point, node.end_point),
            }
        if node.type == "block_sequence_item":
            return self.parser_object(node.named_children[0], deep + 1)

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
        return {}


if __name__ == "__main__":
    parser = YamlParser()
    print(
        parser.parser(
            """
    # type=dlk

    "@config":
        "_name_": basic
        "@optimizer@adam": 1
        name:
            - a
            - b
    """
        )
    )
