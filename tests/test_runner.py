from src.runner import _execute_runner, Arguments


def test_runner():
    args = Arguments(
        exec_command="ping 100.200.100.200 -n 1 -w 1000",
        output_file_path=None,
        period_seconds=1
    )

    _execute_runner(args)
