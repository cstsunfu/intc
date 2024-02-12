# Copyright the author(s) of intc.
#
# This source code is licensed under the Apache license found in the
# LICENSE file in the root directory of this source tree.

import json
import logging
import pathlib
import re
import urllib
from enum import Enum
from functools import lru_cache
from textwrap import dedent
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union
from urllib.parse import unquote

from attrs import define, field, fields
from lsprotocol.types import (
    CompletionItem,
    CompletionItemKind,
    CompletionItemLabelDetails,
    CompletionList,
    Diagnostic,
    DiagnosticSeverity,
    Hover,
    Location,
    MarkupContent,
    MarkupKind,
    Position,
    Range,
)
from pygls.server import LanguageServer

logger = logging.getLogger("intc_lsp")
try:
    from intc_lsp.src.parser_json import JsonParser
    from intc_lsp.src.parser_yaml import YamlParser
    from intc_lsp.src.trace import root_trace
except Exception as e:
    logger.error(f"import parser error : {e}")

try:
    from intc.register import ic_help, ic_repo, type_module_map
    from intc.utils import split_trace
except Exception as e:
    logger.error(f"import ic_repo error : {e}")


@lru_cache(maxsize=128)
def value2str(value):
    """convert the value to str

    Args:
        value: any type of value
    Returns:
        str value
    """
    if isinstance(value, str):
        return value
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, (list, tuple, dict)):
        return json.dumps(value)
    if value is None:
        return "null"
    try:
        return str(value)
    except:
        return ""


@lru_cache(maxsize=128)
def get_module_type_by_uri(server, uri: str):
    """get the module type by the uri
    Args:
        server: IntcLanguageServer
        uri: the file uri

    Returns:
        module type
        is_entry: True or False, means the uri is a entry module file
    """
    uri = unquote(uri)
    uri_parser_result = urllib.parse.urlparse(uri)
    assert uri_parser_result.scheme == "file"
    uri = uri_parser_result.path
    file_name = pathlib.Path(uri).name
    if server.entry_pattern and server.entry_pattern.match(uri):
        # NOTE: for entry, there is no module_type info from the filename
        return "", True
    elif server.modules_pattern and server.modules_pattern.match(uri):
        module_type = file_name.split(".")[0].split("#")[0].split("@")[0]
        return module_type, False
    return "", False


@define
class ParseResult:
    semantic_trace: str = field(
        default="", metadata={"help": "The semantic trace path, resolve the .name"}
    )
    lex_trace: str = field(default="", metadata={"help": "The cursor node path"})
    trace_result: str = field(default="", metadata={"help": "The cursor node value"})
    is_entry: bool = field(
        default=False,
        metadata={"help": "True means the file is a entry module, False means not"},
    )
    is_key_or_none: Optional[bool] = field(
        default=None,
        metadata={
            "help": "True or False means matching the key or value, None means not match"
        },
    )
    parser_tree: Optional[Dict] = field(
        default=None, metadata={"help": "The parser tree"}
    )
    anchor_dict: Optional[Dict] = field(
        default=None,
        metadata={
            "help": "The anchors dict in the path to the cursor, key is anchor name, value is the trace path"
        },
    )
    additional: Optional[Dict] = field(
        default=None,
        metadata={
            "help": "Additional info, when the cursor is on module root, return the base module name"
        },
    )


class HelpStatus(Enum):
    SUCCESS = "SUCCESS"
    NO_MODULE_NAME = "NO_MODULE_NAME"
    NO_MODULE_HELP = "NO_MODULE_HELP"
    NO_MODULE_TYPE_NAME = "NO_MODULE_TYPE_NAME"
    UN_RECOGNIZED = "UN_RECOGNIZED"


class HoverType(Enum):
    SUCCESS = 0
    VALUE_NOT_IN_OPTION = 1
    MODULE_NOT_FOUND = 2
    CURSOR_WORD_NOT_FOUND = 3
    RESOLVE_ERROR = 4
    UN_COVER_ERROR = 5
    HELP_INFO_NOT_FOUND = 6
    DEPRECATED = 7


