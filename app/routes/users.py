from fastapi import APIRouter,Request,Form
from fastapi.responses import HTMLResponse, RedirectResponse
from app.services.xiq_client import XIQClient
from app.services.user_assoc import UserMailAssoc
from app.services.config_store import ConfigStore
from app.services.smtp_mailer import send_email
from app.utils.generate_password import generate_password
from app.i18n import templates
router=APIRouter(prefix='/users')

@router.get('/', response_class=HTMLResponse)
def list_users(request:Request):
    token=request.session.get('token')
    users=XIQClient(token).list_users()
    return templates.TemplateResponse('users.html',{'request':request,'users':users})

@router.get('/create', response_class=HTMLResponse)
def form(request:Request):
    token=request.session.get('token')
    groups=XIQClient(token).list_groups()
    return templates.TemplateResponse('create_user.html',{'request':request,'groups':groups})

@router.post('/create')
def create(request:Request,
           user_group_id:int=Form(...),
           user_name:str=Form(...),
           name:str=Form(""),
           email_address:str=Form(""),
           phone_number:str=Form(""),
           password_choice:str=Form("auto"),
           password_manual:str=Form(""),
           send_email_flag:str=Form("no")):

    token=request.session.get('token')
    app_user=request.session.get('app_user')
    assoc=UserMailAssoc()
    cfg_id=assoc.get(app_user)
    store=ConfigStore()
    cfg=store.get(cfg_id) if cfg_id else store.get_default()
    client=XIQClient(token)
    password = generate_password() if password_choice=="auto" else password_manual
    payload={
        "user_group_id": user_group_id,
        "user_name": user_name,
        "name": name or None,
        "email_address": email_address or None,
        "phone_number": phone_number or None,
        "password": password,
        "email_password_delivery": email_address or None,
        "sms_password_delivery": phone_number or None
    }

    user=client.create_user(payload)

    if user and cfg and email_address and send_email_flag=="yes":
        text=f"Hello {user_name},\n\nYour account was created.\nUser: {user_name}\nPass: {password}\n"
        send_email(cfg, email_address, "Your credentials", text)

    return RedirectResponse('/users',303)

@router.post('/delete')
def delete(request:Request,user_id:str=Form(...)):
    token=request.session.get('token')
    XIQClient(token).delete_user(user_id)
    return RedirectResponse('/users',303)
