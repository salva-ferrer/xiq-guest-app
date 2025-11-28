from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse

from app.i18n import AVAILABLE_LOCALES, DEFAULT_LOCALE, LOCALE_COOKIE

router = APIRouter()


@router.post("/set-locale")
def set_locale(request: Request, locale: str = Form(DEFAULT_LOCALE), next: str = Form("/")):
    locale_value = locale if locale in AVAILABLE_LOCALES else DEFAULT_LOCALE
    next_url = next or request.headers.get("referer") or "/"
    response = RedirectResponse(next_url, status_code=303)
    response.set_cookie(LOCALE_COOKIE, locale_value, max_age=60 * 60 * 24 * 365, path="/")
    request.state.locale = locale_value
    return response
