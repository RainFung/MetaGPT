#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import shutil
from collections import OrderedDict
from pathlib import Path

from metagpt.const import WORKSPACE_ROOT
from metagpt.logs import logger
from metagpt.roles import Role
from metagpt.actions import DataProcess
from metagpt.schema import Message
from metagpt.utils.common import CodeParser
from metagpt.utils.special_tokens import MSG_SEP, FILENAME_CODE_SEP


class DataAnalyst(Role):
    def __init__(
            self,
            name: str = "rain",
            profile: str = "DataAnalyst",
            goal: str = "Process and analyze data to obtain information",
            constraints: str = "Accuracy of data conclusions",
    ):
        super().__init__(name, profile, goal, constraints)
        self._init_actions([DataProcess(name)])
        # how to use watch
        # self._watch([WriteDesign])

