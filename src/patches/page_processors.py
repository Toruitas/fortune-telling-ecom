from django import forms
from django.http import HttpResponseRedirect
from django.template.defaultfilters import slugify
from mezzanine.pages.page_processors import processor_for
from mezzanine.conf import settings
from mezzanine.pages.page_processors import processor_for
from mezzanine.utils.views import paginate
from cartridge.shop.models import Category, Product, DiscountCode# from .models import Author

from el_pagination.decorators import page_template


# class AuthorForm(forms.Form):
#     name = forms.CharField()
#     email = forms.EmailField()
#
# @processor_for(Author)
# def author_form(request, page):
#     form = AuthorForm()
#     if request.method == "POST":
#         form = AuthorForm(request.POST)
#         if form.is_valid():
#             # Form processing goes here.
#             redirect = request.path + "?submitted=true"
#             return HttpResponseRedirect(redirect)
#     return {"form": form}


# @page_template('pages/category_page.html')
@processor_for(Category, exact_page=True)
def category_processor(request, page, extra_context=None):
    """
    Add paging/sorting to the products for the category.
    """
    settings.use_editable()
    products = Product.objects.published(for_user=request.user
                                ).filter(page.category.filters()).distinct()
    featured_products = Product.objects.published(for_user=request.user
                                ).filter(shoppage=True
                                         ).distinct().order_by('-publish_date')[:4]
    sort_options = [(slugify(option[0]), option[1])
                    for option in settings.SHOP_PRODUCT_SORT_OPTIONS]
    sort_by = request.GET.get("sort", sort_options[0][1])
    products = paginate(products.order_by(sort_by),
                        request.GET.get("page", 1),
                        settings.SHOP_PER_PAGE_CATEGORY,
                        settings.MAX_PAGING_LINKS)
    products.sort_by = sort_by
    sub_categories = page.category.children.published()
    child_categories = Category.objects.filter(id__in=sub_categories)
    classes_category = Category.objects.get(slug="shop/classes")
    # find prices to display for each product
    products_discounts = []
    for p in products.object_list:
        # create list of tuples, then iterate through them in template
            try:
                discount = DiscountCode.objects.filter(title="{}+{}".format(p.sku,request.user.membership.level))[0]
                discount_deduction = discount.discount_deduct
            except:
                discount_deduction = 0
            products_discounts.append((p,discount_deduction))
    # try:
    #     discount = DiscountCode.objects.filter(title=request.user.membership.level)[0]
    #     discount_percent = (100 - discount.discount_percent)/ 100
    # except:
    #     discount_percent = 1
    context = {"products": products,
               "featured_products":featured_products,
               "child_categories": child_categories,
               "classes_category":classes_category,
               "products_discounts": products_discounts,
               'page_template': 'pages/category_page.html',
               }
    # print(sort_options)
    # if extra_context is not None:
    #
    # if request.is_ajax():
    #     template = page_template
    #     context.update({"template":template})
    return context
