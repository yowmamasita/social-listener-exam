"""
OAuth dance session
"""

from google.appengine.ext import ndb
from ferris.core.ndb import Model
from flow_property import FlowProperty


class Session(Model):

    scopes = ndb.StringProperty(indexed=False, repeated=True)
    admin = ndb.BooleanProperty(indexed=False)
    force_prompt = ndb.BooleanProperty(indexed=False)
    redirect = ndb.StringProperty(indexed=False)
    flow = FlowProperty(indexed=False)

    @classmethod
    def _get_kind(cls):
        return '__ferris__oauth2_session'
