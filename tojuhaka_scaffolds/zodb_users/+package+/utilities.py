def has_special(string):
    import re
    return re.search(r"[^A-Za-z0-9_]+", string)

# Returns content-objects from the database
# Use this whenever you must get a specific object from ZODB
# instead of travelling with __parent__ attributes
def get_resource(resource, request):
    root = request.root
    options = {
        'groups': root['groups'],
        'users': root['users'],
    }
    return options[resource]

