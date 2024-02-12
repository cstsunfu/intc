# Copyright the author(s) of intc.
#
# This source code is licensed under the Apache license found in the
# LICENSE file in the root directory of this source tree.

import importlib
import io
import json
import logging
import os
import re
import sys
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple
from urllib.parse import urlparse

import hjson
from intc import ic_repo
from intc.loader import load_submodule
from lsprotocol.types import (
    ALL_TYPES_MAP,
    INITIALIZE,
    INITIALIZED,
    TEXT_DOCUMENT_CODE_ACTION,
    TEXT_DOCUMENT_COMPLETION,
    TEXT_DOCUMENT_DEFINITION,
    TEXT_DOCUMENT_DID_CHANGE,
    TEXT_DOCUMENT_DID_OPEN,
    TEXT_DOCUMENT_DID_SAVE,
    TEXT_DOCUMENT_FORMATTING,
    TEXT_DOCUMENT_HOVER,
    CodeAction,
    CodeActionKind,
    CodeActionOptions,
    CodeActionParams,
    Command,
    CompletionItem,
    CompletionItemKind,
    CompletionList,
    CompletionOptions,
    CompletionParams,
    CompletionTriggerKind,
    Diagnostic,
    DiagnosticSeverity,
    DocumentFormattingParams,
    Hover,
    InitializeParams,
    InitializeResult,
    InitializeResultServerInfoType,
    Location,
    MarkupContent,
    MarkupKind,
    Position,
    Range,
    SaveOptions,
    ServerCapabilities,
    TextDocumentPositionParams,
    TextDocumentSaveRegistrationOptions,
    TextDocumentSyncKind,
    TextEdit,
    WorkspaceEdit,
)
from pygls.protocol import lsp_method
from pygls.server import LanguageServer

from intc_lsp.src import HoverType, IntcResolve
from intc_lsp.version import __version__

logger = logging.getLogger("intc_lsp")


ALL_TYPES_MAP["TextDocumentSaveOptions"] = TextDocumentSaveRegistrationOptions


class IntcLanguageServer(LanguageServer):
    """The intc LanguageServer"""

    def __init__(
        self,
        name,
        version,
        text_document_sync_kind=TextDocumentSyncKind.Full,
        max_workers=4,
    ) -> None:
        super().__init__(
            name=name,
            version=version,
            text_document_sync_kind=text_document_sync_kind,
            max_workers=max_workers,
        )
        self.did_opend_files = set()
        self.resolve: IntcResolve = None
        self.options = {}
        self.modules_pattern = ""
        self.support_file_types = ["json", "yaml", "yml", "jsonc", "hjson", "json5"]
        self.entry_pattern = ""

    def update_config_partern(self, root_path):
        """update the pattern of the entry and modules
        Args:
            root_path:
                the root path of the workspace
        Returns:
            None
        """
        if not self.options:
            return
        entry_pattern = ""
        modules_pattern = ""
        for entry in self.options.get("entry", []):
            entry_path = os.path.join(
                root_path, entry, r"[^/]*\." + f"({'|'.join(self.support_file_types)})"
            )
            entry_pattern = (
                f"{entry_path}"
                if not entry_pattern
                else f"{entry_pattern}|{entry_path}"
            )
        for module in self.options.get("module", []):
            module_path = os.path.join(
                root_path, module, r"[^/]*\." + f"({'|'.join(self.support_file_types)})"
            )
            modules_pattern = (
                f"{module_path}"
                if not modules_pattern
                else f"{modules_pattern}|{module_path}"
            )
        logger.info(
            f"update_config_partern: entry_pattern : {entry_pattern}, modules_pattern : {modules_pattern}"
        )
        self.entry_pattern = re.compile(entry_pattern)
        self.modules_pattern = re.compile(modules_pattern)

    def init_new_file(self, params):
        uri = urlparse(params.text_document.uri).path
        if uri in self.did_opend_files:
            return
        logger.info(f"init_new_file: {uri}")
        try:
            root_path = Path(self.workspace.root_path)
        except Exception as e:
            root_path = Path(uri).parent

        intc_setting = ""
        real_root = Path(uri).parent
        while (root_path.parent != real_root) and not intc_setting:
            for meta_config in [".intc.json", ".intc.jsonc"]:
                if os.path.isfile(os.path.join(real_root, meta_config)):
                    intc_setting = os.path.join(real_root, meta_config)
                    break
            if not intc_setting:
                real_root = real_root.parent

        if not intc_setting:
            logger.info(f"self: can not found init setting for {uri}")
            return
        try:
            self.options = dict(hjson.load(open(intc_setting, "r")))
            self.update_config_partern(real_root)
            logger.info(f"init: load .intc.json done")
            logger.info(json.dumps(self.options, indent=4))
        except Exception as e:
            logger.error(f"init: load .intc.json error : {e}")
            self.show_message_log(f"intc_server: load .intc.json error")

        try:
            self.resolve = IntcResolve(intc_server)
            logger.info(f"init: init the intc_resolve")
        except Exception as e:
            logger.error(f"init: init intc_resolve error : {e}")
            self.show_message_log(f"intc_server: init intc_resolve error")

        logger.info(f"init: before dynamic import")
        logger.info(f"init: ic_repo: {ic_repo}")

        null_buffer = io.StringIO()
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        sys.stdout = null_buffer
        sys.stderr = null_buffer

        try:
            sys.path.append(str(real_root))
        except:
            logger.error(f"init: add root path {real_root} error")
        os.environ["IN_INTC"] = "1"
        for package in self.options.get("src", []):
            try:
                importlib.import_module(package)
                logger.info(f"init: import {package}")
            except Exception as e:
                logger.error(f"init: on import package `{package}` error : {e}")

        try:
            logger.info(load_submodule(str(real_root)))
        except Exception as e:
            logger.info(f"loader sub module error: {e}")

        sys.stdout = original_stdout
        sys.stderr = original_stderr
        null_buffer.seek(0)
        output = null_buffer.read()
        logger.info(f"init import output: {output}")
        logger.info(f"init: after dynamic import")
        logger.info(f"init: ic_repo: {ic_repo}")
        logger.info(f"init: init the intc_lsp done")
        self.did_opend_files.add(uri)


