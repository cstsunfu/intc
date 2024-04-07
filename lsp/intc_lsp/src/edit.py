# Copyright the author(s) of intc.
#
# This source code is licensed under the Apache license found in the
# LICENSE file in the root directory of this source tree.

import time

from tree_sitter import Language, Parser


def get_change(old_source_byte: bytes, new_source_byte: bytes):
    """get the changed range between old source and new source
    Args:
        old_source_byte: the old source
        new_source_byte: the new source
    Returns:
        a dict contain the changed range
    """
    old_byte_lines = old_source_byte.split(b"\n")
    new_byte_lines = new_source_byte.split(b"\n")
    start_line = 0
    start_byte = 0
    old_end_line = len(old_byte_lines)
    new_end_line = len(new_byte_lines)
    old_end_byte = len(old_source_byte)
    new_end_byte = len(new_source_byte)
    for i in range(min(len(old_byte_lines), len(new_byte_lines))):
        if not old_byte_lines[i] == new_byte_lines[i]:
            break
        start_line = i
        start_byte += len(old_byte_lines) + 1

    for i in range(1, min(len(old_byte_lines), len(new_byte_lines))):
        if not old_byte_lines[-i] == new_byte_lines[-i]:
            old_end_line -= i
            new_end_line -= i
            break
        cur_line_byte = len(old_byte_lines[-i]) + 1
        old_end_byte -= cur_line_byte
        new_end_byte -= cur_line_byte
    return {
        "start_byte": start_byte,
        "old_end_byte": old_end_byte,
        "new_end_byte": new_end_byte,
        "start_point": (start_line, 0),
        "old_end_point": (old_end_line, 0),
        "new_end_point": (new_end_line, 0),
    }


if __name__ == "__main__":
    HJSON_LANGUAGE = Language("intc_lsp/lib/json_ts.so", "json")
    parser = Parser()
    parser.set_language(HJSON_LANGUAGE)

    old_source_str = """
    {
        "processor": {
            "_base": "basic@span_cls#pretrained",
            "config": {
                "feed_order": ["load", "seq_lab_loader", "tokenizer", "label_gather", "span_cls_relabel", "save"]
                "tokenizer_config_path": "./data/bert/tokenizer.json", // the tokenizer config path (the tokenizer.json path)
                "data_dir": "./bert/output/",  // save load data base dir
                "size": 3,  // save load data base dir
                "drop": 0.3,  // save load data base dir
            },
        }
    }
    """

    new_source_str = """
    {
        "processor": {
            "_base": "basic@span_cls#pretrained",
                "drop": 0.3,  // save load data base dir
            },
        }
    }
    """

    old_source = old_source_str.encode("utf8")
    new_source = new_source_str.encode("utf8")

    old_tree = parser.parse(old_source)

    ctime = 0
    for _ in range(1000):
        ss = time.time()
        changes = get_change(old_source, new_source)
        old_tree.edit(**changes)
        ctime += time.time() - ss
        new_tree = parser.parse(new_source, old_tree)
    print(f"get diff: {ctime}")

    start = time.time()
    for _ in range(1000):
        changes = get_change(old_source, new_source)
        old_tree.edit(**changes)
        new_tree = parser.parse(new_source, old_tree)
    end = time.time()
    print(f"get diff + add parse: {end - start}")

    start = time.time()
    for _ in range(1000):
        # old_tree.edit(**get_change(old_source_str, new_source_str))
        new_tree = parser.parse(new_source)
    end = time.time()
    print(f"full parse new: {end - start}")

    start = time.time()
    for _ in range(1000):
        # old_tree.edit(**get_change(old_source_str, new_source_str))
        new_tree = parser.parse(old_source)
    end = time.time()
    print(f"full parse old: {end - start}")
