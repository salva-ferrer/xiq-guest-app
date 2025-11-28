import requests

BASE = 'https://api.extremecloudiq.com'


class UnauthorizedError(Exception):
    """Raised when the XIQ API rejects the current token."""


class XIQClient:
    def __init__(self, token=None):
        self.token = token

    def headers(self):
        return {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

    def _raise_for_auth(self, response):
        if response.status_code in (401, 403):
            raise UnauthorizedError()

    def login(self, u, p):
        r = requests.post(f"{BASE}/login", json={"username": u, "password": p})
        if r.status_code == 200:
            self.token = r.json().get("access_token")
            return True
        return False

    def list_groups(self):
        r = requests.get(f"{BASE}/usergroups", headers=self.headers())
        self._raise_for_auth(r)
        return r.json().get("data", [])

    def list_users(self):
        r = requests.get(f"{BASE}/endusers", headers=self.headers())
        self._raise_for_auth(r)
        return r.json().get("data", [])

    def create_user(self, p):
        r = requests.post(f"{BASE}/endusers", json=p, headers=self.headers())
        self._raise_for_auth(r)
        if r.status_code in (200, 201):
            return r.json()
        print("Create error:", r.status_code, r.text)
        return None

    def delete_user(self, id):
        r = requests.delete(f"{BASE}/endusers/{id}", headers=self.headers())
        self._raise_for_auth(r)
