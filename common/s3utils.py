from storages.backends.s3boto import S3BotoStorage


class MediaS3BotoStorage(S3BotoStorage):
    location = 'media'


class StaticS3BotoStorage(S3BotoStorage):
    location = 'static'