def find_module_root(parser_result: ParseResult):
    """find the module name, and the relative trace path

    Args:
        parser_result:
            current cursor node information

    Returns:
        module_name, traces
    """

    def find_module_root_by_parent(
        semantic_traces: List[str], lex_traces: List[str], trace: str
    ):
        """find the real module name based on the parent modules

        Args:
            semantic_traces: the whole semantic trace paths
            lex_traces: the whole lex trace paths
            trace: final trace

        Returns:
            model_name like @module_type@module_name
        """
        par_traces = [trace]
        for semantic_trace, lex_trace in zip(semantic_traces[::-1], lex_traces[::-1]):
            logger.info(
                f"find_module_root_by_parent: semantic_trace : {semantic_trace}, lex_trace : {lex_trace}"
            )
            if (
                semantic_trace.startswith("@")
                and len(semantic_trace.lstrip("@").split("@")) >= 2
            ):
                type_names = semantic_trace.lstrip("@").split("@")
                module_type = type_names[0].split("#")[0]
                module_name = type_names[-1].split("#")[0]
                try:
                    par_module = ic_repo[(module_type, module_name)]
                    for par_trace in par_traces:
                        par_module = par_module[par_trace]
                    base_module_name = par_module.get("_base", "") or par_module.get(
                        "_name", ""
                    )
                    if base_module_name:
                        type_names = trace.lstrip("@").split("@")
                        module_type = type_names[0].split("#")[0]
                        base_module_name = type_names[-1].split("#")[0]
                        return f"@{module_type}@{base_module_name}"
                except Exception as e:
                    logger.info(
                        f"find_module_root_by_parent: can not find the module {module_type}@{module_name}, {e}"
                    )
                    return ""
            if lex_trace.startswith("@"):
                lex_trace = f'@{lex_trace.lstrip("@")}'
            par_traces.insert(0, lex_trace)
        return ""

    try:
        if parser_result.semantic_trace is None:
            return "", []
        semantic_traces = split_trace(parser_result.semantic_trace)
        lex_traces = split_trace(parser_result.lex_trace)
        if len(semantic_traces) != len(lex_traces):
            logger.error(
                f"the length of semantic_traces and lex_traces is not equal, '{parser_result.semantic_trace}', '{parser_result.lex_trace}'"
            )
            lex_traces = semantic_traces
        if (
            parser_result.is_key_or_none == True
            and parser_result.trace_result is not None
        ):
            semantic_traces.append(parser_result.trace_result)
            lex_traces.append(parser_result.trace_result)
        logger.info(f"find_module_root: semantic_traces : {semantic_traces}")
        logger.info(f"find_module_root: lex_traces : {lex_traces}")
        if (
            parser_result.additional
            and "on_semantic_module_name" in parser_result.additional
        ):
            on_semantic_module_name = parser_result.additional[
                "on_semantic_module_name"
            ]
            if (
                on_semantic_module_name.startswith("@")
                and len(on_semantic_module_name.lstrip("@").split("@")) >= 2
            ):
                return parser_result.additional["on_semantic_module_name"], []
        traces = []
        logger.info(f"find_module_root: semantic_traces : {semantic_traces}")
        for i, (trace, lex_trace) in enumerate(
            zip(semantic_traces[::-1], lex_traces[::-1])
        ):
            if trace.startswith("@"):
                if len(trace.lstrip("@").split("@")) >= 2:
                    type_names = trace.lstrip("@").split("@")
                    module_type = type_names[0].split("#")[0]
                    module_name = type_names[-1].split("#")[0]
                    return f"@{module_type}@{module_name}", traces
                else:
                    module_name = find_module_root_by_parent(
                        semantic_traces[::-1][i + 1 :], lex_traces[::-1][i + 1 :], trace
                    )
                    logger.info(
                        f"find_module_root: by parent module_name : {module_name}, traces : {traces}"
                    )
                    if module_name:
                        return module_name, traces
                    else:
                        return trace, traces
            else:
                traces.insert(0, trace)
        return "", []
    except Exception as e:
        logger.error(f"get_key_help: error : {e}")
        return "", []


