from __future__ import absolute_import, unicode_literals
import os

from django import VERSION as DJANGO_VERSION
from django.utils.translation import ugettext_lazy as _
# from machina import get_apps as get_machina_apps
# from machina import MACHINA_MAIN_TEMPLATE_DIR, MACHINA_MAIN_STATIC_DIR


######################
# CARTRIDGE SETTINGS #
######################

# The following settings are already defined in cartridge.shop.defaults
# with default values, but are common enough to be put here, commented
# out, for conveniently overriding. Please consult the settings
# documentation for a full list of settings Cartridge implements:
# http://cartridge.jupo.org/configuration.html#default-settings

# Sequence of available credit card types for payment.
# SHOP_CARD_TYPES = ("Mastercard", "Visa", "Diners", "Amex")

# Setting to turn on featured images for shop categories. Defaults to False.
# SHOP_CATEGORY_USE_FEATURED_IMAGE = True

# Set an alternative OrderForm class for the checkout process.
# SHOP_CHECKOUT_FORM_CLASS = 'cartridge.shop.forms.OrderForm'

# If True, the checkout process is split into separate
# billing/shipping and payment steps.
# SHOP_CHECKOUT_STEPS_SPLIT = True

# If True, the checkout process has a final confirmation step before
# completion.
# SHOP_CHECKOUT_STEPS_CONFIRMATION = True

# Controls the formatting of monetary values accord to the locale
# module in the python standard library. If an empty string is
# used, will fall back to the system's locale.
SHOP_CURRENCY_LOCALE = "en_US.UTF-8"
# SHOP_CURRENCY_LOCALE = "en_HK.UTF-8"
# SHOP_CURRENCY_LOCALE = "zh_CN.UTF-8"
# SHOP_CURRENCY_LOCALE = "ja_JP.UTF-8"

# Dotted package path and name of the function that
# is called on submit of the billing/shipping checkout step. This
# is where shipping calculation can be performed and set using the
# function ``cartridge.shop.utils.set_shipping``.
# SHOP_HANDLER_BILLING_SHIPPING = \
#                       "cartridge.shop.checkout.default_billship_handler"

# Dotted package path and name of the function that
# is called once an order is successful and all of the order
# object's data has been created. This is where any custom order
# processing should be implemented.
# SHOP_HANDLER_ORDER = "cartridge.shop.checkout.default_order_handler"

# Dotted package path and name of the function that
# is called on submit of the payment checkout step. This is where
# integration with a payment gateway should be implemented.
# SHOP_HANDLER_PAYMENT = "cartridge.shop.checkout.default_payment_handler"

# Sequence of value/name pairs for order statuses.
# SHOP_ORDER_STATUS_CHOICES = (
#     (1, "Unprocessed"),
#     (2, "Processed"),
# )

# Sequence of value/name pairs for types of product options,
# eg Size, Colour. NOTE: Increasing the number of these will
# require database migrations!
# SHOP_OPTION_TYPE_CHOICES = (
#     (1, "Size"),
#     (2, "Colour"),
# )

# Sequence of indexes from the SHOP_OPTION_TYPE_CHOICES setting that
# control how the options should be ordered in the admin,
# eg for "Colour" then "Size" given the above:
# SHOP_OPTION_ADMIN_ORDER = (2, 1)


######################
# MEZZANINE SETTINGS #
######################

# The following settings are already defined with default values in
# the ``defaults.py`` module within each of Mezzanine's apps, but are
# common enough to be put here, commented out, for conveniently
# overriding. Please consult the settings documentation for a full list
# of settings Mezzanine implements:
# http://mezzanine.jupo.org/docs/configuration.html#default-settings

# Controls the ordering and grouping of the admin menu.
#
# ADMIN_MENU_ORDER = (
#     ("Content", ("pages.Page", "blog.BlogPost",
#        "generic.ThreadedComment", (_("Media Library"), "fb_browse"),)),
#     (_("Shop"), ("shop.Product", "shop.ProductOption", "shop.DiscountCode",
#        "shop.Sale", "shop.Order")),
#     ("Site", ("sites.Site", "redirects.Redirect", "conf.Setting")),
#     ("Users", ("auth.User", "auth.Group",)),
# )

# A three item sequence, each containing a sequence of template tags
# used to render the admin dashboard.
#
# DASHBOARD_TAGS = (
#     ("blog_tags.quick_blog", "mezzanine_tags.app_list"),
#     ("comment_tags.recent_comments",),
#     ("mezzanine_tags.recent_actions",),
# )

