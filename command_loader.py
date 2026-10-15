"""Automatically load every Python command module from ./commands."""
import importlib.util
import logging
from pathlib import Path

log = logging.getLogger(__name__)
COMMANDS_DIR = Path(__file__).resolve().parent / "commands"


async def load_commands(bot) -> None:
    COMMANDS_DIR.mkdir(parents=True, exist_ok=True)
    loaded = 0

    for file_path in sorted(COMMANDS_DIR.glob("*.py")):
        if file_path.name.startswith("_"):
            continue

        module_name = f"lxcky_command_{file_path.stem}"
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None or spec.loader is None:
            log.warning("Skipped command file with no import loader: %s", file_path.name)
            continue

        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
            setup = getattr(module, "setup", None)
            if setup is None:
                log.warning("Skipped %s: expected an async setup(bot) function", file_path.name)
                continue
            await setup(bot)
            loaded += 1
            log.info("Loaded command module: %s", file_path.name)
        except Exception:
            log.exception("Failed to load command module: %s", file_path.name)

    log.info("Loaded %s command module(s)", loaded)
