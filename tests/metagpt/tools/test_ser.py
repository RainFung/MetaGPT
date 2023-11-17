#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Desc   : the unittests of metagpt/memory/memory_storage.py

from typing import List

from metagpt.memory.memory_storage import MemoryStorage
from metagpt.schema import Message
from metagpt.actions import BossRequirement
from metagpt.actions import WritePRD
from metagpt.actions.action_output import ActionOutput
from metagpt.tools.ser import serialize, deserialize
from metagpt.actions import Action, WritePRD, WriteTest, WriteCode
from metagpt.provider.openai_api import CostManager, OpenAIGPTAPI
from metagpt.llm import LLM
from metagpt.logs import logger
import pytest
import asyncio



# def test_idea_message():
#     api_design = "设计一个名为'add'的函数，该函数接受两个整数作为输入，并返回它们的和。"
#     write_code = WriteCode(name="write_code")
#
#     code = asyncio.run(write_code.run(api_design, filename='ser.py'))
#     logger.info(serialize(write_code))

# @pytest.mark.asyncio
# async
def test_idea_message():
    # msg = Message(role='User', content='WTF')
    # s = serialize(msg)
    # i = deserialize(s)
    # assert msg == i
    #
    # c = CostManager()
    # c.update_cost(1, 2, "gpt-4")
    # s = serialize(c)
    # i = deserialize(s)
    # assert c == i

    c = LLM()
    s = serialize(c)
    logger.info(s)

    #
    c = Action()
    # s = serialize(c)
    # i = deserialize(s)
    # assert c == i


    # api_design = "设计一个名为'add'的函数，该函数接受两个整数作为输入，并返回它们的和。"
    # write_code = WriteCode(name="write_code")
    #
    # code = await write_code.run(api_design)
    # print(code)
    # print(serialize(write_code))

    # api_design = "设计一个名为'add'的函数，该函数接受两个整数作为输入，并返回它们的和。"
    # c = WriteCode(name="write_code", context=api_design)
    # code = await c.run(api_design)
    # logger.info(code)

    # 我们不能精确地预测生成的代码，但我们可以检查某些关键字
    # assert 'def add' in code
    # assert 'return' in code
    #
    # s = serialize(c)
    # i = deserialize(s)
    # assert c == i
