from __future__ import annotations

import asyncio

from quantpilot_market_data import cli


def test_compatible_event_loop_factory_returns_selector_loop() -> None:
    loop = cli.compatible_event_loop_factory()
    try:
        assert isinstance(loop, asyncio.SelectorEventLoop)
    finally:
        loop.close()


def test_main_uses_selector_loop_factory_on_windows(monkeypatch) -> None:
    captured: dict[str, object] = {}

    monkeypatch.setattr(cli.sys, "platform", "win32")
    monkeypatch.setattr(
        cli.uvicorn, "run", lambda app, **kwargs: captured.update(app=app, **kwargs)
    )
    monkeypatch.setenv("QUANTPILOT_MARKET_HOST", "127.0.0.2")
    monkeypatch.setenv("QUANTPILOT_MARKET_PORT", "8123")
    monkeypatch.setenv("QUANTPILOT_MARKET_RELOAD", "1")

    cli.main()

    assert captured == {
        "app": "quantpilot_market_data.api:app",
        "host": "127.0.0.2",
        "port": 8123,
        "loop": cli.compatible_event_loop_factory,
        "reload": True,
    }
