import csv, os
MAP='data/user_mail_map.csv'
class UserMailAssoc:
    def __init__(self): 
        if not os.path.exists(MAP):
            with open(MAP,'w',newline='') as f: csv.writer(f).writerow(["app_user","mail_config_id"])
    def get(self,u):
        with open(MAP) as f:
            for r in csv.DictReader(f):
                if r["app_user"]==u: return r["mail_config_id"]
