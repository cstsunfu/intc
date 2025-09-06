# Copyright the author(s) of intc.
import json

from src.config import Model

from intc import MISSING, Parser, cregister, ic_repo, init_config

parser_configs = Parser(json.load(open("./config/model.json"))).parser_init()
assert len(parser_configs) == 1

print(parser_configs[0]["@model"].para1)
assert parser_configs[0]["@model"].para1 == 8
assert parser_configs[0]["@model"].para2 == 200
assert parser_configs[0]["@model"].para3 == 300
assert parser_configs[0]["@model"].para4 == 500
