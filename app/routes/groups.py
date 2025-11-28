from fastapi import APIRouter,Request
from fastapi.responses import HTMLResponse
from app.services.xiq_client import XIQClient, UnauthorizedError
from app.i18n import templates
router=APIRouter(prefix='/groups')

@router.get('/', response_class=HTMLResponse)
def groups(request:Request):
    token=request.session.get('token')
    if not token:
        from fastapi.responses import RedirectResponse
        return RedirectResponse('/login', status_code=303)
    client = XIQClient(token)
    try:
        groups=client.list_groups()
    except UnauthorizedError:
        request.session.clear()
        from fastapi.responses import RedirectResponse
        return RedirectResponse('/login', status_code=303)

    return templates.TemplateResponse('groups.html',{'request':request,'groups':groups})
