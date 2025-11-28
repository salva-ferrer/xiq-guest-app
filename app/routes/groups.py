from fastapi import APIRouter,Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.services.xiq_client import XIQClient

templates=Jinja2Templates(directory='app/templates')
router=APIRouter(prefix='/groups')

@router.get('/', response_class=HTMLResponse)
def groups(request:Request):
    token=request.session.get('token')
    groups=XIQClient(token).list_groups()
    return templates.TemplateResponse('groups.html',{'request':request,'groups':groups})
