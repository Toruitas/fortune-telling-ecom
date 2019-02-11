# custom_storages.py
from django.conf import settings
from django.core.files.storage import get_storage_class
from storages.backends.s3boto import S3BotoStorage
from filebrowser_safe.storage import S3BotoStorageMixin


class StaticStorage(S3BotoStorage, S3BotoStorageMixin):
    location = settings.STATICFILES_LOCATION

    # def __init__(self, *args, **kwargs):
    #     kwargs['custom_domain'] = settings.AWS_CLOUDFRONT_DOMAIN
    #     super(StaticStorage, self).__init__(*args, **kwargs)


class MediaStorage(S3BotoStorage,S3BotoStorageMixin):
    """uploads to 'mybucket/media/', serves from 'cloudfront.net/media/'
    http://stackoverflow.com/questions/31357353/using-cloudfront-with-django-s3boto
    http://stackoverflow.com/questions/25422543/use-aws-s3-vs-cloudfront
    http://www.leehodgkinson.com/blog/my-mezzanine-s3-setup/
    """
    location = settings.MEDIAFILES_LOCATION

    # def __init__(self, *args, **kwargs):
    #     kwargs['custom_domain'] = settings.AWS_CLOUDFRONT_DOMAIN
    #     super(MediaStorage, self).__init__(*args, **kwargs)


class CachedS3BotoStorage(S3BotoStorage):
    """
    S3 storage backend that saves the files locally, too.
    """
    def __init__(self, *args, **kwargs):
        super(CachedS3BotoStorage, self).__init__(*args, **kwargs)
        self.local_storage = get_storage_class(
            "compressor.storage.CompressorFileStorage")()

    def save(self, name, content):
        self.local_storage._save(name, content)
        super(CachedS3BotoStorage, self).save(name, self.local_storage._open(name))
        return name