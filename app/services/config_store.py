import json
CONFIG_PATH='data/mail_configs.json'
class ConfigStore:
    def _load(self): return json.load(open(CONFIG_PATH))
    def get(self,id):
        for c in self._load():
            if c['id']==id: return c
    def get_default(self):
        items=self._load()
        for c in items:
            if c.get("is_default"): return c
        return items[0] if items else None
