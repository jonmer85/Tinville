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

class CompressorS3BotoStorage(S3BotoStorage):
    def __init__(self, *args, **kwargs):
        kwargs['location'] = 'compressor'
        super(CompressorS3BotoStorage, self).__init__(*args, **kwargs)
        self.local_storage = get_storage_class(
            'compressor.storage.CompressorFileStorage')()

    def save(self, name, content):

        name = super(CompressorS3BotoStorage, self).save(name, content)
        self.local_storage._save(name, content)
        return name

    def get_available_name(self, name):
        """ Overwrite existing file with the same name. """
        if FILE_OVERWRITE or name == 'manifest.json':
            name = self._clean_name(name)
            return name
        return super(CompressorS3BotoStorage, self).get_available_name(name)