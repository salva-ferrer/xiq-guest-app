from fastapi import APIRouter,Request,Form
from fastapi.responses import HTMLResponse, RedirectResponse
from app.services.xiq_client import XIQClient
from app.i18n import templates
router=APIRouter()

@router.get('/login', response_class=HTMLResponse)
def form(request:Request):
    return templates.TemplateResponse('login.html',{'request':request})

@router.post('/login')
def login(request:Request, username:str=Form(...), password:str=Form(...)):
    c=XIQClient()
    if c.login(username,password):
        request.session['token']=c.token
        request.session['app_user']=username
        return RedirectResponse('/',303)
    return templates.TemplateResponse('login.html',{'request':request,'error_key':'login_failed'})
