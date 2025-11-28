from fastapi import APIRouter,Request,Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from app.services.xiq_client import XIQClient

templates=Jinja2Templates(directory='app/templates')
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
    return templates.TemplateResponse('login.html',{'request':request,'error':'Login failed'})
