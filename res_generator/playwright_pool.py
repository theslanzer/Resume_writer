# playwright_pool.py
from pathlib import Path
from playwright.sync_api import sync_playwright, Browser, Page, Playwright

class _BrowserPool:
    _ctx: Playwright | None = None     # type hints help the checker
    _browser: Browser | None = None

    @classmethod
    def page(cls) -> Page:
        if cls._browser is None:
            cls._ctx = sync_playwright().start()
            cls._browser = cls._ctx.chromium.launch()
        return cls._browser.new_page()

    @classmethod
    def close(cls) -> None:
        if cls._browser is not None:
            cls._browser.close()
            cls._browser = None
        if cls._ctx is not None:       # ✅ guard before .stop()
            cls._ctx.stop()
            cls._ctx = None
