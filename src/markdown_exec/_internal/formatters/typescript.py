# Formatter for executing TypeScript code.

from __future__ import annotations

from typing import Any

import sys
import os
import subprocess
from markdown_exec._internal.logger import get_logger
from markdown_exec._internal.formatters.base import base_format

_logger = get_logger(__name__)


def _run_typescript(
    code: str,
    returncode: int | None = None,  # noqa: ARG001
    session: str | None = None,
    id: str | None = None,  # noqa: A002
    **extra: str,
) -> str:
    if session:
        _logger.warn(
            "Sessions have not been implemented for TypeScript. The block will fail if scoped definitions defined in other blocks are referenced."
        )
    project_root = os.getcwd()
    prelude_path = os.path.join(project_root, "mexec-prelude.ts")
    if os.path.exists(prelude_path):
        code = f'import "{prelude_path}";\n{code}'

    process = subprocess.run(
        ["bun", "--silent", "run", "-"],
        input=code,
        cwd=project_root,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    
    _handle_process_logs(process)
    
    if process.returncode != 0:
        _logger.error(f"TypeScript execution failed: {process.stderr}")
        return f"```typescript\n{process.stderr}\n```"
    return process.stdout


def _handle_process_logs(process):
    if process.stderr:
        for line in process.stderr.splitlines():
            if line.startswith("[LOG:"):
                try:
                    header, msg = line.split("]", 1)
                    level = header.replace("[LOG:", "").strip()
                    
                    if level == "WARN":
                        _logger.warning(f"TS,WRN: {msg.strip()}")
                    elif level == "ERROR":
                        _logger.error(f"TS,ERR: {msg.strip()}")
                    else:
                        _logger.info(f"TS,INF: {msg.strip()}")
                except ValueError:
                    print(f"TS stderr: {line}", file=sys.stderr)
            else:
                print(line, file=sys.stderr)

def _format_typescript(**kwargs: Any) -> str:
    return base_format(language="typescript", run=_run_typescript, **kwargs)