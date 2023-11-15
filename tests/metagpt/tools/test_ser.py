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
from metagpt.actions import Action, WritePRD, WriteTest
from metagpt.provider.openai_api import CostManager, OpenAIGPTAPI
from metagpt.llm import LLM

def test_idea_message():
    # msg = Message(role='User', content='WTF')
    # s = serialize(msg)
    # print(s)
    # i = deserialize(s)
    # print(i)
    # assert msg == i


    # idea = 'Write a cli snake game'
    # role_id = 'UTUser1(Product Manager)'
    # message = Message(role='BOSS', content=idea, cause_by=BossRequirement)
    # print(serialize(message))

    c = CostManager()
    s = serialize(c)
    i = deserialize(s)
    assert c == i

    c = Action()
    s = serialize(c)
    i = deserialize(s)
    assert c == i
