from datetime import datetime
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _

from cartridge.shop.models import Product, ProductVariation, Order, DiscountCode,Category

from .CalendarConvert import Get8Zi
from .forms import FortuneForm


def fortune_view(request, template="fortune/fortune_form.html",
                 extra_context=None):
    """
    form: fortuneform
    initial data: prefill with user's profile birthday, but don't update if they change it. Allow that to be changed
    on profile page though.

    http://www.fengshui-village.com/en/bazi.php
    http://feng-shui.lovetoknow.com/Feng_Shui_Elements_Based_on_Birthday
    http://www.fengshuimastersingapore.sg/birth-profile/
    https://www.travelchinaguide.com/intro/astrology/four-pillar.htm
    http://www.fourpillars.net/calculator.php
    http://www.wofs.com/index.php?option=com_jumi&fileid=6
    http://www.my8z.com/toolscode.php
    https://github.com/mattxlee/eightwords
    http://blog.csdn.net/luozhuang/article/details/8678846
    http://www.oschina.net/code/snippet_1178728_33431      THIS ONE MAKES SENSE
    http://www.cnblogs.com/hhh5460/p/4302499.html
    https://github.com/swordzjj/PyLunar

    todo: add CalendarConvert to view.
    todo: link static img urls of Kiki's calligraphy to the image urls.
    todo: find out what this means.

    :param request:
    :return:
    """
    # birthday form
    # present or
    # process, turn into datetime obj? Or directly into ints?
    # calculate w/ Get8Zi
    # use character pairs to find the appropriate img url from static/img/8chars
    # in template, use interpolation {% static img/8chars/{{子子}}.jpg %}
    # show other descriptions for the fortune
    form = FortuneForm(request.POST or None)
    # if request.method == "POST":
    #     print(request.POST)
    if request.method == "POST" and form.is_valid():
        # print(form.cleaned_data)
        data = form.cleaned_data
        birthdate = datetime.combine(data['birthday'], data['birthtime'])
        year, month, day, hour, minute, *args = birthdate.timetuple()  # *args to catch extra useless data
        # print(birthdate)
        # print(Get8Zi(year, month, day, hour, min))
        # 四柱 + 考时   十字
        # print(year, month, day, hour, minute)
        # will error out if time is in future
        year, month, day, hour, minute = Get8Zi(year, month, day, hour, minute)
        char_pairs = (
            ("甲子","丙子","戊子","庚子","壬子"),
            ("乙丑","丁丑","己丑","辛丑","癸丑"),
            ("丙寅","戊寅","庚寅","壬寅","甲寅"),
            ("丁卯","己卯","辛卯","癸卯","乙卯"),
            ("戊辰","庚辰","壬辰","甲辰","丙辰"),
            ("己巳","辛巳","癸巳","乙巳","丁巳"),
            ("庚午","壬午","甲午","丙午","戊午"),
            ("辛未","癸未","乙未","丁未","己未"),
            ("壬申","甲申","丙申","戊申","庚申"),
            ("癸酉","乙酉","丁酉","己酉","辛酉"),
            ("甲戌","丙戌","戊戌","庚戌","壬戌"),
            ("乙亥","丁亥","己亥","辛亥","癸亥")
        )
        single_chars = ['甲', '子', '丙', '戊', '庚', '壬', '乙', '丑', '丁', '己', '辛',
                        '癸', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
        # ten heavenly stems
        ten_stems = {"甲": ("Jia", 1, _("Yang"), _("Wood")), "乙": ("Yi", 2, _("Yin"), _("Wood")),
                     "丙": ("Bing", 3, _("Yang"), _("Fire")), "丁": ("Ding", 4, _("Yin"), _("Fire")),
                     "戊": ("Wu", 5, _("Yang"), _("Earth")), "己": ("Ji", 6, _("Yin"), _("Earth")),
                     "庚": ("Geng", 7, _("Yang"), _("Metal")), "辛": ("Xin", 8, _("Yin"), _("Metal")),
                     "壬": ("Ren", 9, _("Yang"), _("Water")), "癸": ("Gui", 10, _("Yin"), _("Water"))}
        # twelve earthly branches
        # # twelve earthly branches
        twelve_branches = {"子": ("Zi", 1, _("Yang"), _("Water"), _("Rat")),
                           "丑": ("Chou", 2, _("Ying"), _("Earth"), _("Ox")),
                           "寅": ("Yin", 3, _("Yang"), _("Wood"), _("Tiger")),
                           "卯": ("Mao", 4, _("Ying"), _("Wood"), _("Rabbit")),
                           "辰": ("Chen", 5, _("Yang"), _("Earth"), _("Dragon")),
                           "巳": ("Si", 6, _("Ying"), _("Fire"), _("Snake")),
                           "午": ("Wu", 7, _("Yang"), _("Fire"), _("Horse")),
                           "未": ("Wei", 8, _("Ying"), _("Earth"), _("Goat")),
                           "申": ("Shen", 9, _("Yang"), _("Metal"), _("Monkey")),
                           "酉": ("You", 10, _("Ying"), _("Metal"), _("Rooster")),
                           "戌": ("Xu", 11, _("Yang"), _("Earth"), _("Dog")),
                           "亥": ("Hai", 12, _("Ying"), _("Water"), _("Pig"))}
        ten_chars = (year, month, day, hour, minute)
        times = [_("Year"),_("Month"),_("Day"),_("Hour"),_("Minute")]
        displayed_chars = []
        for i, pair in enumerate(ten_chars):
            displayed_chars.append((times[i], pair, ten_stems[pair[0]], twelve_branches[pair[1]]))
        # print(displayed_chars)
        template = "fortune/fortune_display.html"
        context = {"displayed_chars": displayed_chars[:-1],
                   "meta_title": _("Your 8 Characters"),
                   "title": _("Your 8 Characters"),}
        return TemplateResponse(request, template, context)
        #     return redirect("fortune_display", ten_chars="".join(ten_chars))
    context = {"form": form, "title": _("Ba Zi Fortune"), "button_text":_("Get your Ba Zi")}
    context.update(extra_context or {})
    return TemplateResponse(request, template, context)


def fortune_display_view(request, template="fortune/fortune_display.html",
                 extra_context=None):
    """
    This is a dummy/test view

    :param request:
    :param template:
    :param extra_context:
    :return:
    """
    dummy = [('Year', '丙申', ('Bing', 3, 'Yang', 'Fire'), ('Shen', 9, 'Yang', 'Metal', 'Monkey')),
     ('Month', '壬子', ('Ren', 9, 'Yang', 'Water'), ('Zi', 1, 'Yang', 'Water', 'Rat')),
     ('Day', '戊子', ('Wu', 5, 'Yang', 'Earth'), ('Zi', 1, 'Yang', 'Water', 'Rat')),
     ('Hour', '丁巳', ('Ding', 4, 'Yin', 'Fire'), ('Si', 6, 'Yin', 'Fire', 'Snake')),
     ('Minute', '己酉', ('Ji', 6, 'Yin', 'Earth'), ('You', 10, 'Yin', 'Metal', 'Rooster'))]

    context = {"meta_title": _("Eight Characters Fortune"), "displayed_chars": dummy}
    return TemplateResponse(request, template, context)


def prayers_view(request, template="fortune/prayers.html",extra_context=None):
    """
    Perhaps a better term would be "dispel" or clear out demons/curses etc
    :param request:
    :param template:
    :param extra_context:
    :return:
    """
    prayers = Product.objects.filter(is_fortune=True)
    prayers = prayers[:8]
    context = {"meta_title": _("Prayers"),
               "title": _("Prayers"),
               "prayers":prayers}
    return TemplateResponse(request, template, context)