class IntcResolve(object):
    """docstring for IntcResolve"""

    def __init__(self, server):
        super(IntcResolve, self).__init__()
        self.server: LanguageServer = server
        self.json_parser: JsonParser = None
        self.yaml_parser: YamlParser = None
        self.reserved_words = {"_base", "_name", "_anchor", "_search", "_G"}

        try:
            self.json_parser = JsonParser()
            logger.info(f"init : json parser")
        except Exception as e:
            logger.error(f"init : json parser error : {e}")
        try:
            self.yaml_parser = YamlParser()
            logger.info(f"init : yaml parser")
        except Exception as e:
            logger.error(f"init : yaml parser error : {e}")

    def cursor_word(
        self, uri: str, source: str, position: Position, include_all: bool = True
    ) -> Optional[Tuple[str, Range]]:
        if source is None:
            source = self.server.workspace.get_document(uri).source

        def _cursor_line() -> str:
            line = source.split("\n")[position.line]
            return str(line)

        line = _cursor_line()

        cursor = position.character
        for m in re.finditer(r"\w+", line):
            end = m.end() if include_all else cursor
            if m.start() <= cursor <= m.end():
                word = (
                    line[m.start() : end],
                    Range(
                        start=Position(line=position.line, character=m.start()),
                        end=Position(line=position.line, character=end),
                    ),
                )
                return word
        return None

    def get_module_help(self, module_name: str):
        """get the module help from ic_help

        Args:
            module_name: @module_type@module_name

        Returns:
            help information of the module
        """
        logger.info(f"get_module_help: module_name: {module_name}")
        type_names = module_name.lstrip("@").split("@")
        if len(type_names) < 1:
            logger.error(
                f"get_module_help: unrecognized module_name error : {module_name}"
            )
            return {}, HelpStatus.UN_RECOGNIZED
        elif len(type_names) == 1:
            module_type = type_names[0].split("#")[0]
            name = ""
        else:
            module_type = type_names[0].split("#")[0]
            name = type_names[-1].split("#")[0]
        try:
            return ic_help[(module_type, name)], HelpStatus.SUCCESS
        except Exception as e:
            logger.error(f"get_module_help error: {e}")
            if not module_type and not name:
                return {}, HelpStatus.NO_MODULE_TYPE_NAME
            elif len(type_names) == 1 or not name:
                return {}, HelpStatus.NO_MODULE_NAME
            else:
                return {}, HelpStatus.NO_MODULE_HELP

    def completions(
        self, position: Position, uri: str, trigger_char: str
    ) -> CompletionList:
        """get the completions items for the given position and uri

        Args:
            position: cursor position
            uri: the file uri
            trigger_char: the trigger character

        Returns:
            completions items
        """
        items = []
        source = self.server.workspace.get_document(uri).source

        def _update_source(source):
            lines = source.split("\n")
            line = lines[position.line]
            if not line.strip():
                line = " " * position.character + '" "'
            elif line.strip().endswith(":"):
                rline = line.rstrip()
                lrline = len(rline)
                if position.character > lrline:
                    line = (
                        rline
                        + " " * max((position.character - len(rline) - 1), 0)
                        + '" ",'
                    )
            return "\n".join(
                lines[: position.line] + [line] + lines[position.line + 1 :]
            )

        try:
            source = _update_source(source)
        except Exception as e:
            logger.error(f"completions: update source error : {e}")
            return CompletionList(is_incomplete=False, items=[])
        logger.info(f"completions: source : {source}")
        parser_tree = self.parser_tree(uri, source)

        module_type, is_entry = get_module_type_by_uri(self.server, uri)
        logger.info(f"uri: {uri}. module_type: {module_type}")
        parser_result = self.parser_cursor(
            parser_tree, position, module_type, source, is_entry
        )

        logger.info(f"completions parser_result : {parser_result}")

        # 1. can not resolve the semantic trace
        if parser_result.semantic_trace is None:
            return CompletionList(is_incomplete=False, items=[])
        module_name, traces = find_module_root(parser_result)

        module_help_meta, get_help_status = self.get_module_help(module_name)
        logger.info(
            f"completion: module_help_meta : {module_help_meta}, get_help_status : {get_help_status}, traces : {traces}"
        )
        # 2. can not resolve the module name
        if get_help_status == HelpStatus.NO_MODULE_NAME:
            # 2.2. only module type, no module name, completion on key, complete "_base"
            if parser_result.is_key_or_none == True and not parser_result.trace_result:
                items.append(
                    CompletionItem(
                        label=f"_base",
                        kind=CompletionItemKind.Module,
                        label_details=CompletionItemLabelDetails(
                            description="BaseField"
                        ),
                        documentation=MarkupContent(
                            kind=MarkupKind.Markdown,
                            value=f"BaseField\n\nThe initial module, you can set the base module name as a `str` in its value.",
                        ),
                    )
                )
                return CompletionList(is_incomplete=True, items=items)
            # 2.3. only module type, no module name, completion on value, complete the inherited module name
            elif (parser_result.is_key_or_none == False and traces == ["_base"]) or (
                parser_result.is_key_or_none == True
                and parser_result.trace_result.startswith("@")
                and trigger_char == "@"
            ):
                logger.info(f"completion: the module name is {module_name}")
                module_type = module_name.lstrip("@").split("#")[0].split("@")[0]
                for name in type_module_map[module_type]:
                    module_help = ic_help[(module_type, name)]
                    items.append(
                        CompletionItem(
                            label=name,
                            kind=CompletionItemKind.Module,
                            label_details=CompletionItemLabelDetails(
                                description="ModuleField"
                            ),
                            documentation=MarkupContent(
                                kind=MarkupKind.Markdown,
                                value=module_help.get("_meta", {}).get("help", ""),
                            ),
                        )
                    )
                return CompletionList(is_incomplete=True, items=items)
            # 2.4. trigger by "@" completion on the module type
            elif (
                parser_result.is_key_or_none == True
                and parser_result.trace_result == "@"
            ):
                for module_type in type_module_map:
                    items.append(
                        CompletionItem(
                            label=module_type,
                            label_details=CompletionItemLabelDetails(
                                description="ModuleField"
                            ),
                            kind=CompletionItemKind.Module,
                            documentation=MarkupContent(
                                kind=MarkupKind.Markdown,
                                value=f"ChildModule\n\nThe configure of `{module_type}` module",
                            ),
                        )
                    )
                return CompletionList(is_incomplete=False, items=items)
        # 3. success resolve
        elif get_help_status == HelpStatus.SUCCESS:
            # 3.1. completion on key, complete the module para names
            if parser_result.is_key_or_none == True:
                if not module_help_meta:
                    return CompletionList(is_incomplete=False, items=[])
                for trace in traces:
                    if trace:
                        module_help_meta = module_help_meta.get("properties", {}).get(
                            trace, {}
                        )
                    if not module_help_meta:
                        return CompletionList(is_incomplete=False, items=[])
                properties = module_help_meta.get("properties", {})
                for key in properties:
                    if key in {"_G"} and not parser_result.is_entry:
                        continue
                    help = ""
                    kind = CompletionItemKind.Field
                    if key.startswith("@"):
                        help = "The `Children` module"
                        kind = CompletionItemKind.Class
                        type_name = "SubModule"
                    else:
                        if key in self.reserved_words:
                            kind = CompletionItemKind.Property
                        meta = properties[key]
                        type_name = meta.get("type_name", "")
                        is_deprecated = meta.get("deprecated", False)
                        prefix = ""
                        if is_deprecated == True:
                            prefix = "`Deprecated`\n"
                        elif is_deprecated and isinstance(is_deprecated, str):
                            prefix = f"`Deprecated` {is_deprecated}\n"

                        if type_name:
                            _key = key.replace("_", r"\_")
                            type_str = f"""{_key} -> `{type_name}`\n\n"""
                        else:
                            type_str = ""
                        if key in self.reserved_words:
                            help = f"""{prefix}{type_str}\n{dedent(meta.get("description", ""))}"""
                        else:
                            help = f"""{prefix}{type_str}\n{dedent(meta.get("description", ""))}"""

                    items.append(
                        CompletionItem(
                            label=key,
                            label_details=CompletionItemLabelDetails(
                                description=type_name
                            ),
                            kind=kind,
                            documentation=MarkupContent(
                                kind=MarkupKind.Markdown, value=help
                            ),
                        )
                    )
                return CompletionList(is_incomplete=True, items=items)
            # 3.2. completion the basic module name
            elif parser_result.is_key_or_none == False and traces == ["_base"]:
                module_type = module_name.lstrip("@").split("#")[0].split("@")[0]
                for name in type_module_map[module_type]:
                    module_help_meta = ic_help[(module_type, name)]
                    help = dedent(module_help_meta.get("description", ""))
                    if help:
                        help = f"{module_type}@{name} -> `ModuleField`\r\n{help}"
                    else:
                        help = "ModuleField"
                    items.append(
                        CompletionItem(
                            label=name,
                            kind=CompletionItemKind.Module,
                            label_details=CompletionItemLabelDetails(
                                description="ModuleField"
                            ),
                            documentation=MarkupContent(
                                kind=MarkupKind.Markdown, value=help
                            ),
                        )
                    )
                return CompletionList(is_incomplete=True, items=items)
            # 3.3 completion on value, complete the value suggestions
            elif parser_result.is_key_or_none == False:
                logger.info(f"completion: completion on value, traces : {traces}")
                if not module_help_meta:
                    return CompletionList(is_incomplete=False, items=[])
                for trace in traces:
                    if trace:
                        module_help_meta = module_help_meta.get("properties", {}).get(
                            trace, {}
                        )
                    if not module_help_meta:
                        return CompletionList(is_incomplete=False, items=[])
                meta = module_help_meta
                if not meta:
                    return CompletionList(is_incomplete=False, items=[])
                logger.info(f"completion: completion on value, meta : {meta}")
                default = meta.get("default", "")
                suggestions = meta.get("suggestions", [])
                if default != "":
                    items.append(
                        CompletionItem(
                            label=value2str(default),
                            label_details=CompletionItemLabelDetails(
                                description=meta.get("type", "value")
                            ),
                            kind=CompletionItemKind.Value,
                            documentation=MarkupContent(
                                kind=MarkupKind.Markdown, value=f"Default value"
                            ),
                        )
                    )
                    suggestions = [
                        suggestion
                        for suggestion in suggestions
                        if suggestion != default
                    ]
                options = meta.get("enum", [])
                options = [
                    option for option in options if option not in set(suggestions)
                ]

                for option in options:
                    items.append(
                        CompletionItem(
                            label=value2str(option),
                            kind=CompletionItemKind.Value,
                            label_details=CompletionItemLabelDetails(
                                description=meta.get("type", "value")
                            ),
                            documentation=MarkupContent(
                                kind=MarkupKind.Markdown, value=f"Option Value"
                            ),
                        )
                    )
                for suggestion in suggestions:
                    items.append(
                        CompletionItem(
                            label=value2str(suggestion),
                            kind=CompletionItemKind.Value,
                            label_details=CompletionItemLabelDetails(
                                description=meta.get("type", "value")
                            ),
                            documentation=MarkupContent(
                                kind=MarkupKind.Markdown, value=f"Suggestion Value"
                            ),
                        )
                    )
                logger.info(f"completion: completion on value, items : {items}")
                return CompletionList(is_incomplete=False, items=items)
        elif get_help_status == HelpStatus.NO_MODULE_TYPE_NAME:
            if parser_result.is_key_or_none == True and trigger_char == "@":
                for module_type in type_module_map:
                    items.append(
                        CompletionItem(
                            label=module_type,
                            kind=CompletionItemKind.Module,
                            label_details=CompletionItemLabelDetails(
                                description="ModuleField"
                            ),
                            documentation=MarkupContent(
                                kind=MarkupKind.Markdown,
                                value="ChildModule\n\nThe configure of `{module_type}` module",
                            ),
                        )
                    )
                return CompletionList(is_incomplete=True, items=items)

        return CompletionList(is_incomplete=False, items=items)

    def definition(
        self, position: Position, uri: str, source: str = None
    ) -> List[Location]:
        """get the definition information for the given position and uri

        Args:
            position: cursor position
            uri: the file uri

        Returns:
            list of Location object
        """
        word = self.cursor_word(uri, source, position, True)
        if not word:
            return []

        if source is None:
            source = self.server.workspace.get_document(uri).source
        parser_tree = self.parser_tree(uri, source)
        module_type, is_entry = get_module_type_by_uri(self.server, uri)
        logger.info(f"uri: {uri}. module_type: {module_type}")
        parser_result = self.parser_cursor(
            parser_tree, position, module_type, source, is_entry
        )

        if parser_result.semantic_trace is None:
            return []
        logger.info(f"parser_result : {parser_result}")
        module_name, traces = find_module_root(parser_result)
        logger.info(f"definition: module_name : {module_name}, traces : {traces}")

        if not module_name:
            return []
        module_help_meta, _ = self.get_module_help(module_name)
        if not module_help_meta:
            return []

        logger.info(f"definition: module_help_meta: {module_help_meta}")
        if not traces or traces == ["_base"]:
            file_path = module_help_meta.get("position", {})
            file_paths = []
            if file_path:
                file_paths.append(file_path)
            for inter_file_path in module_help_meta.get("inter_files", []):
                file_paths.append({"file_path": inter_file_path, "line_no": 0})
            return [
                Location(
                    uri=f"file://{file['file_path']}",
                    range=Range(
                        start=Position(line=max(file["line_no"] - 1, 0), character=0),
                        end=Position(line=max(file["line_no"] - 1, 0), character=0),
                    ),
                )
                for file in file_paths
            ]
        for trace in traces:
            module_help_meta = module_help_meta.get("properties", {}).get(trace, {})
        if module_help_meta and "position" in module_help_meta:
            para_position = module_help_meta.get("position", {})
            if not para_position:
                return []
            return [
                Location(
                    uri=f"file://{para_position['file_path']}",
                    range=Range(
                        start=Position(
                            line=max(para_position["line_no"] - 1, 0), character=0
                        ),
                        end=Position(
                            line=max(para_position["line_no"] - 1, 0), character=0
                        ),
                    ),
                )
            ]
        return []

    def hover(self, position: Position, uri: str = "", source: str = None) -> Dict:
        """resolve the hover information for the given position and uri

        Args:
            position: cursor position
            uri: the file uri

        Returns:
            Hover object or None

        """
        word = self.cursor_word(uri, source, position, True)
        logger.info(f"hover: position : {position}, word : {word}")
        if not word:
            return {
                "type": HoverType.CURSOR_WORD_NOT_FOUND,
                "field_type": None,
                "message": "Not found the cursor word",
                "range": Range(
                    start=position,
                    end=position,
                ),
            }
        if source is None:
            source = self.server.workspace.get_document(uri).source
        parser_tree = self.parser_tree(uri, source)
        module_type, is_entry = get_module_type_by_uri(self.server, uri)
        parser_result = self.parser_cursor(
            parser_tree, position, module_type, source, is_entry
        )
        if parser_result.semantic_trace is None:
            logger.error(f"hover parser_result : {parser_result}")
            return {
                "type": HoverType.RESOLVE_ERROR,
                "field_type": None,
                "message": "Can not resolve the semantic trace",
                "range": word[1],
            }
        module_name, traces = find_module_root(parser_result)

        if not module_name:
            return {
                "type": HoverType.RESOLVE_ERROR,
                "field_type": None,
                "message": "Can not resolve the module name",
                "range": word[1],
            }

        if traces and traces[0] in ["_G"]:
            return {
                "type": HoverType.SUCCESS,
                "field_type": None,
                "message": "On the global para",
                "range": word[1],
            }

        module_help_meta, get_help_status = self.get_module_help(module_name)
        if not isinstance(module_help_meta, dict):
            logger.error(
                f"hover: UN_COVER_ERROR, module_help_meta : {module_help_meta}"
            )
            return {
                "type": HoverType.UN_COVER_ERROR,
                "field_type": None,
                "message": "Unrecognized Case",
                "range": word[1],
            }

        if get_help_status != HelpStatus.SUCCESS:
            return {
                "type": HoverType.MODULE_NOT_FOUND,
                "field_type": None,
                "message": "Can not find the module help",
                "range": word[1],
            }

        if (not traces and parser_result.is_key_or_none == True) or (
            traces == ["_base"]
        ):
            return {
                "type": HoverType.SUCCESS,
                "field_type": "ModuleField",
                "message": dedent(
                    f"""
                    {module_name} -> `ModuleField`\r\n
                    {dedent(module_help_meta.get('description', '').strip())}
                    """
                ),
                "range": word[1],
            }
        trace = ""
        for trace in traces:
            module_help_meta = module_help_meta.get("properties", {}).get(trace, {})
        if not isinstance(module_help_meta, dict):
            return {
                "type": HoverType.UN_COVER_ERROR,
                "field_type": None,
                "message": "Unrecognized error",
                "range": word[1],
            }
        if not module_help_meta:
            return {
                "type": HoverType.HELP_INFO_NOT_FOUND,
                "field_type": None,
                "message": "Can not find the help info for this para.",
                "range": word[1],
            }

        def _option_rep(options):
            result = []
            for key in options:
                key = str(key)
                if len(key) > 10:
                    key = key[:8] + "..."
                result.append(f"    {key}")
            return "\n".join(result)

        if trace:
            type_name = module_help_meta.get("type_name", "")
            prefix = ""
            is_deprecated = module_help_meta.get("deprecated", False)
            if is_deprecated == True:
                prefix = "`Deprecated`\n"
            elif is_deprecated and isinstance(is_deprecated, str):
                prefix = f"`Deprecated` {is_deprecated}\n"
            if type_name:
                _trace = trace.replace("_", r"\_")
                type_str = f"""{_trace} -> **`{type_name}`**\n\n"""
            else:
                type_str = ""
            if parser_result.is_key_or_none == True:
                return {
                    "type": HoverType.SUCCESS
                    if not is_deprecated
                    else HoverType.DEPRECATED,
                    "field_type": type_name,
                    "message": f"""{prefix}{type_str}\n{dedent(module_help_meta.get("description", ""))}""",
                    "range": word[1],
                }
            else:
                options_list = module_help_meta.get("enum", [])
                suggest_list = module_help_meta.get("suggestions", [])
                addition_list = module_help_meta.get("additions", [])

                postfix = ""
                if options_list:
                    postfix = f"""`Options`:\n{_option_rep(options_list)}"""
                if suggest_list:
                    postfix = (
                        f"""{postfix}\n`Suggestions`:\n{_option_rep(suggest_list)}"""
                    )
                if addition_list:
                    postfix = (
                        f"""{postfix}\n`Additions`:\n{_option_rep(addition_list)}"""
                    )
                if options_list or addition_list:
                    return {
                        "type": HoverType.SUCCESS,
                        "field_type": type_name,
                        "message": f"""{prefix}{type_str}\n{dedent(module_help_meta.get("description", ""))}\n{postfix}""",
                        "candidate_value": {
                            "options": options_list,
                            "suggestions": suggest_list,
                            "additions": addition_list,
                        },
                        "range": word[1],
                    }
                else:
                    return {
                        "type": HoverType.SUCCESS,
                        "field_type": type_name,
                        "message": f"""{prefix}{type_str}\n{dedent(module_help_meta.get("description", ""))}\n{postfix}""",
                        "range": word[1],
                    }

        logger.error(
            f"hover: UN_COVER_ERROR, module_help_meta : {module_help_meta}, traces: {traces}"
        )
        return {
            "type": HoverType.UN_COVER_ERROR,
            "message": "Unrecognized case",
            "range": word[1],
        }

    def diagnostics(self, uri: str) -> List[Diagnostic]:
        """

        Args:
            uri: the file uri

        Returns:
            diagnostics information

        """
        ignore_keys = {"_anchor", "_G", "_search", "_base"}
        iter_fileds = {"NestField", "SubModule", "ModuleField"}

        @lru_cache(maxsize=64)
        def _(source, uri):
            tree = self.parser_tree(uri, source)

            def _resolve_tree(tree):
                diag_result = []

                if isinstance(tree, list):
                    for sub_tree in tree:
                        diag_result.extend(_resolve_tree(sub_tree))
                elif isinstance(tree, dict):
                    if tree.get("__type") == "document":
                        # detect the base module
                        detected = False
                        try:
                            for sub_tree in tree.get("__value", []):
                                if (
                                    (not isinstance(sub_tree, dict))
                                    or (sub_tree.get("__type", "") != "pair")
                                    or (
                                        sub_tree.get("__key", {}).get("__type")
                                        != "string"
                                    )
                                    or (
                                        sub_tree.get("__key", {}).get("__value")
                                        != "_base"
                                    )
                                ):
                                    logger.warning(
                                        f"diagnostics: skip document value in sub_tree: {sub_tree}"
                                    )
                                    continue
                                base_range = sub_tree.get("__key", {}).get(
                                    "__range", []
                                )
                                base_row, base_column = -1, -1
                                try:
                                    base_row, base_column = (
                                        base_range[0][0],
                                        (base_range[0][1] + base_range[1][1]) // 2,
                                    )
                                except:
                                    logger.warning(
                                        f"diagnostics: can not get base range sub_tree : {sub_tree}"
                                    )
                                    break
                                if base_row == -1 or base_column == -1:
                                    logger.warning(
                                        f"diagnostics: can not get the base_row or base_column, {sub_tree}"
                                    )
                                    break
                                base_position = Position(
                                    line=base_row, character=base_column
                                )
                                hover_result = self.hover(base_position, uri, source)
                                if hover_result["type"] == HoverType.SUCCESS:
                                    detected = True
                                else:
                                    diag_result.append(
                                        Diagnostic(
                                            range=Range(
                                                start=Position(
                                                    line=base_range[0][0],
                                                    character=base_range[0][1],
                                                ),
                                                end=Position(
                                                    line=base_range[1][0],
                                                    character=base_range[1][1],
                                                ),
                                            ),
                                            message="Can not resolve the module name",
                                            severity=DiagnosticSeverity.Error,
                                        )
                                    )
                                break

                        except Exception as e:
                            logger.error(f"diagnostics: detect base error : {e}")
                        try:
                            for sub_tree in tree.get("__value", []):
                                # if can not resolve the module name, ignore the paras for this module
                                if (
                                    not detected
                                    and isinstance(sub_tree, dict)
                                    and (sub_tree.get("__type", "") == "pair")
                                ):
                                    sub_tree_key = sub_tree.get("__key", {})
                                    if not isinstance(sub_tree_key, dict):
                                        logger.error(
                                            f"diagnostics: sub_tree_key : {sub_tree_key}"
                                        )
                                        continue
                                    if not (
                                        sub_tree_key.get("__type", "") == "string"
                                        and sub_tree_key.get("__value", "").startswith(
                                            "@"
                                        )
                                    ):
                                        continue
                                diag_result.extend(_resolve_tree(sub_tree))
                        except Exception as e:
                            logger.error(f"diagnostics: document value error : {e}")
                    elif tree.get("__type", "") == "pair":
                        key = tree.get("__key", {}).get("__value", "")
                        key_range = tree.get("__key", {}).get("__range", [])
                        key_row, key_column = -1, -1
                        # only the key without error, then check the value
                        key_passed = False
                        try:
                            key_row, key_column = (
                                key_range[0][0],
                                (key_range[0][1] + key_range[1][1]) // 2,
                            )
                        except:
                            return diag_result
                        if key_row == -1 or key_column == -1:
                            return diag_result
                        if key.startswith("@"):
                            key_position = Position(line=key_row, character=key_column)
                            hover_result = self.hover(key_position, uri, source)
                            if hover_result["type"] == HoverType.SUCCESS:
                                key_passed = True
                            else:
                                diag_result.append(
                                    Diagnostic(
                                        range=Range(
                                            start=Position(
                                                line=key_range[0][0],
                                                character=key_range[0][1],
                                            ),
                                            end=Position(
                                                line=key_range[1][0],
                                                character=key_range[1][1],
                                            ),
                                        ),
                                        message=hover_result["message"],
                                        severity=DiagnosticSeverity.Error,
                                    )
                                )
                        elif key in ignore_keys:
                            return diag_result
                        else:
                            key_position = Position(line=key_row, character=key_column)
                            hover_result = self.hover(key_position, uri, source)
                            if hover_result["type"] == HoverType.SUCCESS:
                                key_passed = True
                            elif hover_result["type"] == HoverType.DEPRECATED:
                                diag_result.append(
                                    Diagnostic(
                                        range=Range(
                                            start=Position(
                                                line=key_range[0][0],
                                                character=key_range[0][1],
                                            ),
                                            end=Position(
                                                line=key_range[1][0],
                                                character=key_range[1][1],
                                            ),
                                        ),
                                        message="This para is `deprecated`",
                                        severity=DiagnosticSeverity.Information,
                                    )
                                )
                            else:
                                logger.error(
                                    f"diagnostics: hover_result : {hover_result}"
                                )
                                diag_result.append(
                                    Diagnostic(
                                        range=Range(
                                            start=Position(
                                                line=key_range[0][0],
                                                character=key_range[0][1],
                                            ),
                                            end=Position(
                                                line=key_range[1][0],
                                                character=key_range[1][1],
                                            ),
                                        ),
                                        message=hover_result["message"],
                                        severity=DiagnosticSeverity.Error,
                                    )
                                )
                        if key_passed and hover_result["field_type"] in iter_fileds:
                            if not isinstance(tree, dict):
                                return diag_result
                            for sub_tree in tree.get("__value", []):
                                # only check the pairs
                                if (
                                    (not isinstance(sub_tree, dict))
                                    or (not (sub_tree.get("__type", "") == "pair"))
                                    or (
                                        not (
                                            sub_tree.get("__key", {}).get("__type")
                                            == "string"
                                        )
                                    )
                                ):
                                    continue
                                diag_result.extend(_resolve_tree(sub_tree))
                        else:
                            if not isinstance(tree, dict):
                                logger.info(f"diagnostics: not dict tree : {tree}")
                                return diag_result
                            # FIXME: options for list or dict value
                            try:
                                value = tree.get("__value", {}).get("__value", "")
                            except:
                                logger.warning(
                                    f"diagnostics: currently do not support list or dict value"
                                )
                                return diag_result
                            value_range = tree.get("__value", {}).get("__range", [])
                            value_row, value_column = -1, -1
                            try:
                                value_row, value_column = (
                                    value_range[0][0],
                                    value_range[0][1],
                                )
                            except:
                                return diag_result
                            value_position = Position(
                                line=value_row, character=value_column + 1
                            )
                            hover_result = self.hover(value_position, uri, source)
                            options = hover_result.get("candidate_value", {}).get(
                                "options", []
                            )
                            if options:
                                options = set(options)
                                if True in options:
                                    options.remove(True)
                                    options.add("true")
                                if False in options:
                                    options.remove(False)
                                    options.add("false")
                                if None in options:
                                    options.remove(None)
                                    options.add("null")
                                if value not in options:
                                    diag_result.append(
                                        Diagnostic(
                                            range=Range(
                                                start=Position(
                                                    line=value_range[0][0],
                                                    character=value_range[0][1],
                                                ),
                                                end=Position(
                                                    line=value_range[1][0],
                                                    character=value_range[1][1],
                                                ),
                                            ),
                                            message=f"{value} is not in supported options: `{options}`",
                                            severity=DiagnosticSeverity.Warning,
                                        )
                                    )
                    else:
                        logger.warning(f"diagnostics: not document or pair: {tree}")
                else:
                    logger.warning(f"diagnostics: not dict or list tree : {tree}")

                return diag_result

            return _resolve_tree(tree)

        source = self.server.workspace.get_document(uri).source
        return _(source, uri)

    def parser_tree(self, uri: str, source: str = ""):
        """parser the source to AST

        Args:
            uri: the source code uri

        Kwargs:
            source: optional, the source code

        Returns:
            the parser tree
        """

        @lru_cache(maxsize=128)
        def _(uri, source):
            if source is None:
                source = self.server.workspace.get_document(uri).source
            if (
                uri.endswith(".json")
                or uri.endswith(".jsonc")
                or uri.endswith(".json5")
                or uri.endswith(".hjson")
            ):
                try:
                    parser_tree = self.json_parser.parser(source)
                    return parser_tree
                except Exception as e:
                    logger.error(f"parser tree: json parser error : {e}")
                    return {}
            elif uri.endswith(".yaml") or uri.endswith(".yml"):
                try:
                    parser_tree = self.yaml_parser.parser(source)
                    return parser_tree
                except Exception as e:
                    logger.error(f"parser tree: yaml parser error : {e}")
                    return {}
            else:
                logger.warning(f"not support file type {uri}")
                return {}

        return _(uri, source)

    def parser_cursor(
        self,
        parser_tree,
        position: Position,
        module_type_from_uri: str,
        source: str,
        is_entry: bool,
    ) -> ParseResult:
        """parser the source to AST, and get the cursor position node information, and the trace information
        Args:
            parser_tree: the tree of parser result
            position: (line, character)
            module_type_from_uri: the module type detected from the uri
            is_entry: True means the file is a entry module, False means is a submodule
        Returns:
            the ParseResult object
        """
        _position: tuple = (position.line, position.character)

        @lru_cache(maxsize=128)
        def wrap(source, _position, module_type_from_uri, is_entry):
            result = {"is_entry": is_entry}
            result["parser_tree"] = parser_tree
            try:
                (
                    semantic_trace,
                    lex_trace,
                    trace_result,
                    is_key_or_none,
                    anchor_dict,
                    additional,
                ) = root_trace(parser_tree, _position, module_type_from_uri)
            except Exception as e:
                logger.error(f"hover: error : {e}")
                return ParseResult(**result)
            result["semantic_trace"] = semantic_trace
            result["lex_trace"] = lex_trace
            result["trace_result"] = trace_result
            result["is_key_or_none"] = is_key_or_none
            result["anchor_dict"] = anchor_dict
            result["additional"] = additional
            return ParseResult(**result)

        return wrap(source, _position, module_type_from_uri, is_entry)


if __name__ == "__main__":
    resolver = IntcResolve(LanguageServer("test", "0.1"))
