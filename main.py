import requests
import secrets
import time

base_url = "https://api.mail.gw"

def get_request_json(url, headers=None):
    r = requests.get(url, headers=headers)
    if r.status_code < 200 or r.status_code > 204:
        return None
    return r.json()

def post_request_json(url, body, headers=None):
    r = requests.post(url, json=body, headers=headers)
    if r.status_code < 200 or r.status_code > 204:
        return None
    return r.json()

def get_domains():
    data = get_request_json(base_url + "/domains")
    if data is None:
        return None
    return [domain["domain"] for domain in data["hydra:member"]]

def create_account(user, domain, password):
    data = post_request_json(base_url + "/accounts", {
        "address": user+"@"+domain, 
        "password": password
        }
    )
    return data

def get_token(address, password):
    data = post_request_json(base_url + "/token", {
        "address":address, 
        "password":password
        }
    )
    return data

def get_messages(auth_headers):
    data = get_request_json(base_url + "/messages", auth_headers)
    return data

def get_message(message_id, auth_headers):
    data = get_request_json(base_url + "/messages/" + message_id, headers=auth_headers)
    return data

domains = get_domains()
password = secrets.token_hex(16)
account = create_account(secrets.token_hex(8), domains[0], password)

address = account["address"]
print("account created: " + address + " (id: " + account["id"] + ")")
data = get_token(address, password)
token = data["token"]
headers = {"Authorization": "Bearer " + token}
print("Waiting for the email...")

waiting = True
while waiting:
    time.sleep(2)
    messages = get_messages(headers)
    for message in messages["hydra:member"]:
        print("Received email from " + message["from"]["address"] + " - subject: " + message["subject"] + " - text:\n")
        print(get_message(message["id"], headers)["html"])
        waiting = False