import smtplib, ssl
from email.message import EmailMessage
import logging, traceback

logger=logging.getLogger("smtp_mailer")
logger.setLevel(logging.DEBUG)
h=logging.StreamHandler()
h.setFormatter(logging.Formatter("[SMTP] %(levelname)s: %(message)s"))
logger.addHandler(h)

def send_email(cfg,to,subject,text):
    logger.debug(f"Preparing email to {to} via {cfg['host']}:{cfg['port']}")
    msg=EmailMessage()
    msg["From"]=f"{cfg['from_name']} <{cfg['from_email']}>"
    msg["To"]=to; msg["Subject"]=subject
    msg.set_content(text)
    ctx=ssl.create_default_context()
    try:
        with smtplib.SMTP(cfg['host'], cfg['port'], timeout=10) as s:
            s.set_debuglevel(1)
            if cfg.get("use_tls",True): s.starttls(context=ctx)
            if cfg.get("username"): s.login(cfg['username'], cfg['password'])
            s.send_message(msg)
        logger.info("Email sent OK")
        return True
    except Exception:
        logger.error("Error sending email:")
        logger.error(traceback.format_exc())
        return False