intc_server = IntcLanguageServer("intc-language-server", __version__)


@intc_server.feature(INITIALIZED)
def initialize(params: InitializeParams) -> Optional[InitializeResult]:
    """Initialize the language server
    Args:
        params:
            the init parameters provide by the client
    Returns:
        Optional[InitializeResult]
    """
    logger.info(f"init: paras: {params}")
    intc_server.show_message_log(f"intc_server: start init")
    if not intc_server.workspace.root_path:
        intc_server.show_message_log(f"init: no root path")
        return
    else:
        logger.info(f"init: root path: {intc_server.workspace.root_path}")


@intc_server.feature(
    TEXT_DOCUMENT_COMPLETION,
    CompletionOptions(trigger_characters=['"', ":", " ", "@"]),
)
def completions(params: CompletionParams) -> CompletionList:
    """Provide completion list trigger by the trigger_characters
    Args:
        params:
            the parameters provide by the client, provide the completion position and the source uri
    Returns:
        a list of completion items
    """
    logger.info(f"completions: paras: {params}")
    completions = intc_server.resolve.completions(
        params.position, params.text_document.uri, params.context.trigger_character
    )
    return completions


@intc_server.feature(TEXT_DOCUMENT_HOVER)
def hover(params: TextDocumentPositionParams) -> Optional[Hover]:
    """Provide the code help information of the hover position
    Args:
        server:
            the intc LanguageServer
        params:
            the parameters provide by the client, provide the hover position and the source uri
    Returns:
        a list of completion items
    """
    intc_server.show_message_log(f"on hover: {params}")

    logger.info(f"hover: paras: {params}")
    hover_result = intc_server.resolve.hover(params.position, params.text_document.uri)
    if hover_result["type"] not in {
        HoverType.RESOLVE_ERROR,
        HoverType.UN_COVER_ERROR,
        HoverType.CURSOR_WORD_NOT_FOUND,
    }:
        return Hover(
            contents=MarkupContent(
                kind=MarkupKind.Markdown, value=hover_result["message"]
            ),
            range=hover_result["range"],
        )
    else:
        return None


@intc_server.feature(TEXT_DOCUMENT_DEFINITION)
def definition(params: TextDocumentPositionParams) -> Optional[List[Location]]:
    """Provide completion list
    Args:
        server:
            the intc LanguageServer
        params:
            the parameters provide by the client, provide the hover position and the source uri
    Returns:
        a list of completion items
    """

    logger.info(f"definition: paras: {params}")
    definitions = intc_server.resolve.definition(
        params.position, params.text_document.uri
    )
    if definitions:
        return definitions


def diagnostics(params: TextDocumentPositionParams) -> None:
    """publish the diagnostics hint
    Args:
        server:
            the intc LanguageServer
        params:
            the parameters provide by the client, provide the source uri
    Returns:
        None
    """

    logger.info(f"diagnostics: paras: {params}")
    try:
        display_diagnostics = intc_server.resolve.diagnostics(params.text_document.uri)
    except Exception as e:
        logger.error(f"diagnostics: error : {e}")
        return
    logger.info(f"display: {display_diagnostics}")
    intc_server.publish_diagnostics(params.text_document.uri, display_diagnostics)


@intc_server.feature(TEXT_DOCUMENT_DID_OPEN)
def did_open(params):
    logger.info(f"did_open: paras: {params}")
    intc_server.init_new_file(params)
    diagnostics(params)


@intc_server.feature(TEXT_DOCUMENT_DID_CHANGE)
def did_change(params):
    logger.info(f"did_change: paras: {params}")
    diagnostics(params)


if __name__ == "__main__":
    intc_server.start_io()
