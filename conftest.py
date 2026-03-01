import sys
from pathlib import Path


def pytest_configure(config):
    root = Path(__file__).parent
    cwd = Path.cwd()

    # Running pytest from inside a day-NN folder (most common case)
    if cwd.name.startswith("day-") and cwd.parent == root:
        _add(str(cwd))
        _add(str(cwd / "src"))
        return

    # Running pytest from the project root with explicit day-NN paths
    for arg in config.args:
        arg_path = Path(arg) if Path(arg).is_absolute() else cwd / arg
        for parent in [arg_path, *arg_path.parents]:
            if parent.name.startswith("day-") and parent.parent == root:
                _add(str(parent))
                _add(str(parent / "src"))
                break


def _add(path: str) -> None:
    if path not in sys.path:
        sys.path.insert(0, path)
