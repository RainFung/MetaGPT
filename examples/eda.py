#!/usr/bin/env python

import asyncio

from metagpt.actions.data_process import DataAnalyse


async def main():
    file_path = "../tests/data/data_for_test.csv"
    context = "Analyze loans for different age groups?"
    role = DataAnalyse()
    await role.run(context, file_path)


if __name__ == '__main__':
    asyncio.run(main())
