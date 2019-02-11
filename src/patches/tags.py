# from django import template
# from sorl.thumbnail import get_thumbnail
# from mezzanine.core.templatetags import mezzanine_tags


# used to replace normal mezz {% thumbnail tag %} with sorl.
# not useful at this point
# register = template.get_library("mezzanine_tags")

# https://github.com/mariocesar/sorl-thumbnail
# @register.simple_tag
# def thumbnail(image_url, width, height, quality=95, left=0.5, top=0.5):
#     im = get_thumbnail(image_url, "%sx%s" % (width, height), crop='center', quality=quality)
#     return im.url
#
# mezzanine_tags.thumbnail = thumbnail