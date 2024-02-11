# Copyright the author(s) of intc.
import json

# import intc_lsp
from src import Model

from intc import Parser, cregister, ic_repo, init_config

print(cregister.get("model", "submodule_exp", get_class=True) == Model)

parser_configs = Parser(json.load(open("./config/model.json"))).parser()
print(ic_repo)
# print(parser_configs)
# print(init_config(parser_configs[0])["@model"]["@glove"].dropout_rate)
