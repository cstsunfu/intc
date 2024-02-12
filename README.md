<p align="center">
  <h2 align="center"> Python Intelligence Config Manager</h2>
</p>

<p align="center">
A Python Config Manager for Humans
</p>


<div style="text-align:center">
<span style="width:70%;display:inline-block">

![main](./pics/vsc_main.png)
</div>

<h4 align="center">
    <p>
        <b>English</b> |
        <a href="https://github.com/cstsunfu/intc/blob/main/README_zh.md">简体中文</a>
    </p>
</h4>


* [Installation](#installation)
* [Feature List](#feature-list)
* [Intc Use Case](#intc-use-case)
    * [Parameter reference and lambda syntax](#parameter-reference-and-lambda-syntax)
    * [Parameter search](#parameter-search)
    * [DataClass && Json Schema](#dataclass-json-schema)
* [Intc-LSP](#intc-lsp)
    * [Hover Document](#hover-document)
    * [Diagnostic](#diagnostic)
    * [Completion](#completion)
    * [Goto/Peek Definition](#gotopeek-definition)

`intc` is a powerful intelligent config management tool that provides features such as module inheritance, nested modules, parameter references, hyperparameter search, and support for dynamic parameter calculation using lambda expressions.

The accompanying Language Server Protocol (`intc-lsp`) enhances our editing and browsing experience, tightly integrating configuration files with Python code. `intc-lsp` helps you conveniently access Python semantic information while writing and reading `intc` files, offering features such as error prompts, parameter completion, intelligent navigation, and parameter help document display.

In addition to being used for config files, `intc` can also be directly used as a `dataclass`. It can convert `dataclasses` defined using `intc` into JSON schemas for data type constraints, and can also perform data checks on JSON data, including return values from tools like `LLM`, generating error prompts for iterative optimization in `LLM`.


### Installation

1. Prepare a Python environment, requiring `python>=3.8`, and currently tested only on `Linux` and `Mac`. Support for `Windows` may have issues.
2. Install `intc` and `intc-lsp`. If you don't need features like intelligent completion, you can only install `intc`.


```bash
# install from pypi
pip install intc
pip install intc-lsp
```


Or from source:

```bash
cd intc/
pip install .
cd ../lsp
pip install .
```

3. Installing Intelligent Completion Plugins

`intc` provides a generic Language Server Protocol (`LSP`), theoretically usable with any editor or `IDE` that supports `LSP`. However, I primarily use `(neo)vim` for most of my work and occasionally `vscode`, so the adaptation has been done for these two editors.

* Neovim

`Neovim` is powerful and easy to extend, and the community has provided very friendly support for `LSP`. Refer to `plugins/neovim` for specific instructions.

* VSCode

`VSCode` can also support `LSP` by installing the corresponding plugin for `intc-lsp`. Refer to `plugins/vscode` for specific instructions.

* Other IDEs and Editors

  Assistance from experienced individuals is needed to improve documentation for other IDEs and editors.

### Feature List

Below is a brief introduction to some of the main features. For detailed usage, you can jump to the corresponding use case.

* Module Inheritance
    * `intc` Python classes can inherit from each other like normal Python classes.
    * `intc` config files are parameter instantiations of Python classes and can also be seen as inheriting from Python classes.
    * Additionally, in some complex config files, there can also be inheritance relationships between configs.

* Nested Modules
    * Modules can be nested, with a higher-level module containing parameters as well as other sub-modules. For example, in a task of training neural networks, a trainer can contain not only its parameters but also sub-modules like model, optimizer, and scheduler.

* Parameter References
    * A parameter can depend on the value of one or more other parameters, supporting lambda dynamic parameter value calculation.

* Parameter Search
    * In many tasks, there are multiple parameter combinations. `intc` expands all parameter combinations in the form of Cartesian products.

* Dataclass
    * Can be used directly as a dataclass for a module's parameter class, can generate JSON schemas, and can perform parameter checks.

* Config Help Document
    * `intc-lsp` provides parameter hover prompts, displaying parameter help documents when the pointer is placed over a parameter.

* Config Error Prompt
    * `intc-lsp` checks if your parameter fillings are correct.

* Config Parameter Completion
    * `intc-lsp` provides semantic completion while editing config files.

* Config Parameter Navigation
    * `intc-lsp` provides `goto/peek definition` support for browsing or editing config files, leveraging Python source code.

* etc.

### Intc Use Case

We will start by introducing the basic usage of `intc` with an example from `intc/examples/exp1`.

Example structure:

```
├── config                         -- config file，support the json or jsonc，you should point the path to config in the .intc.json
│   ├── model.json
│   └── model_search.jsonc
├── .intc.json                     -- for intc
├── run.py                         -- your own code
└── src                            -- your project
    └── __init__.py
```

Compared with an ordinary python project, the intc project requires a `.intc.json` file to describe some `meta` data of the project. The following is the configuration in this exp:

```.intc.json
{
    // "module": ["config/module"],  // the directory for submodule config, relative to currently directory, for this example there is no submodule
    "entry": ["config"],                 // the main config file path
    "src": [                           // the python module used for this project
        "src"
    ]
}

```

The Python code using `intc` is very similar to `dataclass`. Compared with original dataclass, it provides functions such as numerical checking, model registration, and json schema generation, etc.

```python
from intc import (
    MISSING,            # MISSING is a const value, in intc it always be `???`
    Base,               # all the intc config class/dataclass will inherit this class
    BoolField,          # bool field
    DictField,          # dict field
    FloatField,         # ...
    IntField,
    AnyField,
    ListField,
    NestField,          # nested field, it's is a dict that can accept the constraints of the key and value
    StrField,
    SubModule,
    cregister,          # register for intc, you can registed a dataclass to cregister, the key is a tuple (module_type, module_name))


@cregister("model", "simple_cls")  # registed the Model as ("model", "simple_cls"), which `module_type is model`, `module_name is simple_cls`
class Model(Base):                 # inherit the Base class, or you can just omit it, like the BertEmbedding at below
    embedding_combine_method = StrField( # the intc attribute
        value="concat",                  # default value
        options=["concat", "concat_linear"], # the value must be one of these
        help="the combine method, just `concat` or use `linear` on the concated embedding",
    )
    embedding_size = IntField(
        value=MISSING, help="the sum of bert and glove embedding size" # if the default value is MISSING, you must provide one when you init it
    )
    active = StrField(
        value="relu",
        options=["relu", "tanh", "sigmoid", "none"],
        help="the activation function",
    )
    submodule = SubModule(   # submodules, you can nested other dataclass/intc config in it
        value={},
        suggestions=[        # suggestions means some suggestion submodules, it's useful for intc-lsp to complete
            "embedding",
            "decode",
        ],
        help="submodules for basic model",
    )

@cregister("embedding", "bert")
class BertEmbedding:
    hidden_size = IntField(
        value=MISSING,
        minimum=1,
        help="the input/output/hidden size for bert, must >= 1",
    )
    dropout_rate = FloatField(
        value=0.0, minimum=0.0, maximum=1.0, help="the dropout rate for bert"  #
    )
....
```

In the actual development process, we often use config files to configure business logic, and `json` (and its derived formats, such as `jsonc`) is very suitable for editing configuration files. `intc` combined with `intc-lsp` provides a very good solution for this. The following is an example of configuring an existing dataclass:

```jsonc
// file config/model.jsonc
{
    "@model@simple_cls": {  // Indicates who is configuring, in the format of @module_type@module_name @model@simple_cls corresponding to the `Model` registered with this name
        "active": "none",
        "embedding_size": "@$.@glove.hidden_size, @$.@bert.hidden_size @lambda x, y: x+y", // The value here is calculated by dynamic lambda. The value of embedding_size is the sum of @embedding@glove.hidden_size and @embedding@bert.hidden_size. For the syntax of lambda, please see the introduction to lambda in this manual.
        "@embedding@glove": { // submodule, submodule also recognized as @module_type@module_name
            "hidden_size": 300,
            "vocab_size": 5000
        },
        "@embedding@bert": {
            "hidden_size": 768
        }
    }
}
```

#### Parameter reference and lambda syntax

We often encounter that the output of an encode module has the same dimension as the input of the decode module. In the configuration file, we hope that the values of these two parameters are always consistent. Intc supports one parameter being a reference to another parameter, so that we only if one of the parameters needs to be modified, the value of the other parameter is also modified simultaneously.

Sometimes the value of one of our parameters depends on multiple other parameters. For example, in a multi-encode model, the input dimension of the decode module is the sum of the dimensions output by all encode models. For such complex references, intc provides `lambda` Supports complex dynamic value calculations.

Before introducing `lambda` expressions, we first introduce the reference rules of parameters:

Let’s take the following config as an example:

```json
{
    "@parent@p": {
        "para_p_a": "value_p_a"
        "@wang@lao": {
            "para_lao": "value_lao"
        },
        "@children@wang": {
            "_anchor": "cwang",
            "para_wang_a": "value_wang_a",
        },
        "@children@li": {
            "para_li_a": "value_li_a",
            "para_li_b": "..."
        },
        "para_p_b": "..."
    },
    "para_a": "value_a"
}
```
We want to reference the value elsewhere when calculating `para_p_b`:

The vanilla way:

* If we want to reference the value of `para_p_a`, `para_p_a` is at the same level as the current position, we use `$` to indicate the same level, then the reference of the value of `para_p_a` at the position of `para_p_b` should be written as `$ .para_p_a`
* If we want to refer to the value of `para_a`, `para_a` is one level above the current position, we use `$$` to represent the previous level (I believe you are smart and have discovered that each additional `$` represents the previous level) go back one more level), then the reference of the value of `para_a` at the position of `para_p_b` should be written as `$$.para_a`
* If we want to reference the value of `para_li_a`, we can find that `para_li_a` is located at the next level of `@children@li` at the same level as the current position, so the value of `para_li_a` should be referenced at the position of `para_p_b` Written as `$.@children@li.para_li_a`

Simplified expression:

Since expressions such as `@children@li` as module names are often very long and inconvenient to write, we often only need the prefix or suffix of the module name to distinguish a module, so the last example above is in `para_p_b` The value of `para_li_a` quoted everywhere can be written as `$.@li.para_li_a`, where `@children@li` is simplified to `@li` without causing ambiguity. It should be noted that the simplification here must be The prefix or suffix of the original expression can only be used in module names (that is, it can only be staged with special symbols such as `@`). This is done to reduce the difficulty of reading and reduce the occurrence of ambiguity.

Anchor point:

And if we want to reference the value of `para_wang_a` at `para_p_b`, the path here also has to go through a module name `@children@wang`. We cannot use the above simplified expression technique, because no matter we choose the prefix `@children` (the prefix of `@children@li`) or the suffix `@wang` (the prefix of `@wang@old` is `@wang`) will cause ambiguity, so we can only honestly write down the full Is it famous? Not so. In order to make some long-distance references more convenient, intc also supports `global anchors` to provide convenience for remote dependencies. In this example, we see that there is a` inside `@children@wang` _anchor` keyword, we can reference the value of `_anchor` at any position to refer to the sibling element at its position. Therefore, at `para_p_b` we can refer to the value of `para_wang_a` through `cwang.value_wang_a` .

It should be noted that there can be multiple `_anchor`, but the same name must not appear. Each value of `_anchor` must be globally unique, so do not set `_anchor` in a submodule.

Syntax for value references:
The reference of intc is realized through `@lambda` expression. The reference rules are:

```
{
    "para1": "value1",
    "para2": "@lambda @$.para1"
}
```

In addition to being used for value references, `lambda` can also be used in very complex situations. The following are the `lambda` syntax types and usage examples supported by intc:

1. General Grammar

The most common syntax for intc's `lambda` is

```
@para_1, @para_2, ...@para_n  @lambda x1, x2, ...xn: use x1 to xn calc the value
|__________________________|  |________________________________________________|
             │                                     │
  Here you need to pass a            The lambda expression here follows
  lambda parameter that              Python's lambda syntax rules. The
  corresponds to the                 parameters passed in are the
  parameters of the                  corresponding parameter names.
  subsequent lambda
  expression <para_1 -> x1>.
  The expression of each
  para here follows the
  reference rules.
```

```json
{
    "para1": 1,
    "para2": 2,
    "para3": "@$.para1, @$.para2 @lambda x, y: x+y"
}
```
Here `para3` is a value that needs to be calculated by `lambda`. The calculation result is the value of `para1` and `para2` and `3`

2. `lambda` calculation
Sometimes we simply want to calculate a value through `lambda` without referencing other parameters, then we can write like this:

```json
{
    "para1": "@lambda _: list(range(100))"
}
```

At this time, the value of `para1` is still a `lambda` expression, but the input parameter of this expression is empty, and the value of this expression is `[0, 1, 2..., 98, 99]`

3. Value reference through lambda

The syntax is described in the Parameter Reference section


#### Parameter search

When doing experiments, we need to verify the combination of multiple parameters. `intc` provides us with the ability to parameter grid search. It combines each search condition in the form of a Cartesian product and returns a config list.

```jsonc
// data.json
{
    "para1": 1,
    "para2": 100,
    "@children":{
        "cpara1": 1000,
        "cpara2": "a",
        "_search": {
            "cpara1": "@lambda _: list(range(1000, 1003))"
        }
    },
    "_search": {
        "para1": [1, 2, 3],
        "para2": "@lambda _: [100, 200, 300]",
        "@children.cpara2": ['a', 'b', 'c']
    }
}

```

```python
import json
from intc import Parser
assert len(Parser(json.load(open('data.json')).parser())) == 81
```

As shown in the example, the value searched for by the argument of `intc` can be a `list` or a `lambda` expression returning a `list`, but the `lambda` expression currently used in `_search` is currently Only value calculation is supported, and other parameters cannot be referenced to participate in the calculation. The reason for this restriction is that `_search` itself may change the structure of config, and the reference must be made when the config structure is fixed. So the calculation of the actual reference happens after `_search` generates the fixed config

#### DataClass && Json Schema

In addition to being used as a config management tool, `intc` can also be used as a `dataclass`. In particular, `intc`, in addition to supporting the import and export of general `json` data, can also export `json schema` according to the definition. , which is very useful for some specific scenarios such as agreeing on the input and output format of a large model.

```python
import json

from intc import MISSING, Base, IntField, NestField, StrField, dataclass


@dataclass
class LLMOutput(Base):
    """The output of the LLM model"""

    user_name = StrField(value=MISSING, help="Name of the person")

    class Info:
        age = IntField(value=MISSING, minimum=1, maximum=150, help="Age of the person")
        blood_type = StrField(
            value=MISSING, options=["A", "B", "AB", "O"], help="Blood type"
        )

    user_info = NestField(value=Info, help="User information")
    lines = IntField(value=MISSING, help="Number of lines in the output")
print(json.dumps(LLMOutput._json_schema(), indent=4))
```

Json Schema Output:
```json
{
    "properties": {
        "user_name": {
            "description": "Name of the person",
            "type": "string",
            "deprecated": false
        },
        "user_info": {
            "description": "User information",
            "type": "object",
            "properties": {
                "age": {
                    "description": "Age of the person",
                    "type": "integer",
                    "deprecated": false,
                    "minimum": 1,
                    "maximum": 150
                },
                "blood_type": {
                    "description": "Blood type",
                    "type": "string",
                    "enum": [
                        "A",
                        "B",
                        "AB",
                        "O"
                    ],
                    "deprecated": false
                }
            }
        }
    },
    "type": "object",
    "description": "The output of the LLM model",
    "$schema": "https://json-schema.org/draft/2020-12/schema"
}
```
### Intc-LSP
#### Hover Document

<div style="text-align:center">
<span style="width:47%;display:inline-block">

![nvim hover](./pics/nvim_hover.png)

</span>
<span style="width:47%;display:inline-block">

![vsc hover](./pics/vsc_hover.png)

</span>
</div>

#### Diagnostic

<div style="text-align:center">
<span style="width:47%;display:inline-block">

![nvim diag](./pics/nvim_diag.png)

</span>
<span style="width:47%;display:inline-block">

![vsc diag](./pics/vsc_diag.png)

</span>
</div>

#### Completion

<div style="text-align:center">
<span style="width:47%;display:inline-block">

![nvim comp](./pics/nvim_comp.png)

</span>
<span style="width:47%;display:inline-block">

![vsc comp](./pics/vsc_comp.png)

</span>
</div>

#### Goto/Peek Definition

<div style="text-align:center">
<span style="width:47%;display:inline-block">

![nvim goto](./pics/nvim_goto.png)

</span>
<span style="width:47%;display:inline-block">

![vsc goto](./pics/vsc_goto.png)

</span>
</div>
