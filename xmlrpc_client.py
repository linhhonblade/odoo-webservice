import functools
import xmlrpc.client
HOST = 'localhost'
PORT = 8069
DB = 'database'
USER = 'hitomowoshi'
PASS = 'hitomowoshi'
ROOT = 'http://%s:%d/xmlrpc/' % (HOST, PORT)

# 1. Login
uid = xmlrpc.client.ServerProxy(ROOT + 'common').login(DB, USER, PASS)
print("Logged in as %s (uid: %d)" % (USER, uid))

call = functools.partial(xmlrpc.client.ServerProxy(
    ROOT + 'object').execute, DB, uid, PASS)

# 2. Read the sessions
sessions = call('openacademy.session', 'search_read', [], ['name', 'seats'])
for session in sessions:
    print("Session %s (%s seats)" % (session['name'], session['seats']))

# 3. Create a new session
session_id = call('openacademy.session', 'create', {
                  'name': 'Session from xmlrpc client', 'course_id': 1, })
print("Created new session sucessfully")
# 4. Create a new session for the Functional course
# course_id = call('openacademy.course', 'search', [
#                  ('name', 'ilike', 'Functional')])[0]
# session_id = call('openacademy.session', 'create', {
# 'name': 'Session for Functional course', 'course_id': course_id})
