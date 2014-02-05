import ferris
from ..models.setting import Setting


class Settings(ferris.Controller):
    class Meta:
        prefixes = ('admin',)
        components = (ferris.scaffold.Scaffolding,)
        Model = Setting

    def startup(self):
        self.context['setting_classes'] = Setting.get_classes()

    def admin_list(self):
        self.context['settings'] = ferris.settings.settings()

    def admin_edit(self, key):
        model = Setting.factory(key)
        instance = model.get_instance()

        self.meta.Model = model
        self.scaffold.ModelForm = ferris.model_form(model)

        self.context['settings_class'] = model

        return ferris.scaffold.edit(self, instance.key.urlsafe())
