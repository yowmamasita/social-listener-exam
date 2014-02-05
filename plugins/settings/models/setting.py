import ferris
from google.appengine.api import memcache


class Setting(ferris.Model):
    _defaults = {}
    _settings = {}
    _settings_key = None
    _name = 'Unknown'

    class __metaclass__(ferris.Model.__metaclass__):
        def __new__(meta, name, bases, dict):
            cls = ferris.Model.__metaclass__.__new__(meta, name, bases, dict)
            if name != 'Setting':
                Setting._settings[ferris.inflector.underscore(cls.__name__)] = cls
            return cls

    @classmethod
    def factory(cls, name):
        return cls._settings[ferris.inflector.underscore(name)]

    @classmethod
    def _get_kind(cls):
        return '__ferris__' + cls.__name__

    @classmethod
    def get_key(cls):
        return ferris.ndb.Key('Setting', 'Parent', cls, cls._settings_key)

    @classmethod
    def get_instance(cls):
        result = cls.get_instance_async().get_result()
        if not result:
            result = cls.get_default(True)
        return result

    @classmethod
    def get_default(cls, wait=True):
        defaults = cls._defaults.copy()
        defaults.update(ferris.settings.defaults().get(cls._settings_key, {}))

        result = cls(key=cls.get_key(), **defaults)
        f = result.put_async()
        if wait:
            f.get_result()
        return result

    @classmethod
    def get_instance_async(cls):
        key = cls.get_key()
        return key.get_async()

    @classmethod
    def get_classes(cls):
        return cls._settings

    @classmethod
    @ferris.cached('__ferris_settings')
    def get_settings(cls):
        settings = {}

        # Gather all of the settings instances as futures
        futures = {}
        for k, settings_cls in cls._settings.iteritems():
            futures[settings_cls] = settings_cls.get_instance_async()

        # Wait for them to finish together
        ferris.ndb.Future.wait_all(futures.itervalues())

        # Transform them into dictionaries, using the default if needed.
        for settings_cls, future in futures.iteritems():
            value = future.get_result()
            if not value:
                value = settings_cls.get_default(wait=False)

            settings[settings_cls._settings_key] = value.to_dict()

        return settings

    def after_put(self, key):
        memcache.delete('__ferris_settings')


class TimezoneSetting(Setting):
    _name = 'Timezone'
    _settings_key = 'timezone'
    local = ferris.ndb.StringProperty(indexed=False)


class EmailSetting(Setting):
    _name = 'Email'
    _settings_key = 'email'
    sender = ferris.ndb.StringProperty(indexed=False)


class OAuth2Setting(Setting):
    _name = 'OAuth2'
    _settings_key = 'oauth2'
    _description = """
    OAuth2 Configuration should be generated from
    <a href='https://code.google.com/apis/console'>The API Console</a>.
    """
    client_id = ferris.ndb.StringProperty(indexed=False)
    client_secret = ferris.ndb.StringProperty(indexed=False)