# A sequence of templates used by the ``page_menu`` template tag. Each
# item in the sequence is a three item sequence, containing a unique ID
# for the template, a label for the template, and the template path.
# These templates are then available for selection when editing which
# menus a page should appear in. Note that if a menu template is used
# that doesn't appear in this setting, all pages will appear in it.

# PAGE_MENU_TEMPLATES = (
#     (1, _("Top navigation bar"), "pages/menus/dropdown.html"),
#     (2, _("Left-hand tree"), "pages/menus/tree.html"),
#     (3, _("Footer"), "pages/menus/footer.html"),
# )

# A sequence of fields that will be injected into Mezzanine's (or any
# library's) models. Each item in the sequence is a four item sequence.
# The first two items are the dotted path to the model and its field
# name to be added, and the dotted path to the field class to use for
# the field. The third and fourth items are a sequence of positional
# args and a dictionary of keyword args, to use when creating the
# field instance. When specifying the field class, the path
# ``django.models.db.`` can be omitted for regular Django model fields.
#
# EXTRA_MODEL_FIELDS = (
#     (
#         # Dotted path to field.
#         "mezzanine.blog.models.BlogPost.image",
#         # Dotted path to field class.
#         "somelib.fields.ImageField",
#         # Positional args for field class.
#         (_("Image"),),
#         # Keyword args for field class.
#         {"blank": True, "upload_to": "blog"},
#     ),
#     # Example of adding a field to *all* of Mezzanine's content types:
#     (
#         "mezzanine.pages.models.Page.another_field",
#         "IntegerField", # 'django.db.models.' is implied if path is omitted.
#         (_("Another name"),),
#         {"blank": True, "default": 1},
#     ),
# )

# Setting to turn on featured images for blog posts. Defaults to False.
#
# BLOG_USE_FEATURED_IMAGE = True

# If True, the django-modeltranslation will be added to the
# INSTALLED_APPS setting.
USE_MODELTRANSLATION = True


########################
# MAIN DJANGO SETTINGS #
########################

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
# AWS
ALLOWED_HOSTS = ["*",".ap-northeast-1.elasticbeanstalk.com/", 'localhost']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'

# If you set this to True, Django will use timezone-aware datetimes.
USE_TZ = True

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en"

# Supported languages
LANGUAGES = (
    ('en', _('English')),
    ('zh-hans', _('Simplified Chinese')),
    ('zh-hant', _('Traditional Chinese'))
)

# https://docs.djangoproject.com/en/1.10/topics/i18n/translation/
# http://django-modeltranslation.readthedocs.io/en/latest/usage.html#fallback-languages
MODELTRANSLATION_FALLBACK_LANGUAGES = {
    'default': ('en',),
    'zh-hans': ('zh-hant','zh-hans','en',),
    'zh-hant': ('zh-hans','zh-hant','en',)
}

# A boolean that turns on/off debug mode. When set to ``True``, stack traces
# are displayed for error pages. Should always be set to ``False`` in
# production. Best set to ``True`` in local_settings.py
# AWS
# DEBUG = False

# Whether a user's session cookie expires when the Web browser is closed.
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

AUTHENTICATION_BACKENDS = ("mezzanine.core.auth_backends.MezzanineBackend",)

# The numeric mode to set newly-uploaded files to. The value should be
# a mode you'd pass directly to os.chmod.
FILE_UPLOAD_PERMISSIONS = 0o644





#########
# PATHS #
#########

# Full filesystem path to the project.
PROJECT_APP_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_APP = os.path.basename(PROJECT_APP_PATH)
PROJECT_ROOT = BASE_DIR = os.path.dirname(PROJECT_APP_PATH)

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Every cache key will get prefixed with this value - here we set it to
# the name of the directory the project is in to try and use something
# project specific.
CACHE_MIDDLEWARE_KEY_PREFIX = PROJECT_APP

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/static/"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
# STATIC_ROOT = os.path.join(PROJECT_ROOT, STATIC_URL.strip("/"))
# local in local_settings. This is for AWS
# for Amazon (not Cloudfront), must put in www folder. Otherwise permissions give you that 403 shit
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "www", "static") # formerly static_cdn

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    # MACHINA_MAIN_STATIC_DIR,
    #'/var/www/static/',
]

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = "/media/"

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
# MEDIA_ROOT = os.path.join(PROJECT_ROOT, *MEDIA_URL.strip("/").split("/"))
# for AWS, local in local_settings
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media_cdn")

