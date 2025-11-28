from fastapi import APIRouter,Request
from app.services.smtp_mailer import send_email
from app.services.config_store import ConfigStore
from app.services.user_assoc import UserMailAssoc

router=APIRouter(prefix='/test_smtp')

@router.get('/')
def test(request:Request):
    app_user=request.session.get('app_user')
    if not app_user: return {"error":"not logged in"}

    assoc=UserMailAssoc()
    cfg_id=assoc.get(app_user)
    store=ConfigStore()
    cfg=store.get(cfg_id) if cfg_id else store.get_default()

    if not cfg: return {"error":"no smtp config"}

    ok=send_email(cfg, cfg['from_email'], "SMTP Test", "This is a test.")
    return {"result":"success" if ok else "failure"}
