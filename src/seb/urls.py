from __future__ import unicode_literals

from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.views.i18n import set_language
from mezzanine.core.views import direct_to_template
from mezzanine.conf import settings
import mezzanine

from cartridge.shop.views import order_history

from patches.views import product, cart, checkout_steps_patch, track_order, home_view, blog_post_list
from profiles.views import signup_view

# from machina.app import board

_slash = "/" if settings.APPEND_SLASH else ""



admin.autodiscover()

# Add the urlpatterns for any custom Django applications here.
# You can also change the ``home`` view to add your own functionality
# to the project's homepage.

urlpatterns = i18n_patterns(
    # Change the admin prefix here to use an alternate URL for the
    # admin interface, which would be marginally more secure.
    url("^admin/", include(admin.site.urls)),
    # MY URLS
    # url(r'^test/',include("patches.urls", namespace='test')),
    # url(r'^about1/$', about1, name='about1'),
    url("^profile/", include("profiles.urls")),
    url("^fortune/", include("fortune.urls", namespace="fortune")),
    url("^about/", include("about.urls")),
    url("^payments/", include("payments.urls", namespace="payments")),

)

if settings.USE_MODELTRANSLATION:
    urlpatterns += [
        url('^i18n/$', set_language, name='set_language'),
    ]

blog_installed = "mezzanine.blog" in settings.INSTALLED_APPS
if blog_installed:
    BLOG_SLUG = settings.BLOG_SLUG.rstrip("/")

ACCOUNT_URL = getattr(settings, "ACCOUNT_URL", "/accounts/")
SIGNUP_URL = getattr(settings, "SIGNUP_URL",
                     "/%s/signup/" % ACCOUNT_URL.strip("/"))

_slash = "/" if settings.APPEND_SLASH else ""


urlpatterns += [

    # Blog replacements
    url("^%s/category/(?P<category>.*)%s$" % (BLOG_SLUG, _slash),
        blog_post_list, name="blog_post_list_category"),
    url("^%s/author/(?P<username>.*)%s$" % (BLOG_SLUG, _slash),
        blog_post_list, name="blog_post_list_author"),
    url("^%s/archive/(?P<year>\d{4})/(?P<month>\d{1,2})%s$" % (BLOG_SLUG, _slash),
        blog_post_list, name="blog_post_list_month"),
    url("^%s/archive/(?P<year>\d{4})%s$" % (BLOG_SLUG, _slash),
        blog_post_list, name="blog_post_list_year"),
    url("^%s/$" % BLOG_SLUG, blog_post_list, name="blog_post_list"),

    # Cartridge replacements
    url("^shop/product/(?P<slug>.*)%s$" % _slash, product,
        name="shop_product"),
    url("^shop/cart%s$" % _slash, cart, name="shop_cart"),
    url("^shop/checkout%s$" % _slash, checkout_steps_patch, name="shop_checkout"),
    url("^shop/track_order/(?P<order_id>\d+)%s$" % _slash, track_order, name="track_order"),

    # Cartridge URLs.
    url("^shop/", include("cartridge.shop.urls")),
    url("^account/orders/$", order_history, name="shop_order_history"),
    url("^%s%s$" % (SIGNUP_URL.strip("/"), _slash), signup_view, name="signup"),

    # MACHINA FORUM PAGES
    # ________________________________
    # url(r'^markdown/', include('django_markdown.urls')),
    # url(r'^forum/', include(board.urls)),

    # We don't want to presume how your homepage works, so here are a
    # few patterns you can use to set it up.

    # Homepage as a regular view
    url("^$", home_view, name="home"),

    # HOMEPAGE AS STATIC TEMPLATE
    # ---------------------------
    # This pattern simply loads the index.html template. It isn't
    # commented out like the others, so it's the default. You only need
    # one homepage pattern, so if you use a different one, comment this
    # one out.

    # url("^$", direct_to_template, {"template": "index.html"}, name="home"),

    # HOMEPAGE AS AN EDITABLE PAGE IN THE PAGE TREE
    # ---------------------------------------------
    # This pattern gives us a normal ``Page`` object, so that your
    # homepage can be managed via the page tree in the admin. If you
    # use this pattern, you'll need to create a page in the page tree,
    # and specify its URL (in the Meta Data section) as "/", which
    # is the value used below in the ``{"slug": "/"}`` part.
    # Also note that the normal rule of adding a custom
    # template per page with the template name using the page's slug
    # doesn't apply here, since we can't have a template called
    # "/.html" - so for this case, the template "pages/index.html"
    # should be used if you want to customize the homepage's template.
    # NOTE: Don't forget to import the view function too!

    # url("^$", mezzanine.pages.views.page, {"slug": "/"}, name="home"),

    # HOMEPAGE FOR A BLOG-ONLY SITE
    # -----------------------------
    # This pattern points the homepage to the blog post listing page,
    # and is useful for sites that are primarily blogs. If you use this
    # pattern, you'll also need to set BLOG_SLUG = "" in your
    # ``settings.py`` module, and delete the blog page object from the
    # page tree in the admin if it was installed.
    # NOTE: Don't forget to import the view function too!

    # url("^$", mezzanine.blog.views.blog_post_list, name="home"),

    # MEZZANINE'S URLS
    # ----------------
    # ADD YOUR OWN URLPATTERNS *ABOVE* THE LINE BELOW.
    # ``mezzanine.urls`` INCLUDES A *CATCH ALL* PATTERN
    # FOR PAGES, SO URLPATTERNS ADDED BELOW ``mezzanine.urls``
    # WILL NEVER BE MATCHED!

    # If you'd like more granular control over the patterns in
    # ``mezzanine.urls``, go right ahead and take the parts you want
    # from it, and use them directly below instead of using
    # ``mezzanine.urls``.
    url("^", include("mezzanine.urls")),

    # MOUNTING MEZZANINE UNDER A PREFIX
    # ---------------------------------
    # You can also mount all of Mezzanine's urlpatterns under a
    # URL prefix if desired. When doing this, you need to define the
    # ``SITE_PREFIX`` setting, which will contain the prefix. Eg:
    # SITE_PREFIX = "my/site/prefix"
    # For convenience, and to avoid repeating the prefix, use the
    # commented out pattern below (commenting out the one above of course)
    # which will make use of the ``SITE_PREFIX`` setting. Make sure to
    # add the import ``from django.conf import settings`` to the top
    # of this file as well.
    # Note that for any of the various homepage patterns above, you'll
    # need to use the ``SITE_PREFIX`` setting as well.

    # url("^%s/" % settings.SITE_PREFIX, include("mezzanine.urls"))



]

# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
