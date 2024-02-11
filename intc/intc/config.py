# Copyright the author(s) of intc.
#
# This source code is licensed under the Apache license found in the
# LICENSE file in the root directory of this source tree.

"""
the intc config module
"""
import copy
import inspect
import json
import re
from collections.abc import Callable
from enum import Enum
from typing import (
    Any,
    Callable,
    ClassVar,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from attrs import asdict
from attrs import define as define
from attrs import field, fields, fields_dict

from intc.exceptions import (
    AttrNameError,
    NoModuleFoundError,
    ValueError,
    ValueMissingError,
    ValueOutOfRangeError,
    ValueTypeError,
    ValueValidateError,
)
from intc.share import MISSING, get_registed_instance, registry
from intc.utils import UniModuleName, get_meta_rep, get_position, module_name_check


class CheckStatus(Enum):
    PASS = 0
    FAILED = 1
    SKIP = 2


class BasicCheck(object):
    """general check class, check the value is in options if options is not `None` or if the value is in additions skip all other check"""

    def __init__(
        self,
        options: Optional[List[Any]] = None,
        suggestions: Optional[List[Any]] = None,
        additions: Optional[List[Any]] = None,
        validator: Optional[Callable] = None,
        meta_str: str = "",
    ):
        """
        Args:
            options:
                the value should be in options
            suggestions:
                the suggested values
            additions:
                the values should skip all check, default values is null list, when there is only one addition value, you can set the value itself as additions ranther than a list.
        """
        super(BasicCheck, self).__init__()
        self.meta_str = meta_str
        assert isinstance(options, list) or options is None
        assert isinstance(suggestions, list) or suggestions is None
        assert isinstance(additions, list) or additions is None
        self.options = (
            None
            if options is None
            else set(
                [
                    json.dumps(o, sort_keys=True)
                    if (isinstance(o, dict) or isinstance(o, list))
                    else o
                    for o in options
                ]
            )
        )
        self.suggestions = (
            None
            if suggestions is None
            else set([json.dumps(s, sort_keys=True) for s in suggestions])
        )
        self.additions = (
            None
            if additions is None
            else set(
                [
                    json.dumps(a, sort_keys=True)
                    if (isinstance(a, dict) or isinstance(a, list))
                    else a
                    for a in additions
                ]
            )
        )
        self.validator = validator

    def basic_check(self, value) -> Tuple[Any, CheckStatus]:
        """if the value is in additions:
               return the value itself,
           if the options is not `None` and the value is not in options
               raise ValueError
           else
               return None
        Args:
            value: should checked value

        Returns:
            value and check status
        """
        if value == MISSING or (
            isinstance(value, str) and value.startswith("@") and "@lambda" in value
        ):
            # Skip check value for MISSING
            return value, CheckStatus.SKIP
        dump_value = (
            json.dumps(value, sort_keys=True)
            if (isinstance(value, dict) or isinstance(value, list))
            else value
        )
        if (self.additions is not None) and (dump_value in self.additions):
            return value, CheckStatus.SKIP
        if self.options is not None:
            if dump_value not in self.options:
                raise ValueValidateError(
                    f"Value `{dump_value}` is not in {self.options}. {self.meta_str}"
                )
            else:
                return value, CheckStatus.SKIP
        if self.validator is not None and not self.validator(value):
            validate_code = inspect.getsource(self.validator)
            raise ValueValidateError(
                f"Value {value} is not pass the validator:\n{validate_code}."
            )
        return value, CheckStatus.PASS


class NumConvert(BasicCheck):
    """check the value is a float data and is in range (lower, upper)"""

    def __init__(
        self,
        minimum: Optional[Union[int, float]],
        maximum: Optional[Union[int, float]],
        type_class: Union[Type[int], Type[float]],
        options: Optional[List[Union[int, float]]] = None,
        suggestions: Optional[List[Union[int, float]]] = None,
        additions: Optional[List[Any]] = None,
        validator: Optional[Callable] = None,
        meta_str: str = "",
    ):
        """
        Args:
            minimum:
                the value should be greater than minimum
            maximum:
                the value should be less than maximum
            type_class:
                the type of the value
            options:
                the value should be in options
            additions:
                the values should skip all check, default values is null list, when there is only one addition value, you can set the value itself as additions ranther than a list.
            validator:
                the value should pass the validator
            meta_str:
                the help message
        """
        super(NumConvert, self).__init__(
            options=options,
            suggestions=suggestions,
            additions=additions,
            validator=validator,
            meta_str=meta_str,
        )
        self.minimum = minimum if minimum is not None else -int(1e20)
        self.maximum = maximum if maximum is not None else int(1e20)
        self.type_class = type_class

    def __call__(self, value):
        check_value, check_status = self.basic_check(value)
        if value == -2:
            print(value)
            print(check_value)
            print(check_status)
        if check_status == CheckStatus.SKIP:
            return check_value
        try:
            value = self.type_class(value)
        except Exception as e:
            raise ValueTypeError(f"Cannot convert '{value}' to int. {self.meta_str}")
        if value > self.maximum or value < self.minimum:
            raise ValueOutOfRangeError(
                f"Value {value} is not in range [{self.minimum}, {self.maximum}]. {self.meta_str}"
            )
        return value


class StrConvert(BasicCheck):
    """check the value is a float data and is in range (lower, upper)"""

    def __init__(
        self,
        min_len: Optional[int] = None,
        max_len: Optional[int] = None,
        pattern: Optional[str] = None,
        options: Optional[List[Union[int, float]]] = None,
        suggestions: Optional[List[Union[int, float]]] = None,
        additions: Optional[List[Any]] = None,
        validator: Optional[Callable] = None,
        meta_str: str = "",
    ):
        """
        Args:
            minimum:
                the value should be greater than minimum
            maximum:
                the value should be less than maximum
            type_class:
                the type of the value
            options:
                the value should be in options
            additions:
                the values should skip all check, default values is null list, when there is only one addition value, you can set the value itself as additions ranther than a list.
            validator:
                the value should pass the validator
            meta_str:
                the help message
        """
        super(StrConvert, self).__init__(
            options=options,
            suggestions=suggestions,
            additions=additions,
            validator=validator,
            meta_str=meta_str,
        )
        self.min_len = min_len
        self.max_len = max_len
        self.pattern = None if pattern is None else re.compile(pattern)

    def __call__(self, value):
        check_value, check_status = self.basic_check(value)

        if check_status == CheckStatus.SKIP:
            return check_value
        try:
            value = str(value)
        except Exception as e:
            raise ValueTypeError(f"Cannot convert '{value}' to int. {self.meta_str}")
        if self.min_len is not None or self.max_len is not None:
            str_len = len(value)
            if self.min_len is not None and str_len < self.min_len:
                raise ValueOutOfRangeError(
                    f"The string length of {value} is less than {self.min_len}. {self.meta_str}"
                )
            if self.max_len is not None and str_len > self.max_len:
                raise ValueOutOfRangeError(
                    f"The string length of {value} is greater than {self.max_len}. {self.meta_str}"
                )
        if self.pattern is not None and not self.pattern.match(value):
            raise ValueValidateError(
                f"Value {value} is not match the pattern {self.pattern}. {self.meta_str}"
            )
        return value


class BasicConvert(BasicCheck):
    """check the value is in `options`"""

    def __init__(
        self,
        options: Optional[List[Any]] = None,
        suggestions: Optional[List[Any]] = None,
        additions: Optional[List[Any]] = None,
        validator: Optional[Callable] = None,
        meta_str: str = "",
    ):
        """
        Args:
            options:
                the value should be in options
            additions:
                the values should skip all check, default values is null list, when there is only one addition value, you can set the value itself as additions ranther than a list.
            validator:
                the value should pass the validator
            meta_str:
                the help message
        """
        super(BasicConvert, self).__init__(
            options=options,
            suggestions=suggestions,
            additions=additions,
            validator=validator,
            meta_str=meta_str,
        )

    def __call__(self, value):
        check_value, check_status = self.basic_check(value)
        if check_status in {CheckStatus.SKIP, check_status.PASS}:
            return check_value
        raise ValueError(f"Value {value} is not pass the value check")


def IntField(
    value: Union[int, str],
    help: str = "int field",
    options: Optional[List[int]] = None,
    suggestions: Optional[List[int]] = None,
    additions: Optional[List[Any]] = None,
    deprecated: Union[bool, str] = False,
    minimum: Optional[int] = None,
    maximum: Optional[int] = None,
    validator: Optional[Callable] = None,
) -> int:
    """integer field
    Args:
        value:
            the default value
        options:
            the value must be in options, when you provide options, the suggestions and additions will be ignored
        suggestions:
            the suggested values
        additions:
            when you want to add some value do not check the type and validate by the validator, you can set the value in the additions, like you can set additions = ['1', None] to accept the string '1' and `None` in the int filed
        minimum:
            the value should be greater than minimum
        maximum:
            the value should be less than maximum
        validator:
            the value should pass the validator
    """
    json_schema = {
        "description": help,
        "type_name": "IntField",
        "type": "integer",
        "default": value,
        "position": get_position(),
        "deprecated": deprecated,
    }
    if options is not None:
        assert (
            additions is None
        ), "options and additions cannot be set at the same time, when you want to add you can set all value in the options"
        json_schema["enum"] = options
    if additions is not None:
        json_schema["additions"] = additions
    if suggestions is not None:
        json_schema["suggestions"] = suggestions

    if value != MISSING:
        json_schema["default"] = value
    if minimum is not None:
        json_schema["minimum"] = minimum
    if maximum is not None:
        json_schema["maximum"] = maximum

    meta_str = get_meta_rep(json_schema)
    return field(
        init=True,
        default=value,
        converter=NumConvert(
            minimum=minimum,
            maximum=maximum,
            options=options,
            type_class=int,
            suggestions=suggestions,
            additions=additions,
            validator=validator,
            meta_str=meta_str,
        ),
        type=int,
        metadata=json_schema,
    )


def FloatField(
    value: Union[float, str],
    help: str = "float field",
    options: Optional[List[float]] = None,
    suggestions: Optional[List[float]] = None,
    additions: Optional[List[Any]] = None,
    deprecated: Union[bool, str] = False,
    minimum: Optional[float] = None,
    maximum: Optional[float] = None,
    validator: Optional[Callable] = None,
) -> float:
    """integer field
    Args:
        value:
            the default value
        options:
            the value must be in options, when you provide options, the suggestions and additions will be ignored
        suggestions:
            the suggested values
        additions:
            when you want to add some value do not check the type and validate by the validator, you can set the value in the additions, like you can set additions = ['1', None] to accept the string '1' and `None` in the float filed
        minimum:
            the value should be greater than minimum
        maximum:
            the value should be less than maximum
        validator:
            the value should pass the validator
    """
    json_schema = {
        "description": help,
        "type_name": "FloatField",
        "type": "number",
        "default": value,
        "position": get_position(),
    }
    if options is not None:
        assert (
            additions is None
        ), "options and additions cannot be set at the same time, when you want to add you can set all value in the options"
        json_schema["enum"] = options
    if additions is not None:
        json_schema["additions"] = additions
    if suggestions is not None:
        json_schema["suggestions"] = suggestions
    if deprecated is not None:
        json_schema["deprecated"] = deprecated

    if value != MISSING:
        json_schema["default"] = value
    if minimum is not None:
        json_schema["minimum"] = minimum
    if maximum is not None:
        json_schema["maximum"] = maximum
    meta_str = get_meta_rep(json_schema)
    return field(
        init=True,
        default=value,
        converter=NumConvert(
            minimum=minimum,
            maximum=maximum,
            options=options,
            type_class=float,
            suggestions=suggestions,
            additions=additions,
            validator=validator,
            meta_str=meta_str,
        ),
        type=float,
        metadata=json_schema,
    )


def BoolField(
    value: Union[bool, str],
    help: str = "bool field",
    additions: Optional[List[Any]] = None,
    deprecated: Union[bool, str] = False,
) -> bool:
    """bool field
    Args:
        value:
            the default value
        help:
            the help information
        additions:
            when you want to add some value do not check the type and validate by the validator, you can set the value in the additions, like you can set additions = ['1', None] to accept the string '1' and `None` in the float filed
        deprecated:
            whether this paras is deprecated
    """
    options = [True, False]
    json_schema = {
        "description": help,
        "enum": options,
        "type_name": "BoolField",
        "type": "boolean",
        "default": value,
        "position": get_position(),
    }
    if additions is not None:
        json_schema["additions"] = additions
    if deprecated is not None:
        json_schema["deprecated"] = deprecated

    if value != MISSING:
        json_schema["default"] = value

    meta_str = get_meta_rep(json_schema)
    return field(
        init=True,
        default=value,
        converter=BasicConvert(options=options, meta_str=meta_str, additions=additions),
        type=bool,
        metadata=json_schema,
    )


def StrField(
    value: Union[float, str, None],
    help: str = "float field",
    options: Optional[List[str]] = None,
    suggestions: Optional[List[str]] = None,
    additions: Optional[List[Any]] = None,
    deprecated: Union[bool, str] = False,
    min_len: Optional[int] = None,
    max_len: Optional[int] = None,
    pattern: Optional[str] = None,
    validator: Optional[Callable] = None,
) -> str:
    """integer field
    Args:
        value:
            the default value
        options:
            the value must be in options, when you provide options, the suggestions and additions will be ignored
        suggestions:
            the suggested values
        additions:
            when you want to add some value do not check the type and validate by the validator, you can set the value in the additions, like you can set additions = ['1', None] to accept the string '1' and `None` in the str filed
        min_len:
            if provide, the string length should be greater than min_len
        max_len:
            if provide, the string length should be less than max_len
        pattern:
            the string should match the pattern
        validator:
            the value should pass the validator
    """
    json_schema = {
        "description": help,
        "type_name": "StrField",
        "type": "string",
        "default": value,
        "position": get_position(),
    }
    if options is not None:
        assert (
            additions is None
        ), "options and additions cannot be set at the same time, when you want to add you can set all value in the options"
        json_schema["enum"] = options
    if additions is not None:
        json_schema["additions"] = additions
    if suggestions is not None:
        json_schema["suggestions"] = suggestions
    if pattern is not None:
        json_schema["pattern"] = pattern
    if deprecated is not None:
        json_schema["deprecated"] = deprecated

    if value != MISSING:
        json_schema["default"] = value
    if min_len is not None:
        json_schema["min_len"] = min_len
    if max_len is not None:
        json_schema["max_len"] = max_len
    meta_str = get_meta_rep(json_schema)
    return field(
        init=True,
        default=value,
        converter=StrConvert(
            min_len=min_len,
            max_len=max_len,
            pattern=pattern,
            options=options,
            suggestions=suggestions,
            additions=additions,
            validator=validator,
            meta_str=meta_str,
        ),
        type=str,
        metadata=json_schema,
    )


Dep = TypeVar("Dep", Any, None)


def AnyField(
    value: Type[Dep],
    help: str = "this could be any type",
    options: Optional[List[Any]] = None,
    suggestions: Optional[List[Any]] = None,
    additions: Optional[List[Any]] = None,
    deprecated: Union[bool, str] = False,
    validator: Optional[Callable] = None,
) -> Union[Type[Dep], Any]:
    """integer field
    Args:
        value:
            the default value
        options:
            the value must be in options, when you provide options, the suggestions and additions will be ignored
        suggestions:
            the suggested values
        additions:
            when you want to add some value do not check the type and validate by the validator, you can set the value in the additions, like you can set additions = ['1', None] to accept the string '1' and `None` in the any filed
        validator:
            the value should pass the validator
    """
    json_schema = {
        "description": help,
        "type_name": "AnyField",
        "type": "any",
        "default": value,
        "position": get_position(),
    }
    if options is not None:
        assert (
            additions is None
        ), "options and additions cannot be set at the same time, when you want to add you can set all value in the options"
        json_schema["enum"] = options
    if additions is not None:
        json_schema["additions"] = additions
    if suggestions is not None:
        json_schema["suggestions"] = suggestions
    if deprecated is not None:
        json_schema["deprecated"] = deprecated

    if value != MISSING:
        json_schema["default"] = value
    meta_str = get_meta_rep(json_schema)
    return field(
        init=True,
        default=value,
        converter=BasicConvert(
            options=options,
            suggestions=suggestions,
            additions=additions,
            validator=validator,
            meta_str=meta_str,
        ),
        type=Any,
        metadata=json_schema,
    )


def ListField(
    value: List,
    help: str = "the list field",
    suggestions: Optional[List[List]] = None,
    additions: Optional[List[Any]] = None,
    deprecated: Union[bool, str] = False,
    validator: Optional[Callable] = None,
) -> List:
    """integer field
    Args:
        value:
            the default value
        suggestions:
            the suggested values
        additions:
            when you want to add some value do not check the type and validate by the validator, you can set the value in the additions, like you can set additions = ['1', None] to accept the string '1' and `None` in the list filed
        validator:
            the value should pass the validator
    """
    json_schema = {
        "description": help,
        "type_name": "ListField",
        "type": "array",
        "default": value,
        "position": get_position(),
    }
    if additions is not None:
        json_schema["additions"] = additions
    if suggestions is not None:
        json_schema["suggestions"] = suggestions
    if deprecated is not None:
        json_schema["deprecated"] = deprecated

    if value != MISSING:
        json_schema["default"] = value
    meta_str = get_meta_rep(json_schema)
    if validator is None:
        _validator = lambda x: isinstance(x, list)
    else:
        _validator = lambda x: isinstance(x, list) and validator(x)
    return field(
        init=True,
        default=value,
        converter=BasicConvert(
            suggestions=suggestions,
            additions=additions,
            validator=_validator,
            meta_str=meta_str,
        ),
        type=List,
        metadata=json_schema,
    )


def DictField(
    value: Dict,
    help: str = "the dict field",
    suggestions: Optional[List[Dict]] = None,
    additions: Optional[List[Dict]] = None,
    deprecated: Union[bool, str] = False,
    validator: Optional[Callable] = None,
) -> Dict:
    """dict field
    Args:
        value:
            the default value
        suggestions:
            the suggested values
        additions:
            when you want to add some value do not check the type and validate by the validator, you can set the value in the additions, like you can set additions = ['1', None] to accept the string '1' and `None` in the dict filed
        validator:
            the value should pass the validator
    """
    json_schema = {
        "description": help,
        "type_name": "DictField",
        "type": "object",
        "default": value,
        "position": get_position(),
    }
    if additions is not None:
        json_schema["additions"] = additions
    if suggestions is not None:
        json_schema["suggestions"] = suggestions
    if deprecated is not None:
        json_schema["deprecated"] = deprecated

    if value != MISSING:
        json_schema["default"] = value
    meta_str = get_meta_rep(json_schema)
    if validator is None:
        validator = lambda x: isinstance(x, dict)
    else:
        validator = lambda x: isinstance(x, dict) and validator(x)
    return field(
        init=True,
        default=value,
        converter=BasicConvert(
            suggestions=suggestions,
            additions=additions,
            validator=validator,
            meta_str=meta_str,
        ),
        type=Dict,
        metadata=json_schema,
    )


def EnumField(
    value: Any,
    options: List[Any],
    help: str = "the enum field",
    deprecated: Union[bool, str] = False,
    validator: Optional[Callable] = None,
) -> Any:
    """dict field
    Args:
        value:
            the default value
        options:
            all the available values
        validator:
            the value should pass the validator
    """
    json_schema = {
        "description": help,
        "type_name": "DictField",
        "type": "object",
        "default": value,
        "enum": options,
        "position": get_position(),
    }
    if deprecated is not None:
        json_schema["deprecated"] = deprecated

    if value != MISSING:
        json_schema["default"] = value
    meta_str = get_meta_rep(json_schema)
    if validator is None:
        validator = lambda x: isinstance(x, list)
    else:
        validator = lambda x: isinstance(x, list) and validator(x)
    return field(
        init=True,
        default=value,
        converter=BasicConvert(
            options=options,
            validator=validator,
            meta_str=meta_str,
        ),
        type=Any,
        metadata=json_schema,
    )


class ModuleField(object):
    def __init__(self, child_data):
        self.__child_data__ = copy.deepcopy(child_data)
        self.__child_module__ = {}
        self.__uni_origin_keys_map__ = {}
        self.__update_unikeys__()

    def __get_module__(self, key, value):
        if key in self.__child_module__:
            return self.__child_module__[key]
        module_type_names = key.lstrip("@").split("#")[0].split("@")
        module_type, module_name = "", ""
        if len(module_type_names) == 2:
            module_type, module_name = module_type_names
        elif len(module_type_names) == 1:
            module_type = module_type_names[0]
        else:
            raise ValueError(
                f"the module name {key} is not valid, should be like `module_type[@module_name]`"
            )

        if isinstance(value, dict):
            if "_base" in value:
                module_name = value["_base"]
            if "_name" in value:
                module_name = value["_name"]
        child_class = get_registed_instance(module_type, module_name, get_class=True)
        child_class.__meta__ = {"_base": module_name}
        try:
            self.__child_module__[key] = child_class._from_dict(value)
        except Exception as e:
            raise ValueError(
                f"Init the {module_type}@{module_name} {child_class}, error: {e}"
            )
        return self.__child_module__[key]

    def __update_unikeys__(self):
        self.__uni_origin_keys_map__ = UniModuleName(
            [f"@{key}" for key in self.__child_data__.keys()]
        )

    def __iter__(self):
        for key in self.__child_data__:
            yield key

    def __getitem__(self, key):
        key = self.__uni_origin_keys_map__[f"@{key}"]

        return self.__get_module__(key[1:], self.__child_data__[key[1:]])

    def __getattr__(self, attr):
        return self.__getitem__(attr)

    def __len__(self):
        return len(self.__child_data__)

    def __eq__(self, another):
        try:
            if len(self) != len(another):
                return False
        except:
            return False
        for key in another:
            if key not in self.__child_data__:
                return False
        return True


def NestConvert(data_class: Any):
    """convert the nested value to data_class

    Args:
        options:
            the value should be in options
    Returns:
        the value itself
    """

    def _(value: dict, data_class=data_class):
        if isinstance(value, dict):
            return data_class(**value)
        else:
            return data_class(**asdict(value))

    return _


NestType = TypeVar("NestType")


def NestField(
    value: Type[NestType],
    help: str = "nested(dict like) field",
    suggestions: Optional[List[Dict]] = None,
    type: Type = Type[NestType],
) -> Type[NestType]:
    json_schema = {
        "description": help,
        "type_name": "NestField",
        "type": "object",
        "object_type": value,
        "position": get_position(),
    }
    if suggestions is not None:
        json_schema["suggestions"] = suggestions
    return field(
        default=define(value)(),
        converter=NestConvert(define(value)),
        type=type,
        metadata=json_schema,
    )


def SubmoduleConvert(
    valadator: Optional[Callable] = None, meta_str: Optional[str] = ""
):
    """convert the dict to submodules

    Args:
        valadator: the submodule dict should pass the valadator
        meta_str: the help message
    Returns:
        the value itself
    """

    def _(childs: Dict):
        if valadator is not None and not valadator(childs):
            raise ValueValidateError(
                f"{meta_str}\nValue {childs} is not pass the validator."
            )

        module_filed = ModuleField(childs)

        return module_filed

    return _


def SubModule(
    value: Dict,
    help: str = "the submodule field",
    suggestions: Optional[List[str]] = None,
    validator: Optional[Callable] = None,
) -> ModuleField:
    """
    Args:
        value:
            the default value
        suggestions:
            the suggested SubModule type
        validator:
            validate the submodule value

    Returns:
        a dict of submodule
    """
    json_schema = {
        "description": help,
        "type_name": "SubModule",
        "type": "object",
        "position": get_position(),
        "default": value,
    }
    if suggestions:
        json_schema["suggestions"] = suggestions
    meta_str = get_meta_rep(json_schema)
    return field(
        init=True,
        default=value,
        converter=SubmoduleConvert(validator, meta_str),
        type=type,
        metadata=json_schema,
    )


class IntCMeta(type):
    """
    Protect the class from using the protected name as parameter name
    """

    _deliver_num = 0

    def __new__(cls, name, bases, attrs):
        reserved = {
            "_module_name",
            "_from_dict",
            "_to_dict",
            "_get_module",
            "__meta__",
            "_base",
            "_name",
            "_search",
            "_json_schema",
            "_G",
            "_anchor",
        }
        if not "__attrs_attrs__" in attrs and "submodule" in attrs:
            submodule = attrs["submodule"]
            try:
                if submodule.metadata["type_name"] != "SubModule":
                    raise ValueTypeError(
                        f"submodule is reserved keyword and should be a `SubModule`"
                    )
            except:
                raise ValueTypeError(
                    f"submodule is reserved keyword and should be a `SubModule`"
                )
        if cls._deliver_num > 1:
            for attribute in attrs:
                if attribute in reserved:
                    raise AttrNameError(
                        f'{attribute} is in the protected set "{reserved}", you should not named the para as this name'
                    )
        cls._deliver_num += 1
        protected_class = super().__new__(cls, name, bases, attrs)
        cls.__meta__ = {}
        return protected_class


@define
class Base(metaclass=IntCMeta):
    __meta__ = {}

    def _valid_check(self):
        """check the config is valid
        Raises:
            ValueError: if the config is not valid
        """
        return True

    submodule = SubModule({})

    @classmethod
    def _from_dict(cls, config: Dict = {}) -> "Base":
        new_config = {}
        for key in config:
            if key in {"_base", "_name", "_search", "_G", "_anchor"}:
                continue
            elif key.startswith("@"):
                new_config["submodule"] = new_config.get("submodule", {})
                new_config["submodule"][key[1:].strip()] = config[key]
            else:
                new_config[key] = config[key]
        sample = cls(**new_config)
        sample._valid_check()
        return sample

    @property
    def _module_name(self):
        if self.__meta__.get("_base", ""):
            return self.__meta__["_base"]
        if self.__meta__.get("_name", ""):
            return self.__meta__["_name"]
        return ""

    def _get_named_modules(self, module_type: str = "") -> Dict[str, "Base"]:
        """get all named module of the module_type, if not provide the module_type, return all module

        Args:
            module_type: the module type
        Returns:
            a dict of module, key is the module name, value is the module config
        """
        module_dict = {}
        if "submodule" in self.__dir__():
            for module in self.submodule:
                if not module_type or module_type == module.split("#")[0].split("@")[0]:
                    module_dict[module] = self.submodule[module]
        return module_dict

    def _get_modules(self, module_type: str = "") -> List["Base"]:
        """get modules list of the module_type, if not provide the module_type, return all module

        Args:
            module_type: the module type
        Returns:
            a list of module
        """
        return list(self._get_named_modules(module_type).values())

    @classmethod
    def _json_schema(cls):
        def _rec_resolve(meta, data_info="root"):
            if not isinstance(meta, dict) or not meta:
                return meta

            schema = {}
            if data_info == "properties":
                for key in meta:
                    if key in {
                        "position",
                        "_name",
                        "lines",
                        "_G",
                        "_anchor",
                        "_base",
                        "_search",
                    }:
                        continue
                    schema[key] = _rec_resolve(meta[key], data_info="property")
                return schema
            elif data_info == "property":
                for key in meta:
                    if key in {
                        "type_name",
                        "default",
                        "position",
                        "_name",
                        "lines",
                        "_G",
                        "_anchor",
                        "_base",
                        "_search",
                    }:
                        continue
                    if key == "properties":
                        schema[key] = _rec_resolve(meta[key], data_info="properties")
                    else:
                        schema[key] = meta[key]
            else:
                assert data_info == "root"
                schema["properties"] = _rec_resolve(
                    meta.get("properties", {}), data_info="properties"
                )
                schema["type"] = "object"
                if meta.get("description", ""):
                    schema["description"] = meta["description"]
                schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
            return schema

        return _rec_resolve(cls.__meta__)

    def _to_dict(self, only_para: bool = False, lazy: bool = False) -> Dict:
        """convert the config object to dict
        Args:
            only_para: whether only convert the parameters defined in the class, ignore the `submodule` and `_name`
            lazy: whether parser the submodule directly
        Returns:
            a dict of the config
        """
        result = asdict(self)
        result.pop("submodule", None)
        result.pop("_anchor", None)
        if "submodule" in self.__dir__():
            if (not only_para) and (not lazy):
                for key in self.submodule:
                    result[f"@{key}"] = self.submodule[key]._to_dict(only_para)
            else:
                for key, value in self.submodule.__child_data__.items():
                    result[f"@{key}"] = value
        if not only_para and "__meta__" in self.__dir__():
            if self.__meta__.get("_base", ""):
                result["_name"] = self.__meta__["_base"]
            if self.__meta__.get("_name", ""):
                result["_name"] = self.__meta__["_name"]
        return result

    def __str__(self):
        return json.dumps(self._to_dict())

    def __getitem__(self, key):
        if key[0] in {"@", "#"}:
            return self.submodule[key[1:]]
        return getattr(self, key)


DataClassType = TypeVar("DataClassType")


def init_config(config, DataClass: Type[DataClassType] = Base) -> DataClassType:
    """ """
    for key in ["_G", "_search", "_anchor"]:
        config.pop(key, "")
    return DataClass._from_dict(config)


if __name__ == "__main__":
    pass
