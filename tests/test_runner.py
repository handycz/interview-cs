from src.runner import _execute_runner, Arguments


def test_runner():
    args = Arguments(
        exec_command="sleep 2",
        output_file_path=None,
        period_seconds=1
    )

    _execute_runner(args)
