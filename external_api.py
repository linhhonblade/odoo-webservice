import xmlrpc.client

info = xmlrpc.client.ServerProxy('https://demo.odoo.com/start').start()
url, db, username, password = info['host'], info['database'], info['user'], info['password']
print(info)

# =====================================================
# CONNECTION
# =====================================================

# Login
# The xmlrpc/2/common endpoint provides meta-calls
# which don’t require authentication
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))

# To verify if the connection information is correct before
# trying to authenticate, the simplest call is to ask for the server’s version
common.version()

# The authentication itself is done through the authenticate function
# and returns a user identifier (uid) used in authenticated calls
# instead of the login.
uid = common.authenticate(db, username, password, {})

# ====================================================
# CALLING METHOD
# ====================================================

# The second endpoint is xmlrpc/2/object
# is used to call methods of odoo models via the execute_kw RPC function
# which takes following parameters:
#   string: database to use
#   int: user id (retrieve through authenticate)
#   string: user password
#   string: model name
#   string: method name
#   array/list: params passed by position
#   mapping/dict: params passed by keyword (optional)
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
models.execute_kw(db, uid, password, 'res.partner', 'check_access_rights', [
                  'read'], {'raise_exception': False})

# List records
# search() takes a mandatory domain filter (possibly empty),
# and returns the database identifiers of all
# records matching the filter.
models.execute_kw(db, uid, password, 'res.partner',
                  'search', [[['is_company', '=', True]]])
# offset and limit parameters are available to
# only retrieve a subset of all matched records.
models.execute_kw(db, uid, password, 'res.partner', 'search', [
                  [['is_company', '=', True]]], {'offset': 10, 'limit': 5})

# Count records
# search_count() can be used to retrieve only the
# number of records matching the query
models.execute_kw(db, uid, password, 'res.partner',
                  'search_count', [[['is_company', '=', True]]])

# Read records
# Record data is accessible via the read() method,
# which takes a list of ids (as returned by search())
# and optionally a list of fields to fetch.
ids = models.execute_kw(db, uid, password, 'res.partner', 'search', [
                        [['is_company', '=', True]]], {'limit': 1})
[record] = models.execute_kw(db, uid, password, 'res.partner', 'read', [ids])
# count the number of fields fetched
len(record)
# Fetch only three fields
models.execute_kw(db, uid, password, 'res.partner', 'read', [ids], {
                  'fields': ['name', 'country_id', 'comment']})

# Listing record fields
# fields_get() can be used to inspect a model’s fields
# and check which ones seem to be of interest.
models.execute_kw(db, uid, password, 'res.partner', 'fields_get', [], {
                  'attributes': ['type', 'help', 'string']})

# Search and read
# equivalent to a search() followed by a read(),
# but avoids having to perform two requests and keep ids around
models.execute_kw(db, uid, password, 'res.partner',
                  'search_read', [[['is_company', '=', True]]], {'fields': ['name', 'country_id', 'comment'], 'limit': 5})

# Create record
id = models.execute_kw(db, uid, password, 'res.partner',
                       'create', [{'name': "New Partner", }])

# Update record
models.execute_kw(db, uid, password, 'res.partner',
                  'write', [[id], {'name': "Newer Parner"}])
# Get record name after having changed it
models.execute_kw(db, uid, password, 'res.partner', 'name_get', [[id]])

# Delete record
models.execute_kw(db, uid, password, 'res.partner', 'unlink', [[id]])
# check if the deleted record is still in databse
models.execute_kw(db, uid, password, 'res.partner',
                  'search', [[['id', '=', id]]])

# Create a new custom model with initially only contain
# built-in fields
# custom model name must start with x_
# the state must be provided and manual
# it is not possible to add new methods to a custom model
# only fields
models.execute_kw(db, uid, password, 'ir.model', 'create', [
                  {'name': "Custom Model", 'model': "x_custom_model", 'state': 'manual'}])
models.execute_kw(db, uid, password, 'x_custom_model', 'fields_get', [], {
                  'attributes': ['help', 'type', 'string']})

# Add custom fields x_name to model x_custom
id = models.execute_kw(db, uid, password, 'ir.model', 'create', [
                       {'name': "Custom Model", 'model': 'x_custom', 'state': 'manual'}])
models.execute_kw(db, uid, password, 'ir.model.fields', 'create', [
                  {'model_id': id, 'name': "x_name", 'ttype': 'char', 'state': 'manual', 'required': True}])

# Now create a record of x_custom_model
# This need permission from administration
record_id = models.execute_kw(db, uid, password, 'x_custom', 'create', [
                              {'x_name123': "test record", }])
models.execute_kw(db, uid, password, 'x_custom', 'read', [[record_id]])
