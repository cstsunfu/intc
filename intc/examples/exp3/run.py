# Copyright the author(s) of intc.

import json

from src.config import BertEmbedding, ClsDecode, GloveEmbedding, Model

from intc import Parser, cregister, init_config

assert cregister.get("model", "simple_cls", get_class=True) == Model

parser_configs = Parser(json.load(open("./config/model.json"))).parser_init()
assert len(parser_configs) == 1
assert parser_configs[0]["@model"].active == "none"
assert parser_configs[0]["@model"]["@bert"].hidden_size == 768


parser_search_configs = Parser(
    json.load(open("./config/model_search.jsonc"))
).parser_init()
assert len(parser_search_configs) == 4

assert parser_search_configs[0]["@model"]["@glove"].dropout_rate == 0.2
assert parser_search_configs[0]["@model"]["@bert"].dropout_rate == 0.0
assert parser_search_configs[1]["@model"]["@glove"].dropout_rate == 0.3
assert parser_search_configs[1]["@model"]["@bert"].dropout_rate == 0.0

assert parser_search_configs[2]["@model"]["@glove"].dropout_rate == 0.2
assert parser_search_configs[2]["@model"]["@bert"].dropout_rate == 0.1
assert parser_search_configs[3]["@model"]["@glove"].dropout_rate == 0.3
assert parser_search_configs[3]["@model"]["@bert"].dropout_rate == 0.1
