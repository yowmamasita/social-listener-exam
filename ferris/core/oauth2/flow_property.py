from google.appengine.ext import ndb
from oauth2client.client import Flow
import pickle


class FlowProperty(ndb.TextProperty):
    """
    Manages storing Flow object in an ndb property
    """
    def _validate(self, value):
        if not isinstance(value, Flow):
            raise TypeError("Expected Flow object, got %s" % repr(value))

    def _to_base_type(self, value):
        return pickle.dumps(value)

    def _from_base_type(self, value):
        return pickle.loads(str(value))
