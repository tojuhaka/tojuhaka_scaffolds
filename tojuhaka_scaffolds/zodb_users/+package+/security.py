from passlib.context import CryptContext
from pyramid.security import Allow, Everyone
from pyramid.httpexceptions import HTTPForbidden
from pyramid.events import NewRequest, subscriber
from .utilities import get_resource


# TODO: HIDE?
acl = [(Allow, Everyone, 'view'),
        (Allow, u'group:members', 'edit'),
        (Allow, u'group:admins', 'edit_all'),
        (Allow, u'group:admins', 'edit_content'),
        (Allow, u'group:editors', 'edit_content')]

group_names = {
    'admin': u'group:admins',
    'editor': u'group:editors',
    'member': u'group:members'
}

# Salt for pasword hashes, move to database or somewhere safe (and change it )
salt = u'torpedo'

# Crypt config for password hashes
pwd_context = CryptContext(
    #replace this list with the hash(es) you wish to support.
    #this example sets pbkdf2_sha256 as the default,
    #with support for legacy des_crypt hashes.
    schemes=["pbkdf2_sha256", "des_crypt"],
    default="pbkdf2_sha256",

    #vary rounds parameter randomly when creating new hashes...
    all__vary_rounds="10%",

    #set the number of rounds that should be used...
    #(appropriate values may vary for different schemes,
    # and the amount of time you wish it to take)
    pbkdf2_sha256__default_rounds=8000,
    )

def groupfinder(username, request):
    if username in get_resource('users', request):
        return get_resource('groups', request)[username]

#Protect sessions from Cross-site request forgery attacks
@subscriber(NewRequest)
def csrf_validation(event):
    if event.request.method == "POST":
        token = event.request.POST.get("_csrf")
        if token is None or token != event.request.session.get_csrf_token():
            raise HTTPForbidden("CSRF token is missing or invalid")
