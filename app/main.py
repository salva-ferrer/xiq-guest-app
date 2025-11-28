import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from fastapi.responses import HTMLResponse
from app.routes import auth, users, smtp_test, groups, locale
from app.i18n import LocalizationMiddleware, templates

BASE=os.path.dirname(os.path.abspath(__file__))
app=FastAPI()
app.add_middleware(SessionMiddleware, secret_key="x")
app.add_middleware(LocalizationMiddleware)

app.mount('/static', StaticFiles(directory=os.path.join(BASE,'static')), name='static')
app.include_router(auth.router)
app.include_router(groups.router)
app.include_router(users.router)
app.include_router(smtp_test.router)
app.include_router(locale.router)

@app.get('/', response_class=HTMLResponse)
def dash(request:Request):
    """Redirect unauthenticated users to login before showing the dashboard."""
    if not request.session.get('token'):
        from fastapi.responses import RedirectResponse
        return RedirectResponse('/login')
    return templates.TemplateResponse('dashboard.html', {'request':request})
