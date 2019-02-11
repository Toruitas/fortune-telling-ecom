from datetime import date
from django.db import models
from mezzanine.pages.models import Page
from mezzanine.core.fields import RichTextField

# Create your models here.
# The members of Page will be inherited by the Author model, such
# as title, slug, etc. For authors we can use the title field to
# store the author's name. For our model definition, we just add
# any extra fields that aren't part of the Page model, in this
# case, date of birth.
# basically, create models and fields and it will find a page called modelname.html to render it.
# don't forget to register in admin~~


class Aboutpg(Page):
    """
    http://stackoverflow.com/questions/13930678/mezzanine-rich-text-field
    """
    content1 = RichTextField("Content1")  # ex mission
    # content2 = RichTextField("Content2")  # ex techniques
    image1 = models.ImageField(upload_to="about")  # ex team shot
    # image2 = models.ImageField(upload_to="about")  # ex action shot


    # def can_add(self, request):
    #     return self.children.count() == 0

    # def can_delete(self, request):
    #     return request.user.is_superuser or self.parent is not None
    #
    # def can_move(self, request, new_parent):
    #     if new_parent is None:
    #         msg = 'An author page cannot be a top-level page'
    #         raise PageMoveException(msg)


class Employee(models.Model):
    # not necessary maybe
    belongs_to = models.ForeignKey("Aboutpg")
    name = models.CharField(null=False, blank=False, max_length=120)
    photo = models.ImageField(upload_to="employee")
    signature = models.ImageField(upload_to="employee")
    date_joined = models.DateField("Date joined", default=date.today)
    bio = RichTextField("Bio")


class Terms(Page):
    content = RichTextField("Content")


class Privacy(Page):
    # http://www.website-contracts.co.uk/our-terms-and-conditions.html
    # http://www.contractology.com/free-website-terms-and-conditions.html
    content = RichTextField("Content")