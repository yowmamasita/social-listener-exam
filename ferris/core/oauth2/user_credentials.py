"""
OAuth dance session
"""

from google.appengine.ext import ndb
from ferris.core.ndb import Model
from credentials_property import CredentialsProperty
from ndb_storage import NdbStorage
import hashlib


class UserCredentials(Model):

    user = ndb.UserProperty(indexed=True)
    scopes = ndb.StringProperty(repeated=True, indexed=False)
    admin = ndb.BooleanProperty(indexed=True)
    credentials = CredentialsProperty(indexed=False)
    filter_scopes = ndb.ComputedProperty(lambda x: ','.join(sorted(x.scopes)), indexed=True)

    @classmethod
    def _get_kind(cls):
        return '__ferris__oauth2_user_credentials'

    @classmethod
    def after_get(cls, key, item):
        if item and item.credentials:
            item.credentials = NdbStorage(key, 'credentials', item).get()

    @classmethod
    def _get_key(cls, user, scopes, admin):
        scopes_hash = hashlib.sha1(','.join(sorted(scopes))).hexdigest()
        return ndb.Key(cls, '%s:%s:%s' % (user, scopes_hash, True if admin else False))

    @classmethod
    def create(cls, user, scopes, credentials, admin):
        key = cls._get_key(user, scopes, admin)
        item = cls(key=key, user=user, scopes=scopes, credentials=credentials, admin=admin)
        item.put()
        return item

    @classmethod
    def find(cls, user=None, scopes=None, admin=False):
        if user and scopes:
            key = cls._get_key(user, scopes, admin)
            x = key.get()
        else:
            q = cls.query()
            if user:
                q = q.filter(cls.user == user)
            if scopes:
                q = q.filter(cls.filter_scopes == ','.join(sorted(scopes)))
            if admin:
                q = q.filter(cls.admin == admin)
            x = q.get()

        if x:
            cls.after_get(x.key, x)
        return x

    @classmethod
    def delete_all(cls, user):
        c = cls.query().filter(user=user)
        for x in c:
            x.key.delete()


def find_credentials(user=None, scopes=None, admin=None):
    """
    Finds credentials that fit the criteria provided. If no user is provided,
    the first set of credentials that have the given scopes and privilege level.

    Returns None if no credentials are found.
    """
    return UserCredentials.find(user, scopes, admin)
