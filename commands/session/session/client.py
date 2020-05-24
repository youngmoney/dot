import requests
from .session import Session
import locale

class RemoteSession(Session):
    def __init__(self, session_id, url=None, port=7007):
        partial_url = 'http://%s:%s/session/id/%s/' % (url, str(port), session_id)
        self._url_for_verb = lambda v: partial_url + v

    def start(self):
        response = requests.get(self._url_for_verb('start'))
        return response.status_code == 200

    def stop(self):
        response = requests.get(self._url_for_verb('stop'))
        return response.status_code == 200

    def kill(self):
        response = requests.get(self._url_for_verb('kill'))
        return response.status_code == 200

    def execute(self, command, auto_start=False):
        if auto_start:
            self.start()

        data = {'command': '\n'.join(command)}
        response = requests.put(self._url_for_verb('execute'), data=data)
        if response.content:
            return response.content.decode(locale.getpreferredencoding(False)).split('\n')
        return []

    def is_running(self):
        True
