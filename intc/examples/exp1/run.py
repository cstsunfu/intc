# Copyright the author(s) of intc.

import json

from src import BertEmbedding, ClsDecode, GloveEmbedding, Model

from intc import Parser, cregister, init_config

# print(cregister.get("model", "simple_cls", get_class=True) == Model)

# parser_configs = Parser(json.load(open("./config/model_search.json"))).parser_init()
# print(parser_configs)
# print(parser_configs[0]["@embedding"])
# print(parser_configs[0]["@model"])
# print(type(parser_configs[0]))
# print(type(parser_configs[0]))

print(
    Parser(
        {
            # "_anchor": "a",
            "para1": 1,
            "para2": 100,
            "@children": {
                # "_anchor": "c",
                "cpara2": "a",
                "cpara1": "...",
                "cpara3": "@lambda @_G.t",
            },
            # "para3": "@c.cpara2 @lambda x: x",
            "_G": {"t": "t"}
            # "_search": {
            #     "para1": [1, 2, 3],
            #     "para2": "@lambda _: [100, 200, 300]",
            #     # "@children.cpara2": ["a", "b", "c"],
            # },
        },
    ).parser()
)
