import os
from settingspackage import settings


class HttpTemplateResponse:
    def __init__(self, template):
        import os
        from settingspackage import settings
        self.template = template

    def _generate_response(self):
        for app in settings.INSTALLED_APPS:
            template_path = os.path.join(settings.BASE_DIR, app, self.template)
            if os.path.isfile(template_path):
                with open(template_path) as template:
                    self.response = template.read()

                break
        else:
            raise ValueError('Template not found')


    def get_response(self):
        if not hasattr(self, 'response'):
            self._generate_response()

        return self.response

