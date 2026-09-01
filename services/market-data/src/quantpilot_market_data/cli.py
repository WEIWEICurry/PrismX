from __future__ import annotations

import asyncio
import os
import sys

import uvicorn


def compatible_event_loop_factory() -> asyncio.AbstractEventLoop:
    return asyncio.SelectorEventLoop()


def main() -> None:
    host = os.getenv("QUANTPILOT_MARKET_HOST", "127.0.0.1")
    port = int(os.getenv("QUANTPILOT_MARKET_PORT", "8000"))
    uvicorn.run(
        "quantpilot_market_data.api:app",
        host=host,
        port=port,
        loop=compatible_event_loop_factory if sys.platform == "win32" else "auto",
        reload=os.getenv("QUANTPILOT_MARKET_RELOAD", "0") == "1",
    )


if __name__ == "__main__":
    main()
