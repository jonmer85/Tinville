from storages.backends.s3boto import S3BotoStorage

StaticS3BotoStorage = lambda: S3BotoStorage(location='static')

class MediaS3BotoStorage(S3BotoStorage):
    location = 'media'
