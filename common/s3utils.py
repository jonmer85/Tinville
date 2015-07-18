from django.core.files.storage import get_storage_class
from storages.backends.s3boto import S3BotoStorage, FILE_OVERWRITE


class StaticS3BotoStorage(S3BotoStorage):
    """
    Storage for static files.
    """

    def __init__(self, *args, **kwargs):
        kwargs['location'] = 'static'
        super(StaticS3BotoStorage, self).__init__(*args, **kwargs)


class MediaS3BotoStorage(S3BotoStorage):
    """
    Storage for uploaded media files.
    """

    def __init__(self, *args, **kwargs):
        kwargs['location'] = 'media'
        kwargs['querystring_auth'] = False
        super(MediaS3BotoStorage, self).__init__(*args, **kwargs)

class CompressorS3BotoStorage(StaticS3BotoStorage):

    def get_available_name(self, name):
        name = self._clean_name(name)
        return name