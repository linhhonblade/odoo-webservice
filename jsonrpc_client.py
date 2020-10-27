import json
import random
import urllib.request

HOST = 'localhost'
PORT = 8069
DB = 'database'
USER = 'hitomowoshi'
PASS = 'hitomowoshi'


def json_rpc(url, method, params):
    data = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": random.randint(0, 1000000000),
    }
    req = urllib.request.Request(url=url, data=json.dumps(
        data).encode(), headers={"Content-Type": "application/json", })
    reply = json.loads(urllib.request.urlopen(req).read().decode('UTF-8'))
    if reply.get("error"):
        raise Exception(reply["error"])
    return reply["result"]


def call(url, service, method, *args):
    return json_rpc(url, "call", {"service": service, "method": method, "args": args})


# Login the given database
url = "http://%s:%d/jsonrpc" % (HOST, PORT)
uid = call(url, "common", "login", DB, USER, PASS)
print("Logged in as %s (uid: %d)" % (USER, uid))

# Create a new session
# args = {
#     'name': 'Session from jsonrpc client',
#     'course_id': 1,
# }
# session_id = call(url, "object", "execute", DB, uid, PASS,
#                   'openacademy.session', 'create', args)
# print("Created new session sucessfully")

# Read the sessions
sessions = call(url, "object", "execute", DB, uid, PASS,
                'openacademy.session', 'search_read', [], ['name', 'seats'])
for session in sessions:
    print("Session %s (%s seats)" % (session['name'], session['seats']))
