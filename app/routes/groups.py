from fastapi import APIRouter,Request
from fastapi.responses import HTMLResponse
from app.services.xiq_client import XIQClient
from app.i18n import templates
router=APIRouter(prefix='/groups')

@router.get('/', response_class=HTMLResponse)
def groups(request:Request):
    token=request.session.get('token')
    groups=XIQClient(token).list_groups()
    return templates.TemplateResponse('groups.html',{'request':request,'groups':groups})
