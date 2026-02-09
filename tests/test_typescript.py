"""Tests for the TypeScript formatters."""

from __future__ import annotations

import re
from textwrap import dedent
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pytest
    from markdown import Markdown


def test_output_markdown(md: Markdown) -> None:
    """Assert Markdown is converted to HTML.

    Parameters:
        md: A Markdown instance (fixture).
    """
    html = md.convert(
        dedent(
            """
            ```typescript exec="yes"
            console.log("**Bold!**")
            ```
            """,
        ),
    )
    assert html == "<p><strong>Bold!</strong></p>"


def test_output_html(md: Markdown) -> None:
    """Assert HTML is injected as is.

    Parameters:
        md: A Markdown instance (fixture).
    """
    html = md.convert(
        dedent(
            """
            ```typescript exec="yes" html="yes"
            console.log("**Bold!**")
            ```
            """,
        ),
    )
    assert html == "<p>**Bold!**\n</p>"


def test_error_raised(md: Markdown, caplog: pytest.LogCaptureFixture) -> None:
    """Assert errors properly log a warning and return a formatted traceback.

    Parameters:
        md: A Markdown instance (fixture).
        caplog: Pytest fixture to capture logs.
    """
    html = md.convert(
        dedent(
            """
            ```typescript exec="yes"
            throw new Error("oh no!")
            ```
            """,
        ),
    )
    assert "error:" in html
    assert "oh no!" in html


def test_can_print_non_string_objects(md: Markdown) -> None:
    """Assert we can print non-string objects.

    Parameters:
        md: A Markdown instance (fixture).
    """
    html = md.convert(
        dedent(
            """
            ```typescript exec="yes"
            class NonString {
                toString() {
                    return "string";
                }
            }

            const nonstring = new NonString();
            console.log(nonstring.toString(), nonstring.toString());
            ```
            """,
        ),
    )
    assert "error:" not in html


def test_removing_output_from_typescript_code(md: Markdown) -> None:
    """Assert output lines are removed from pycon snippets.

    Parameters:
        md: A Markdown instance (fixture).
    """
    html = md.convert(
        dedent(
            """
            ```typescript exec="1" source="console"
            >>> console.log("ok")
            ok
            ```
            """,
        ),
    )
    assert "ok" in html
    assert "ko" not in html


def test_functions_have_a_module_attribute(md: Markdown) -> None:
    """Assert functions have a `__module__` attribute.

    Parameters:
        md: A Markdown instance (fixture).
    """
    html = md.convert(
        dedent(
            """
            ```typescript exec="1"
            function func() {}

            console.log(`${func.name}`);
            ```
            """,
        ),
    )
    assert "func" in html
