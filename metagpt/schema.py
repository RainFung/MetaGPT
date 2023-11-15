#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/8 22:12
@Author  : alexanderwu
@File    : schema.py
"""
from __future__ import annotations

from dataclasses import dataclass, Field
from typing import Type, TypedDict

from pydantic import BaseModel, Field

from metagpt.logs import logger


class RawMessage(TypedDict):
    content: str
    role: str


class Message(BaseModel):
    """list[<role>: <content>]"""
    content: str
    instruct_content: BaseModel = Field(default=None)
    role: str = Field(default='user')  # system / user / assistant
    cause_by: Type["Action"] = Field(default="")
    sent_from: str = Field(default="")
    send_to: str = Field(default="")
    restricted_to: str = Field(default="")

    def __str__(self):
        # prefix = '-'.join([self.role, str(self.cause_by)])
        return f"{self.role}: {self.content}"

    def __repr__(self):
        return self.__str__()

    def to_dict(self) -> dict:
        return {
            "role": self.role,
            "content": self.content
        }


class UserMessage(Message):
    """便于支持OpenAI的消息
       Facilitate support for OpenAI messages
    """



class SystemMessage(Message):
    """便于支持OpenAI的消息
       Facilitate support for OpenAI messages
    """


class AIMessage(Message):
    """便于支持OpenAI的消息
       Facilitate support for OpenAI messages
    """


if __name__ == '__main__':
    test_content = 'test_message'
    msgs = [
        UserMessage(content=test_content),
        SystemMessage(content=test_content),
        AIMessage(content=test_content),
        Message(content=test_content, role='QA')
    ]
    logger.info(msgs)
