from ferris.core import events, plugins

plugins.register('settings')


from .models.setting import Setting as SettingModel


@events.on('build_settings')
def on_build_settings(settings):
    overrides = SettingModel.get_settings()
    settings.update(overrides)