# Package/module name to import the root urlpatterns from for the project.
ROOT_URLCONF = "%s.urls" % PROJECT_APP

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PROJECT_ROOT, "templates"),
            # os.path.join(PROJECT_ROOT, "templates/machina"),
            # MACHINA_MAIN_TEMPLATE_DIR,
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.core.context_processors.debug",
                "django.core.context_processors.i18n",
                "django.core.context_processors.static",
                "django.core.context_processors.media",
                "django.core.context_processors.request",
                "django.core.context_processors.tz",
                "mezzanine.conf.context_processors.settings",
                "mezzanine.pages.context_processors.page",
                # machina
                # 'machina.core.context_processors.metadata',
            ],
            "builtins": [
                "mezzanine.template.loader_tags",
            ],
        },
    },
]



# Put strings here, like "/home/html/django_templates"
# or "C:/www/django/templates".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
# for stupid mezzanine collecttemplates command
# dictionary above takes precedence
TEMPLATE_DIRS = (os.path.join(PROJECT_ROOT, "templates"),)

if DJANGO_VERSION < (1, 9):
    del TEMPLATES[0]["OPTIONS"]["builtins"]


################
# APPLICATIONS #
################

# templates come before installed templates
# model translations come after installed mez ones
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.redirects",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
    "mezzanine.boot",
    "mezzanine.conf",
    "mezzanine.core",
    "mezzanine.generic",
    "mezzanine.pages",
    "cartridge_braintree",
    "cartridge.shop",
    "mezzanine.blog",
    "mezzanine.forms",
    "mezzanine.galleries",
    "mezzanine.twitter",
    "mezzanine.accounts",
    # "mezzanine.mobile",
    # other
    "el_pagination",
    "storages",
    "mathfilters",
    'crispy_forms',
    # "django_s3_storage",  # https://github.com/etianen/django-s3-storage
    # 'sorl.thumbnail',  # https://github.com/mariocesar/sorl-thumbnail
    "fortune",
    "about",
    "profiles",
    "patches",  # for model translation, this must be after anything it inherits from
    "payments",
    "django_celery_results",
    'paypal.standard.ipn',
    'compressor',
    "djcelery_email",
    # Machina related apps:
    # 'mptt',
    # 'haystack',
    # 'widget_tweaks',
#     'django_markdown',
# ] + get_machina_apps()
]

# List of processors used by RequestContext to populate the context.
# Each one should be a callable that takes the request object as its
# only parameter and returns a dictionary to add to the context.
# TEMPLATE_CONTEXT_PROCESSORS = (
#     "django.contrib.auth.context_processors.auth",
#     "django.contrib.messages.context_processors.messages",
#     "django.core.context_processors.debug",
#     "django.core.context_processors.i18n",
#     "django.core.context_processors.static",
#     "django.core.context_processors.media",
#     "django.core.context_processors.request",
#     "django.core.context_processors.tz",
#     # mezzanine
#     "mezzanine.conf.context_processors.settings",
#     "mezzanine.pages.context_processors.page",
#
# )


# Machina needs cache
# CACHES = {
#   'default': {
#     'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#   },
#   'machina_attachments': {
#     'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
#     'LOCATION': '/tmp',
#   }
# }
# #
# # # Machina search haystack
# HAYSTACK_CONNECTIONS = {
#   'default': {
#     'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
#   },
# }

# List of middleware classes to use. Order is important; in the request phase,
# these middleware classes will be applied in the order given, and in the
# response phase the middleware will be applied in reverse order.
MIDDLEWARE_CLASSES = [
    "mezzanine.core.middleware.UpdateCacheMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    # Uncomment if using internationalisation or localisation
    # 'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "cartridge.shop.middleware.ShopMiddleware",
    "mezzanine.core.request.CurrentRequestMiddleware",
    "mezzanine.core.middleware.RedirectFallbackMiddleware",
    "mezzanine.core.middleware.TemplateForDeviceMiddleware",
    "mezzanine.core.middleware.TemplateForHostMiddleware",
    "mezzanine.core.middleware.AdminLoginInterfaceSelectorMiddleware",
    "mezzanine.core.middleware.SitePermissionMiddleware",
    # Uncomment the following if using any of the SSL settings:
    # "mezzanine.core.middleware.SSLRedirectMiddleware",
    "mezzanine.pages.middleware.PageMiddleware",
    "mezzanine.core.middleware.FetchFromCacheMiddleware",
    # Machina
    # 'machina.apps.forum_permission.middleware.ForumPermissionMiddleware',
]

# Store these package names here as they may change in the future since
# at the moment we are using custom forks of them.
PACKAGE_NAME_FILEBROWSER = "filebrowser_safe"
PACKAGE_NAME_GRAPPELLI = "grappelli_safe"



#########################
# OPTIONAL APPLICATIONS #
#########################

