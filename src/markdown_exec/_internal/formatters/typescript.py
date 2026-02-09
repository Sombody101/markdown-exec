# Formatter for executing TypeScript code.

from __future__ import annotations

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
        ["bun", "run", "-"],
        input=code,
        cwd=project_root,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if process.returncode != 0:
        _logger.error(f"TypeScript execution failed: {process.stderr}")
        return f"<code>Error:\n{process.stderr}</code>"
    return process.stdout


def _format_typescript(**kwargs: Any) -> str:
    return base_format(language="typescript", run=_run_typescript, **kwargs)


# def _format_typescript(code, **kwargs) -> str:
#     output = _run_typescript(code, **kwargs)
#
#     if kwargs.get("output") == "markdown":
#         return output
#
#     return f"```typescript\n{output}\n```"
