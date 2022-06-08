import argparse
import asyncio
import os
import platform
import sys
from asyncio import subprocess, Task
from dataclasses import dataclass
from typing import Optional


@dataclass
class Arguments:
    exec_command: str
    output_file_path: Optional[str]
    period_seconds: int


@dataclass
class MonitorStats:
    cpu_percent: int
    memory_bytes: int
    handles_descriptors: int

    def to_csv(self) -> str:
        return f"{self.cpu_percent},{self.memory_bytes},{self.handles_descriptors}\n"


def run_runner():
    arguments = _parse_arguments()
    _execute_runner(arguments)


def _parse_arguments():
    parser = argparse.ArgumentParser(description='Executes an command and collects usage data to a CSV')
    parser.add_argument(
        "--file",
        type=str,
        required=False,
        help='output csv file path (if not set, stdout is used instead)'
    )

    parser.add_argument(
        "--exec",
        type=str,
        required=True,
        help="command to execute"
    )

    parser.add_argument(
        "--period",
        type=int,
        required=True,
        help="measurement period in seconds"
    )

    args = parser.parse_args()
    return Arguments(
        exec_command=args.exec,
        output_file_path=args.file,
        period_seconds=args.period
    )


def _execute_runner(arguments: Arguments):
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(
            asyncio.WindowsProactorEventLoopPolicy()
        )

    loop = asyncio.new_event_loop()
    loop.run_until_complete(
        _async_execute_runner(arguments)
    )


async def _async_execute_runner(arguments: Arguments):
    monitor_task = asyncio.create_task(
        _run_monitor(arguments.output_file_path, arguments.period_seconds)
    )
    await _run_process(arguments.exec_command)
    await _cancel_task(monitor_task)


async def _cancel_task(task: Task):
    async def is_task_cancelled():
        return task.cancelled()

    task.cancel()

    await asyncio.wait_for(is_task_cancelled(), 3)


async def _run_process(exec_command: str):
    process = await subprocess.create_subprocess_shell(
        exec_command
    )

    await process.wait()


async def _run_monitor(output_file_path: Optional[str], period_seconds: int):
    if output_file_path:
        with open(output_file_path, "w") as file:
            await _run_monitor_loop(file, period_seconds)
    else:
        await _run_monitor_loop(sys.stdout, period_seconds)


async def _run_monitor_loop(file, period_seconds: int):
    while True:
        data = await _collect_data()
        file.write(data.to_csv())
        file.flush()
        await asyncio.sleep(period_seconds)


async def _collect_data() -> MonitorStats:
    if platform.system() == "Linux":
        return await _collect_data_linux()
    elif platform.system() == "Windows":
        return await _collect_data_windows()
    else:
        raise EnvironmentError("Unsupported platform")


async def _collect_data_linux() -> MonitorStats:
    cpu = await _query_shell("uptime | tr -d ',' | awk '{print $8 * 100}'")
    mem = await _query_shell("free | grep Mem | awk '{print $3}'")
    fds = await _query_shell("lsof | wc -l &> /dev/null")

    return MonitorStats(
        cpu_percent=cpu,
        memory_bytes=mem,
        handles_descriptors=fds,
    )


async def _query_shell(cmd: str) -> int:
    proc = await subprocess.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.DEVNULL
    )
    raw_value = await proc.stdout.readline()

    return int(raw_value.decode("ascii").strip())


async def _collect_data_windows() -> MonitorStats:
    cpu = await _query_wmic("cpu get loadpercentage")
    mem = await _query_wmic("os get freephysicalmemory")
    handles = await _query_wmic("process get handlecount", sum_multiple_values=True)

    return MonitorStats(
        cpu_percent=cpu,
        memory_bytes=mem,
        handles_descriptors=handles,
    )


async def _query_wmic(query: str, *, sum_multiple_values: bool = False) -> int:
    proc = await subprocess.create_subprocess_shell(
        f"wmic {query}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.DEVNULL
    )

    _ = await proc.stdout.readline()

    if sum_multiple_values:
        value = 0

        while True:
            raw_value = await proc.stdout.readline()
            str_value = raw_value.decode("ascii").strip()
            if not str_value.isnumeric():
                break

            value += int(str_value)
    else:
        raw_value = await proc.stdout.readline()
        value = int(raw_value.decode("ascii").strip())

    return value

