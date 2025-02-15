import json

import requests


def clear_sessions(session_id=None):
    """
    Here we query and delete orphan sessions
    docs: https://www.selenium.dev/documentation/grid/advanced_features/endpoints/
    :return: None
    """
    url = "http://127.0.0.1:4444"
    if not session_id:
        # delete all sessions
        r = requests.get("{}/status".format(url))
        data = json.loads(r.text)
        for node in data["value"]["nodes"]:
            for slot in node["slots"]:
                if slot["session"]:
                    id = slot["session"]["sessionId"]
                    r = requests.delete("{}/session/{}".format(url, id))
    else:
        # delete session from params
        r = requests.delete("{}/session/{}".format(url, session_id))
