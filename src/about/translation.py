from modeltranslation.translator import translator, TranslationOptions
from .models import Aboutpg, Terms, Privacy

class TranslatedAboutpg(TranslationOptions):
    fields = ('content1',)


class TranslatedTerms(TranslationOptions):
    fields = ('content',)

class TranslatedPrivacy(TranslationOptions):
    fields = ('content',)


translator.register(Aboutpg, TranslatedAboutpg)
translator.register(Terms, TranslatedTerms)
translator.register(Privacy, TranslatedPrivacy)
