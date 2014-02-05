from oauth2client.client import Storage


class NdbStorage(Storage):

    def __init__(self, key, property_name, entity=None):
        self._key = key
        self._property_name = property_name
        self._entity = entity

    def _get_entity(self):
        if not self._entity:
            self._entity = self._key.get()
        return self._entity

    def locked_get(self):
        credential = None

        entity = self._get_entity()

        if entity is not None:
            credential = getattr(entity, self._property_name)
            if credential and hasattr(credential, 'set_store'):
                credential.set_store(self)

        return credential

    def locked_put(self, credentials):
        entity = self._get_entity()

        if not entity:
            raise ValueError('Entity %s for storage has not been saved' % self._key)
        setattr(entity, self._property_name, credentials)
        entity.put()

    def locked_delete(self):
        self._key.delete()
