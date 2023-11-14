#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/11 14:45
@Author  : alexanderwu
@File    : test_llm.py
"""

import pytest
import enum
from metagpt.llm import LLM
from metagpt.tools.serialization import serialize, deserialize
from metagpt.provider.openai_api import CostManager
from metagpt.config import Config
from metagpt.schema import AIMessage, Message, RawMessage, SystemMessage, UserMessage
from metagpt.actions.write_code import WriteCode


@pytest.fixture()
def llm():
    return LLM()




class TestSerDe:
    def test_ser_primitives(self):
        # i = 10
        # e = serialize(i)
        # assert i == e
        #
        # i = 10.1
        # e = serialize(i)
        # assert i == e
        #
        # i = "test"
        # e = serialize(i)
        # assert i == e
        #
        # i = True
        # e = serialize(i)
        # assert i == e
        #
        # Color = enum.IntEnum("Color", ["RED", "GREEN"])
        # i = Color.RED
        # e = serialize(i)
        # assert i == e
        """
        {'rpm': 10, 'llm': <module 'openai' from '/Users/rain/opt/anaconda3/envs/metagpt/lib/python3.9/site-packages/openai-0.27.8-py3.9.egg/openai/__init__.py'>,
        'model': 'gpt-4', 'auto_max_tokens': False, '_cost_manager': <metagpt.provider.openai_api.CostManager object at 0x12c6ec9d0>, 'last_call_time': 0, 'interval': 6.6}
        """
        # i = LLM()
        # i = CostManager()
        # i.update_cost(1, 2, 'gpt-4')
        # # print(i.__dict__)
        # x = serialize(i)
        # e = deserialize(x)
        # assert e==i
        # print(e)

        # i = Config()
        # s = serialize(i)
        # d = deserialize(s)
        # assert i == d

        i = Message(role='User', content='WTF')
        s = serialize(i)
        d = deserialize(s)
        assert i == d

        # i = WriteCode("write_code")
        # s = serialize(i)
        # d = deserialize(s)
        # assert i == d


    def test_ser_collections(self):
        i = [1, 2]
        e = deserialize(serialize(i))
        assert i == e

        i = ("a", "b", "a", "c")
        e = deserialize(serialize(i))
        assert i == e

        i = {2, 3}
        e = deserialize(serialize(i))
        assert i == e

        i = frozenset({6, 7})
        e = deserialize(serialize(i))
        assert i == e