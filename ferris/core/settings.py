
from webapp2 import get_request
from . import events

_defaults = {}


class ConfigurationError(Exception):
    pass


def defaults(dict=None):
    """
    Adds a set of default values to the settings registry. These can and will be updated
    by any settings modules in effect, such as the Settings Manager.

    If dict is None, it'll return the current defaults.
    """
    if dict:
        _defaults.update(dict)
    else:
        return _defaults


def settings():
    """
    Returns the entire settings registry
    """

    # Check local request storage for the completed settings registry
    try:
        request = get_request()
    except AssertionError:
        request = None

    if request and 'ferris-settings' in request.registry:
        return request.registry['ferris-settings']

    # If it's not there, do the normal thing

    settings = {}
    settings.update(_defaults)
    events.fire('build_settings', settings=settings)

    # Try to store it back in the request
    if request:
        request.registry['ferris-settings'] = settings

    return settings


def get(key, default=None):
    """
    Returns the setting at key, if available, raises an ConfigurationError if default is none, otherwise
    returns the default
    """
    _settings = settings()
    if not key in _settings:
        if default is None:
            raise ConfigurationError("Missing setting %s" % key)
        else:
            return default
    return _settings[key]
