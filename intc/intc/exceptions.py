# Copyright the author(s) of intc.
#
# This source code is licensed under the Apache license found in the
# LICENSE file in the root directory of this source tree.


class ValueMissingError(Exception):
    pass


class ValueTypeError(Exception):
    pass


class AttrNameError(Exception):
    pass


class ValueValidateError(Exception):
    pass


class ValueOutOfRangeError(Exception):
    pass


class ValueError(Exception):
    pass


class RepeatRegisterError(Exception):
    pass


class NoModuleFoundError(Exception):
    pass


class NameError(Exception):
    pass


class KeyNotFoundError(Exception):
    pass


class ParserConfigRepeatError(Exception):
    pass


class InConsistentNameError(Exception):
    pass
