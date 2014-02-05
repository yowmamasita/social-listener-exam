from google.appengine.ext import ndb
from oauth2client.client import Credentials


class CredentialsProperty(ndb.TextProperty):
    """
    Manages storing Oauth2 credentials in an ndb property
    """
    def _validate(self, value):
        if not isinstance(value, Credentials):
            raise TypeError("Expected Credentials object, got %s" % repr(value))

    def _to_base_type(self, value):
        return value.to_json()

    def _from_base_type(self, value):
        return Credentials.new_from_json(value)
