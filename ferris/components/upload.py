from google.appengine.ext import blobstore
import wtforms
import urllib2
import cgi


class Upload(object):
    """
    Automatically handles file upload fields that need to use the blobstore.

    This works by:

     * Detecting if you're on an add or edit action (you can add additional actions with ``upload_actions``, or set ``process_uploads`` to True)
     * Adding the ``upload_url`` template variable that points to the blobstore
     * Updating the ``form_action`` and ``form_encoding`` scaffolding variables to use the new blobstore action
     * Processing uploads when they come back
     * Adding each upload's key to the form data so that it can be saved to the model

    Does not require that the controller subclass ``BlobstoreUploadHandler``, however to serve blobs you must subclass ``BlobstoreDownloadHandler``.
    """

    def __init__(self, controller):
        self.controller = controller
        self.__uploads = None
        self.process_uploads = False
        self.upload_actions = ('add', 'edit')
        self.gs_bucket_name = None

        controller.events.before_startup += self.on_before_startup
        controller.events.scaffold_before_apply += self.on_scaffold_before_apply
        controller.events.after_dispatch += self.on_after_dispatch

    def on_before_startup(self, controller):
        if controller.route.action in self.upload_actions:
            self.process_uploads = True

    def on_scaffold_before_apply(self, controller, container, item):
        if self.process_uploads and isinstance(container, wtforms.Form):
            self.process(container)

    def on_after_dispatch(self, controller, response):
        """
        This will additionally check if ?start is the query string. If so, it will return just the upload url. This is
        great for rest apis.
        """
        if self.process_uploads:
            if not 'upload_url' in controller.context:
                controller.context.set(upload_url=self.generate_upload_url(self.controller.route.action))
                if hasattr(controller, 'scaffold'):
                    controller.scaffold.form_action = controller.context['upload_url']
                    controller.scaffold.form_encoding = 'multipart/form-data'

            if 'start' in controller.request.params:
                if not response:
                    controller.context['data'] = controller.context['upload_url']
                    if 'json' in controller.components:
                        controller.components.json.render()

    def process(self, form, item=None):
        """
        Process all of the incoming file upload and populate the form with them.
        Only processes file fields that are present in the form
        """
        for field in [x for x in form if isinstance(x, wtforms.fields.FileField)]:
            files = self.get_uploads(field.name)
            if files and files[0]:
                getattr(form, field.name).data = files[0].key()
            else:
                delattr(form, field.name)

    def generate_upload_url(self, action=None):
        if not action:
            action = self.controller.route.action

        url = urllib2.unquote(self.controller.uri(action=action, _pass_all=True, _full=True))

        return blobstore.create_upload_url(
            success_path=url,
            gs_bucket_name=self.gs_bucket_name)

    def serve(self, item, property):
        if not item:
            return 404

        self.controller.send_blob(getattr(item, property))

        return self.controller.response

    def get_uploads(self, field_name=None):
        """Get uploads sent to this controller.

        Args:
        field_name: Only select uploads that were sent as a specific field.

        Returns:
        A list of BlobInfo records corresponding to each upload.
        Empty list if there are no blobinfo records for field_name.
        """
        if self.__uploads is None:
            self.__uploads = {}
            for key, value in self.controller.request.params.items():
                if isinstance(value, cgi.FieldStorage):
                    if 'blob-key' in value.type_options:
                        info = blobstore.parse_blob_info(value)
                        self.__uploads.setdefault(key, []).append(info)

        results = []

        if field_name:
            try:
                results = list(self.__uploads[field_name])
            except KeyError:
                pass
        else:
            for uploads in self.__uploads.itervalues():
                results += uploads

        # Workaround for mangled filenames
        return blobstore.BlobInfo.get([x.key() for x in results])
