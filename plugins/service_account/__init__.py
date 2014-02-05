from ferris import plugins, settings, ndb

plugins.register('service_account')

from plugins.settings import SettingModel


class ServiceAccountSettings(SettingModel):
    _name = 'OAuth2 Service Account'
    _settings_key = 'oauth2_service_account'
    domain = ndb.StringProperty(indexed=False, verbose_name="The Google Apps Domain")
    default_user = ndb.StringProperty(indexed=False, verbose_name="The email of the user to impersonate by default")
    client_email = ndb.StringProperty(indexed=False, verbose_name="...@developer.gserviceaccount.com")
    private_key = ndb.TextProperty(verbose_name="PEM Format")


def get_config():
    config = settings.get('oauth2_service_account')
    if not config['private_key'] or not config['client_email'] or not config['domain']:
        raise RuntimeError("OAuth2 Service Account is not configured correctly")
    return config


from oauth2client.client import SignedJwtAssertionCredentials


def build_credentials(scope, user=None):
    """
    Builds service account credentials using the configuration stored in settings
    and masquerading as the provided user.
    """
    config = get_config()

    if not user:
        user = config['default_user']

    if not isinstance(scope, (list, tuple)):
        scope = [scope]

    creds = SignedJwtAssertionCredentials(
        service_account_name=config['client_email'],
        private_key=config['private_key'],
        scope=scope,
        prn=user)

    return creds


def credentials_to_token(credentials):
    """
    Transforms an Oauth2 credentials object into an OAuth2Token object
    to be used with the legacy gdata API
    """
    import httplib2
    import gdata.gauth

    credentials.refresh(httplib2.Http())
    token = gdata.gauth.OAuth2Token(
        client_id=credentials.client_id,
        client_secret=credentials.client_secret,
        scope=credentials.scope,
        user_agent='lolidk/wtfbbq/cloudsherpas',
        access_token=credentials.access_token,
        refresh_token=credentials.refresh_token)
    return token
