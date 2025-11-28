import json
import os
from functools import lru_cache
from typing import Dict, Iterable

from fastapi.templating import Jinja2Templates
from jinja2 import pass_context
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOCALES_DIR = os.path.join(BASE_DIR, "locales")
DEFAULT_LOCALE = "en"
LOCALE_COOKIE = "locale"


def _available_locales() -> Iterable[str]:
    if not os.path.isdir(LOCALES_DIR):
        return []
    for filename in os.listdir(LOCALES_DIR):
        if filename.endswith(".json"):
            yield os.path.splitext(filename)[0]


AVAILABLE_LOCALES = set(_available_locales()) or {DEFAULT_LOCALE}


@lru_cache(maxsize=16)
def load_translations(locale: str) -> Dict[str, str]:
    locale_name = locale if locale in AVAILABLE_LOCALES else DEFAULT_LOCALE
    path = os.path.join(LOCALES_DIR, f"{locale_name}.json")
    if not os.path.exists(path):
        path = os.path.join(LOCALES_DIR, f"{DEFAULT_LOCALE}.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_accept_language(header_value: str) -> Iterable[str]:
    if not header_value:
        return []
    for item in header_value.split(","):
        locale_part = item.split(";")[0].strip()
        if locale_part:
            yield locale_part.split("-")[0]


def detect_locale(request: Request) -> str:
    cookie_locale = request.cookies.get(LOCALE_COOKIE)
    if cookie_locale in AVAILABLE_LOCALES:
        return cookie_locale
    for locale in parse_accept_language(request.headers.get("accept-language")):
        if locale in AVAILABLE_LOCALES:
            return locale
    return DEFAULT_LOCALE


@pass_context
def translate(context, key: str) -> str:
    request: Request = context.get("request")
    translations = getattr(request.state, "translations", {}) if request else {}
    return translations.get(key, key)


templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
templates.env.globals["t"] = translate
templates.env.globals["available_locales"] = sorted(AVAILABLE_LOCALES)


class LocalizationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        locale = detect_locale(request)
        request.state.locale = locale
        request.state.translations = load_translations(locale)
        response = await call_next(request)
        return response
