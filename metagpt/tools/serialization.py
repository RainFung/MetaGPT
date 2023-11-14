#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/11/04
@Author  : rain
@File    : serialization.py
"""
from __future__ import annotations

import dataclasses
import enum
import functools
import logging
import sys
from importlib import import_module
from typing import TYPE_CHECKING, Any, Pattern, TypeVar, Union, cast

import attr
# import re2
from metagpt.llm import LLM
if TYPE_CHECKING:
    from types import ModuleType

log = logging.getLogger(__name__)

MAX_RECURSION_DEPTH = sys.getrecursionlimit() - 1

CLASSNAME = "__classname__"
VERSION = "__version__"
DATA = "__data__"
SCHEMA_ID = "__id__"
CACHE = "__cache__"

OLD_TYPE = "__type"
OLD_SOURCE = "__source"
OLD_DATA = "__var"
OLD_DICT = "dict"

DEFAULT_VERSION = 0

T = TypeVar("T", bool, float, int, dict, list, str, tuple, set)
U = Union[bool, float, int, dict, list, str, tuple, set]
S = Union[list, tuple, set]

_serializers: dict[str, ModuleType] = {}
_deserializers: dict[str, ModuleType] = {}
_stringifiers: dict[str, ModuleType] = {}
_extra_allowed: set[str] = set()

_primitives = (int, bool, float, str)
_builtin_collections = (frozenset, list, set, tuple)  # dict is treated specially.


def get_module_name(obj):
    if callable(obj) and hasattr(obj, "__module__") and hasattr(obj, "__name__"):
        return f"{obj.__module__}.{obj.__name__}"

    cls = obj if isinstance(obj, type) else type(obj)
    module = cls.__module__
    name = cls.__qualname__
    if module and module != "__builtin__":
        return f"{module}.{name}"
    else:
        return name


import pkgutil
from importlib import import_module
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from types import ModuleType


def import_string(dotted_path: str):
    """
    Import a dotted module path and return the attribute/class designated by the last name in the path.

    Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit(".", 1)
    except ValueError:
        raise ImportError(f"{dotted_path} doesn't look like a module path")

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError:
        raise ImportError(f'Module "{module_path}" does not define a "{class_name}" attribute/class')


def serialize(obj: object):
    """
    """
    # None tpyes remains None
    if obj is None:
        return obj

    # primitive types remains self
    if isinstance(obj, _primitives):
        if isinstance(obj, enum.Enum):
            return obj.value
        return obj

    # iterator types
    if isinstance(obj, set):
        return set(serialize(o) for o in obj)
    if isinstance(obj, frozenset):
        return frozenset(serialize(o) for o in obj)
    if isinstance(obj, list):
        return [serialize(o) for o in obj]
    if isinstance(obj, tuple):
        return tuple(serialize(o) for o in obj)
    if isinstance(obj, dict):
        return {str(k): serialize(v) for k, v in obj.items()}

    # class types
    cls = type(obj)  # __class__
    module_name = get_module_name(obj)  # __module__.__qualname__ or __module__.__name__

    dct = {CLASSNAME: module_name, VERSION: getattr(cls, "__version__", DEFAULT_VERSION),}
    # _serializers[module_name] =

    # attr annotated
    if attr.has(cls):
        # Only include attributes which we can pass back to the classes constructor
        data = attr.asdict(cast(attr.AttrsInstance, obj), recurse=True, filter=lambda a, v: a.init)
        dct[DATA] = serialize(data)
        return dct

    # dataclasses
    if dataclasses.is_dataclass(cls):
        # fixme: unfortunately using asdict with nested dataclasses it looses information
        data = dataclasses.asdict(obj)  # type: ignore[call-overload]
        dct[DATA] = serialize(data)
        return dct

    # object / class brings their own
    if hasattr(obj, "serialize"):
        data = getattr(obj, "serialize")()
        if isinstance(data, dict):
            data = serialize(data)
        dct[DATA] = data
        return dct
    raise TypeError(f"cannot serialize object of type {cls}")


def deserialize(o):
    """
    Deserialize an object of primitive type and uses an allow list to determine if a class can be loaded.

    :param o: primitive to deserialize into an arbitrary object.
    :param full: if False it will return a stringified representation
                 of an object and will not load any classes
    :param type_hint: if set it will be used to help determine what
                 object to deserialize in. It does not override if another
                 specification is found
    :return: object
    """
    # None types remains None
    if o is None:
        return o
    # primitive types remains self
    if isinstance(o, _primitives):
        return o
    # iterator types for loops
    if isinstance(o, _builtin_collections):
        col = [deserialize(d) for d in o]
        if isinstance(o, tuple):
            return tuple(col)
        if isinstance(o, set):
            return set(col)
        if isinstance(o, frozenset):
            return frozenset(col)
        return col

    if not isinstance(o, dict):
        return o

    if CLASSNAME not in o:
        return {str(k): deserialize(v) for k, v in o.items()}


    # custom deserialization starts here
    cls: Any
    version = 0
    value: Any = None
    classname = ""

    if CLASSNAME in o:
        classname, value = o[CLASSNAME], o.get(DATA)
    cls = import_string(classname)
    # cls = import_string(classname)
    # return cls
    # print(cls)
    # attr or dataclass or pydantic.v1
    if attr.has(cls) or dataclasses.is_dataclass(cls):
        class_version = getattr(cls, "__version__", 0)
        if int(version) > class_version:
            raise TypeError(
                "serialized version of %s is newer than module version (%s > %s)",
                classname,
                version,
                class_version,
            )

        return cls(**deserialize(value))

    if not classname:
        raise TypeError("classname cannot be empty")

    # no deserializer available
    raise TypeError(f"No deserializer found for {classname}")


if __name__ == "__main__":
    from metagpt.provider.openai_api import CostManager
    # llm = LLM()
    cm = CostManager()
    deserialize(serialize(cm))