# These will be added to ``INSTALLED_APPS``, only if available.
OPTIONAL_APPS = (
    "debug_toolbar",
    "django_extensions",
    "compressor",
    PACKAGE_NAME_FILEBROWSER,
    PACKAGE_NAME_GRAPPELLI,
)

##################
# LOCAL SETTINGS #
##################

# Allow any settings to be defined in local_settings.py which should be
# ignored in your version control system allowing for settings to be
# defined per machine.

# Instead of doing "from .local_settings import *", we use exec so that
# local_settings has full access to everything defined in this module.
# Also force into sys.modules so it's visible to Django's autoreload.

f = os.path.join(PROJECT_APP_PATH, "local_settings.py")
AWS = False
if os.path.exists(f) and AWS is False:
    import sys
    import imp
    module_name = "%s.local_settings" % PROJECT_APP
    module = imp.new_module(module_name)
    module.__file__ = f
    sys.modules[module_name] = module
    exec(open(f, "rb").read())

###################
# DEPLOY SETTINGS #
###################

else:
    #### deploy settings
    #############
    # DATABASES #
    #############
    DEBUG = False

    # if no local settings, for AWS
    DATABASES = {
        "default": {
            # Add "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            # DB name or path to database file if using sqlite3.
            "NAME": os.environ['RDS_DB_NAME'],
            # Not used with sqlite3.
            "USER": os.environ['RDS_USERNAME'],
            # Not used with sqlite3.
            "PASSWORD": os.environ['RDS_PASSWORD'],
            # Set to empty string for localhost. Not used with sqlite3.
            "HOST": os.environ['RDS_HOSTNAME'],
            # Set to empty string for default. Not used with sqlite3.
            "PORT": os.environ['RDS_PORT'],
        }
    }
    SECRET_KEY = os.environ.get('SECRET_KEY')
    NEVERCACHE_KEY = os.environ.get('NEVERCACHE_KEY')

    #############
    #    AWS    #
    #############

    # THUMBNAIL_FORCE_OVERWRITE = True  # for sorl-thumbnail, quickens s3

    # AWS Settings
    # https://www.caktusgroup.com/blog/2014/11/10/Using-Amazon-S3-to-store-your-Django-sites-static-and-media-files/
    # http://martinbrochhaus.com/s3.html
    # https://realpython.com/blog/python/deploying-a-django-app-and-postgresql-to-aws-elastic-beanstalk/
    # http://www.leehodgkinson.com/blog/my-mezzanine-s3-setup/
    # https://github.com/etianen/django-s3-storage
    # https://github.com/mariocesar/sorl-thumbnail
    AWS_HEADERS = {  # see http://developer.yahoo.com/performance/rules.html#expires
            'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
            'Cache-Control': 'max-age=94608000',
        }
    #http://docs.aws.amazon.com/AmazonS3/latest/API/sigv4-query-string-auth.html
    # allows authenticating with creds in querystring for temp access to a resource
    # Setting to False if not needed helps get rid of uwanted qstrings in compressed
    # output
    AWS_REGION = "ap-northeast-1"
    AWS_QUERYSTRING_AUTH = False
    # Used to make sure that only changed files are uploaded with collectstatic
    AWS_PRELOAD_METADATA = False
    AWS_S3_SECURE_URLS = False
    AWS_S3_ENCRYPTION = False
    AWS_S3_URL_PROTOCOL = "https:"
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME') # environ var in
    # AWS_CLOUDFRONT_DOMAIN = os.environ.get('AWS_CLOUDFRONT_DOMAIN') #todo: change this and set static/media to this
    # S3 specific access key & ID
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')  # environ var in production
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')  # environ var in production
    AWS_S3_CUSTOM_DOMAIN = "{}.s3.amazonaws.com".format(AWS_STORAGE_BUCKET_NAME)
    STATICFILES_LOCATION = 'static'  # formerly static_cdn
    STATIC_ROOT = ''
    STATICFILES_STORAGE = 'patches.custom_storages.StaticStorage'
    STATIC_URL = "{}//{}/{}/".format(AWS_S3_URL_PROTOCOL, AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)
    # STATIC_URL = "{}//{}/{}/".format(AWS_S3_URL_PROTOCOL,AWS_CLOUDFRONT_DOMAIN, STATICFILES_LOCATION)
    MEDIAFILES_LOCATION = 'media_cdn'
    MEDIA_URL = "{}//{}/{}/".format(AWS_S3_URL_PROTOCOL, AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
    # MEDIA_URL = "{}//{}/{}/".format(AWS_S3_URL_PROTOCOL,AWS_CLOUDFRONT_DOMAIN, MEDIAFILES_LOCATION)
    MEDIA_ROOT = ''
    DEFAULT_FILE_STORAGE = 'patches.custom_storages.MediaStorage'

    #############
    #  CELERY   #
    #############
    # http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html
    BROKER_URL = 'sqs://{}:{}@'.format(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY)
    # CELERY_RESULT_BACKEND = 'sqs://aws_access_key_id:aws_secret_access_key@'
    CELERY_RESULT_BACKEND = 'django-db'
    BROKER_TRANSPORT_OPTIONS = {
        'region': 'ap-northeast-1',
    }

    #############
    # COMPRESS  #
    #############
    # http://django-compressor.readthedocs.io/en/latest/remote-storages/
    COMPRESS_URL = STATIC_URL
    COMPRESS_STORAGE = STATICFILES_STORAGE
    COMPRESS_ENABLED = True



####################
# DYNAMIC SETTINGS #
####################

# set_dynamic_settings() will rewrite globals based on what has been
# defined so far, in order to provide some better defaults where
# applicable. We also allow this settings module to be imported
# without Mezzanine installed, as the case may be when using the
# fabfile, where setting the dynamic settings below isn't strictly
# required.
try:
    from mezzanine.utils.conf import set_dynamic_settings
except ImportError:
    pass
else:
    set_dynamic_settings(globals())


####################
#   MY SETTINGS    #
####################
# http://mezzanine.jupo.org/docs/model-customization.html
# This caused problems initially. First deploy have it commented out. Then add in on second.
MIGRATION_MODULES = {
    "pages": "patches.mezz_migrations.pages",
    "forms": "patches.mezz_migrations.forms",
    "galleries": "patches.mezz_migrations.galleries",
    "blog":"patches.mezz_migrations.blogs",
    "accounts":"patches.mezz_migrations.accounts",
    "shop":"patches.mezz_migrations.shop",
    "conf":"patches.mezz_migrations.conf"
}


AUTH_PROFILE_MODULE = "profiles.MyProfile"  # Use this for editing things, create a global view to display everyting else
# ACCOUNTS_PROFILE_VIEWS_ENABLED = False  # disable/enable profile views
ACCOUNTS_VERIFICATION_REQUIRED = False
ACCOUNTS_NO_USERNAME = True
ACCOUNTS_PROFILE_FORM_EXCLUDE_FIELDS = ["shipping_detail_street","shipping_detail_city","shipping_detail_state",
                                        "shipping_detail_postcode","shipping_detail_country"]
SITE_TITLE = "SE BRILLIANT FENG SHUI"
SITE_TAGLINE = "Bringing the Fung to your Shui"
BLOG_SLUG = "articles"
BLOG_USE_FEATURED_IMAGE = True
BLOG_POST_PER_PAGE = 4
EL_PAGINATION_PER_PAGE = BLOG_POST_PER_PAGE
# AKIMSET_API_KEY = http://akismet.com/
# SSL_ENABLED = True
COMMENTS_ACCOUNT_REQUIRED = True
COMMENTS_USE_RATINGS = False
AMAZON_SES = False
SENDBLUE = True
HOMEPAGE_BLOG_POSTS = 2
FILEBROWSER_MAX_UPLOAD_SIZE = 40000000
COMMENTS_DISQUS_SHORTNAME = os.environ.get("DISQUS_SHORTNAME")
DEV_SERVER = True
MEMBERSHIP_DISCOUNT = 10  # number in %... 10% for example
MEMBERSHIP_MULTIPLIER = (100-MEMBERSHIP_DISCOUNT)/100
MEMBERSHIP_DISCOUNT_DECIMAL = MEMBERSHIP_DISCOUNT/100
DEFAULT_RECEIVE_EMAIL = os.environ.get("DEFAULT_RECEIVE_EMAIL")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")
GOOGLE_ANALYTICS_ID = os.environ.get("GOOGLE_ANALYTICS_ID")
CRISPY_TEMPLATE_PACK = 'bootstrap3'

###### CSS Minification ######
# COMPRESS_ENABLED = not DEBUG
COMPRESS_CSS_FILTERS = ['compressor.filters.css_default.CssAbsoluteFilter',  'compressor.filters.cssmin.CSSMinFilter']


###### Payments info
PING_SK = os.environ.get("PING_SK")
PING_APP_ID = os.environ.get("PING_APP_ID")
STRIPE_API_KEY = STRIPE_SK = os.environ.get('STRIPE_SK')
STRIPE_PK = os.environ.get('STRIPE_PK')
STRIPE_CURRENCY = 'cny'
# SHOP_HANDLER_PAYMENT = 'payments.payments_api.process'
PAYPAL_TEST = True
# BRAINTREE_MERCHANT_ID = <your merchant ID>
# BRAINTREE_PUBLIC_KEY = <your public key>
# BRAINTREE_PRIVATE_KEY = <your private key>

###### Shop stuff
SHOP_DISCOUNT_FIELD_IN_CHECKOUT = False
SHOP_USE_WISHLIST = False
SHOP_CATEGORY_USE_FEATURED_IMAGE = True
SHOP_PER_PAGE_CATEGORY = 100
SHOP_USE_RATINGS = False
SHOP_USE_RELATED_PRODUCTS = False
SHOP_CHECKOUT_STEPS_CONFIRMATION = False
SHOP_ORDER_EMAIL_BCC = DEFAULT_RECEIVE_EMAIL
SHOP_PAYMENT_STEP_ENABLED = False
# CHECKOUT_STEP_PAYMENT = 3 doesn't work

##### MACHINA FORUM
# MACHINA_FORUM_NAME = _("Brilliant Forum")
# MACHINA_BASE_TEMPLATE_NAME = "base.html"
# http://django-machina.readthedocs.io/en/stable/forum_permissions.html
# MACHINA_DEFAULT_AUTHENTICATED_USER_FORUM_PERMISSIONS = [
#     'can_see_forum',
#     'can_read_forum',
#     'can_start_new_topics',
#     'can_reply_to_topics',
#     'can_edit_own_posts',
#     'can_post_without_approval',
#     'can_create_polls',
#     'can_vote_in_polls',
#     'can_download_file',
# ]


from django.utils.translation import ugettext_lazy as _

MEMBERSHIPS = {
    "regular": {"price": (0, 0),  # HKD, RMB
                "benefits": [_("Full shop available"),]},
    "gold": {"price": (160, 200),
             "benefits": [_("Full shop available"),
                             _("Full access to all essays"),
                             _("Receive Feng Shui advice from Master Kiki twice each year"),
                             _("Free Feng Shui calendar (HK$200 value)"),
                             _("Gold member prices on all products and classes"),
                             _("High priority for Feng Shui consultations"),
                             _("Full access to the Feng Shui forums")]
             },
    "diamond": {"price": (800, 1000),
                "benefits": [_("Full shop available"),
                                _("Full access to all essays"),
                                _("Receive Feng Shui advice from Master Kiki twice each year"),
                                _("Free Feng Shui calendar (HK$200 value)"),
                                _("Diamond member prices on all products and classes"),
                                _("Highest priority for Feng Shui consultations"),
                                _("Full access to the Feng Shui forums"),
                                _("8 Character Fortune reading"),
                                _("Online Fung Shui consultation for your residence"),
                                _("Receive 10 additional words of wisdom from Master Kiki")]},
}

# sendinblue, sendgrid, or ses?


##### EMAIL SETTINGS #####
##### Email AWS #####
# https://github.com/django-ses/django-ses
# https://pypi.python.org/pypi/django-celery-email
#
# EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'
if AMAZON_SES:
    EMAIL_BACKEND = 'django_ses.SESBackend'
    # CELERY_EMAIL_BACKEND = 'django_ses.SESBackend'
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')  # environ var in production
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')  # environ var in production
    AWS_SES_REGION_NAME = 'us-west-2'
    AWS_SES_REGION_ENDPOINT = 'email.us-west-2.amazonaws.com'
##### Email SendInBlue #####
# https://account.sendinblue.com/advanced/api
elif SENDBLUE:
    EMAIL_HOST = "smtp-relay.sendinblue.com"
    # CELERY_EMAIL_BACKEND = "smtp-relay.sendinblue.com"
    EMAIL_PORT = 587
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
    EMAIL_USE_TLS = True
    # EMAIL_USE_SSL =
else:
    # CELERY_EMAIL_BACKEND = "smtp.gmail.com"
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_PORT = 587
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
    EMAIL_USE_TLS = True
    # EMAIL_USE_SSL =


# CELERY STUFF
# BROKER_URL = 'amqp://localhost'
# CELERY_RESULT_BACKEND = 'amqp://localhost'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Africa/Nairobi'


# http://mezzanine.jupo.org/docs/model-customization.html
# http://bitofpixels.com/blog/techniques-for-modifying-mezzanine/
# https://startcodenow.wordpress.com/2015/04/05/add-extra-field-cartridge-mezzanine/

EXTRA_MODEL_FIELDS = (
    ####### Blog Post extra fields #########
    # image 2 field for blog post
    # (
    #     # Dotted path to field.
    #     "mezzanine.blog.models.BlogPost.image2",
    #     # Dotted path to field class.
    #     "mezzanine.core.fields.FileField",
    #     # Positional args for field class.
    #     ("Image 2",),
    #     # Keyword args for field class.
    #     {"blank": True,
    #      "null": True,
    #      "upload_to": "blog",  # "blog.BlogPost.featured_image2",
    #      },
    # ),
    # # content 2 for blog post
    # (
    #     'mezzanine.blog.models.BlogPost.content2',
    #     "mezzanine.core.fields.RichTextField",
    #     ("Content 2",),
    #     {"blank": True,
    #      "null": True
    #      },
    # ),
    # # image 3 field for blog post
    # (
    #     # Dotted path to field.
    #     "mezzanine.blog.models.BlogPost.image3",
    #     # Dotted path to field class.
    #     "mezzanine.core.fields.FileField",
    #     # Positional args for field class.
    #     ("Image 3",),
    #     # Keyword args for field class.
    #     {"blank": True,
    #      "null": True,
    #      "upload_to": "blog",  # "blog.BlogPost.featured_image2",
    #      },
    # ),
    # # content 3 for blog post
    # (
    #     'mezzanine.blog.models.BlogPost.content3',
    #     "mezzanine.core.fields.RichTextField",
    #     ("Content 3",),
    #     {"blank": True,
    #      "null": True
    #      },
    # ),
    # # image 4 field for blog post
    # (
    #     # Dotted path to field.
    #     "mezzanine.blog.models.BlogPost.image4",
    #     # Dotted path to field class.
    #     "mezzanine.core.fields.FileField",
    #     # Positional args for field class.
    #     ("Image 4",),
    #     # Keyword args for field class.
    #     {"blank": True,
    #      "null": True,
    #      "upload_to": "blog",  # "blog.BlogPost.featured_image2",
    #      },
    # ),
    # # content 4 for blog post
    # (
    #     'mezzanine.blog.models.BlogPost.content4',
    #     "mezzanine.core.fields.RichTextField",
    #     ("Content 4",),
    #     {"blank": True,
    #      "null": True
    #      },
    # ),
    # # image 5 field for blog post
    # (
    #     # Dotted path to field.
    #     "mezzanine.blog.models.BlogPost.image5",
    #     # Dotted path to field class.
    #     "mezzanine.core.fields.FileField",
    #     # Positional args for field class.
    #     ("Image 5",),
    #     # Keyword args for field class.
    #     {"blank": True,
    #      "null": True,
    #      "upload_to": "blog",  # "blog.BlogPost.featured_image2",
    #      },
    # ),
    # # content 5 for blog post
    # (
    #     'mezzanine.blog.models.BlogPost.content5',
    #     "mezzanine.core.fields.RichTextField",
    #     ("Content 5",),
    #     {"blank": True,
    #      "null": True
    #      },
    # ),
    # # image 6 field for blog post
    # (
    #     # Dotted path to field.
    #     "mezzanine.blog.models.BlogPost.image6",
    #     # Dotted path to field class.
    #     "mezzanine.core.fields.FileField",
    #     # Positional args for field class.
    #     ("Image 6",),
    #     # Keyword args for field class.
    #     {"blank": True,
    #      "null": True,
    #      "upload_to": "blog",  # "blog.BlogPost.featured_image2",
    #      },
    # ),
    # # content 6 for blog post
    # (
    #     'mezzanine.blog.models.BlogPost.content6',
    #     "mezzanine.core.fields.RichTextField",
    #     ("Content 6",),
    #     {"blank": True,
    #      "null": True
    #      },
    # ),
    # blog post feature on home page
    (
        'mezzanine.blog.models.BlogPost.frontpage',
        "BooleanField",
        (_("Show on Home"),),
        {"default": False
         },
    ),
    (
        'mezzanine.blog.models.BlogPost.blogpage',
        "BooleanField",
        (_("Show on Blog List"),),
        {"default": False
         },
    ),
    ######## ProductVariation Extra Fields ##########
    # http://bitofpixels.com/blog/collecting-additional-information-on-a-per-product-basis-in-cartridge/
    # http://dodgyville.tumblr.com/post/23028930440/new-fields-in-mezzanine-without-editing-or
    # caveats important!!!
    # variation or product itself?
    (
        'cartridge.shop.models.ProductVariation.price_hkd',
        "cartridge.shop.fields.MoneyField",
        (_("Price HKD"),),
        {"blank": True,
         "null": True
         },
    ),
    (
        'cartridge.shop.models.ProductVariation.gold_member_price_hkd',
        "cartridge.shop.fields.MoneyField",
        (_("Gold Member Price HKD"),),
        {"blank": True,
         "null": True
         },
    ),
    (
        'cartridge.shop.models.ProductVariation.gold_member_price_rmb',
        "cartridge.shop.fields.MoneyField",
        (_("Gold Member Price RMB"),),
        {"blank": True,
         "null": True
         },
    ),
    (
        'cartridge.shop.models.ProductVariation.diamond_member_price_hkd',
        "cartridge.shop.fields.MoneyField",
        (_("Diamond Member Price HKD"),),
        {"blank": True,
         "null": True
         },
    ),
    (
        'cartridge.shop.models.ProductVariation.diamond_member_price_rmb',
        "cartridge.shop.fields.MoneyField",
        (_("Diamond Member Price RMB"),),
        {"blank": True,
         "null": True
         },
    ),
    ######## Order Extra Fields ##########
    (
        'cartridge.shop.models.Order.shipping_id',
        "cartridge.shop.fields.CharField",
        (_("Shipping ID"),),
        {"blank": True,
         "null": True,
         "max_length": 255
         },
    ),
    (
        'cartridge.shop.models.Order.shipping_url',
        "URLField",
        (_("Shipping URL"),),
        {"blank": True,
         "null": True,
         "max_length": 255
         },
    ),
    (
        'cartridge.shop.models.Order.payment_type',
        "CharField",
        (_("Payment Type"),),
        {"blank": True,
         "null": True,
         "max_length": 255
         },
    ),
    (
        'cartridge.shop.models.Order.source_id',
        "django.contrib.postgres.fields.JSONField",
        (_("Stripe Source ID"),),
        {"blank": True,
         "null": True,
         },
    ),
    (
        'cartridge.shop.models.Order.source_obj',
        "django.contrib.postgres.fields.JSONField",
        (_("Stripe Source Object"),),
        {"blank": True,
         "null": True,
         },
    ),
    (
        'cartridge.shop.models.Order.paid',
        "BooleanField",
        (_("Order paid"),),
        {"default": False,
         },
    ),
    (
        'cartridge.shop.models.Order.paid_time',
        "DateTimeField",
        (_("Order paid time"),),
        {"null":True}
    ),
    ########## Product Extra Fields #########
    (
        'cartridge.shop.models.Product.frontpage',
        "BooleanField",
        (_("Display on home products"),),
        {"default":False
         },
    ),
    (
        'cartridge.shop.models.Product.frontbanner',
        "BooleanField",
        (_("Display on home slider"),),
        {"default":False
         },
    ),
    (
        'cartridge.shop.models.Product.shoppage',
        "BooleanField",
        (_("Display product on shop page slider"),),
        {"default":False
         },
    ),
    (
        'cartridge.shop.models.Product.product_type',
        "cartridge.shop.fields.CharField",
        (_("Product Type"),),
        {"default":("regular",_("Regular")),
         "max_length": 255,
         "choices":[("regular",_("Regular")),
                     ("class",_("Class")),("fortune",_("Fortune")),("prayer",_("Prayer")),
                    ("numerology",_("Numerology")),("membership",_('Membership'))]}
    ),
    (
        'cartridge.shop.models.Product.is_membership_level',
        "BooleanField",
        (_("Is Membership"),),
        {"default": False
         },
    ),
    (
        'cartridge.shop.models.Product.is_class',
        "BooleanField",
        (_("Is Class"),),
        {"default": False
         },
    ),
    (
        'cartridge.shop.models.Product.is_fortune',
        "BooleanField",
        (_("Is Fortune"),),
        {"default": False
         },
    ),
    (
        'cartridge.shop.models.Product.num_sold',
        "IntegerField",
        (_("Number Sold"),),
        {"default": 0},
    ),
    (
        # Dotted path to field.
        "cartridge.shop.models.Product.featured_image",
        # Dotted path to field class.
        "mezzanine.core.fields.FileField",
        # Positional args for field class.
        (_("Featured Image"),),
        # Keyword args for field class.
        {"blank": True,
         "null": True,
         "upload_to": "product",
         },
    ),
    ######## Discount Extra Fields #########
    (
        'cartridge.shop.models.DiscountCode.membership_level',
        "cartridge.shop.fields.CharField",
        (_("Membership Level"),),
        {"null":True,
         "blank":True,
         "max_length": 255,
         "choices":[("regular",_("Regular")),("gold",_("Gold")),("diamond",_('diamond'))]}
    )
)