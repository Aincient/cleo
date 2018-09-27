from django.db import models

from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
    StreamFieldPanel
)

from wagtail.core.models import Orderable, Page
from wagtail.core.fields import RichTextField
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField

from wagtailtrans.models import TranslatablePage

from wagtail.search import index

from .blocks import BaseStreamBlock

class TranslatablePageMixin(models.Model):
    # One link for each alternative language
    # These should only be used on the main language page (english)
    dutch_link = models.ForeignKey(Page, null=True, on_delete=models.SET_NULL, blank=True, related_name='+')

    def get_language(self):
        """
        This returns the language code for this page.
        """
        # Look through ancestors of this page for its language homepage
        # The language homepage is located at depth 3
        language_homepage = self.get_ancestors(inclusive=True).get(depth=3)

        # The slug of language homepages should always be set to the language code
        return language_homepage.slug


    # Method to find the main language version of this page
    # This works by reversing the above links

    def english_page(self):
        """
        This finds the english version of this page
        """
        language = self.get_language()

        if language == 'en':
            return self
        elif language == 'nl':
            return type(self).objects.filter(dutch_link=self).first().specific


    # We need a method to find a version of this page for each alternative language.
    # These all work the same way. They firstly find the main version of the page
    # (english), then from there they can just follow the link to the correct page.

    def dutch_page(self):
        """
        This finds the french version of this page
        """
        dutch_page = self.dutch_page()

        if dutch_page and dutch_page.dutch_link:
            return dutch_page.dutch_link.specific

    class Meta:
        abstract = True

class HomePageBlock(models.Model):
    background_color = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    body = models.CharField(max_length=255)
    
    panels = [
        FieldPanel('background_color'),
        FieldPanel('title'),
        FieldPanel('body'),
    ]

    class Meta:
        abstract = True


class HomePageBlockLink(Orderable, HomePageBlock):
    page = ParentalKey('cms.HomePage', on_delete=models.CASCADE, related_name='homepage_blocks')


class HomePage(TranslatablePage, Page):

    template="cms/base/home_page.html"
    
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Homepage image'
    )

    hero_text = RichTextField()

    hero_cta = models.CharField(
        verbose_name='Hero CTA',
        max_length=255,
        help_text='Text to display on Call to Action',
        blank=True
        )

    hero_cta_link = models.CharField(
        verbose_name='Hero Link',
        max_length=255,
        help_text='Hero Link',
        blank=True
        )

    sub_hero_block = RichTextField(blank=True)
    
    body = StreamField(
        BaseStreamBlock(), verbose_name="Home content block", blank=True
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            ImageChooserPanel('image'),
            FieldPanel('hero_text', classname="full"),
            MultiFieldPanel([
                FieldPanel('hero_cta'),
                FieldPanel('hero_cta_link'),
                FieldPanel('sub_hero_block'),
                ])
            ], heading="Hero section"),
            StreamFieldPanel('body'),
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Home'
        

class ContentPage(TranslatablePage, Page):
    body = RichTextField(blank=True)
    template="cms/base/content_page.html"

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Header image'
    )

    body = StreamField(
        BaseStreamBlock(), verbose_name="Page body", blank=True
    )

    content_panels = Page.content_panels + [
        ImageChooserPanel('image'),
        StreamFieldPanel('body'),
    ]

@register_snippet
class FooterText(models.Model):
    """
    This provides editable text for the site footer. Again it uses the decorator
    `register_snippet` to allow it to be accessible via the admin. It is made
    accessible on the template via a template tag defined in base/templatetags/
    navigation_tags.py
    """
    body = RichTextField()

    panels = [
        FieldPanel('body'),
    ]

    def __str__(self):
        return "Footer text"

    class Meta:
        verbose_name_plural = 'Footer Text'

@register_snippet
class CookieTextEN(models.Model):
    """
    This provides editable text for the site footer. Again it uses the decorator
    `register_snippet` to allow it to be accessible via the admin. It is made
    accessible on the template via a template tag defined in base/templatetags/
    navigation_tags.py
    """
    body = RichTextField()

    panels = [
        FieldPanel('body'),
    ]

    def __str__(self):
        return "Cookie text EN"

    class Meta:
        verbose_name_plural = 'Cookie text EN'


@register_snippet
class CookieTextNL(models.Model):
    """
    This provides editable text for the site footer. Again it uses the decorator
    `register_snippet` to allow it to be accessible via the admin. It is made
    accessible on the template via a template tag defined in base/templatetags/
    navigation_tags.py
    """
    body = RichTextField()

    panels = [
        FieldPanel('body'),
    ]

    def __str__(self):
        return "Cookie text NL"

    class Meta:
        verbose_name_plural = 'Cookie text NL'



class FormField(AbstractFormField):
    """
    Wagtailforms is a module to introduce simple forms on a Wagtail site. It
    isn't intended as a replacement to Django's form support but as a quick way
    to generate a general purpose data-collection form or contact form
    without having to write code. We use it on the site for a contact form. You
    can read more about Wagtail forms at:
    http://docs.wagtail.io/en/latest/reference/contrib/forms/index.html
    """
    page = ParentalKey('FormPage', related_name='form_fields', on_delete=models.CASCADE)


class FormPage(TranslatablePage, AbstractEmailForm):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    template="cms/base/form_page.html"
    body = StreamField(BaseStreamBlock())
    thank_you_text = RichTextField(blank=True)

    # Note how we include the FormField object via an InlinePanel using the
    # related_name value
    content_panels = AbstractEmailForm.content_panels + [
        ImageChooserPanel('image'),
        StreamFieldPanel('body'),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]

class ExplorePage(Page):
    """
    Detail view for a specific Explore options
    """

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Header image'
    )

    desciption = RichTextField(blank=True)


    content_panels = Page.content_panels + [
        ImageChooserPanel('image'),
        FieldPanel('desciption'),
    ]

    parent_page_types = ['ExploreIndexPage']

class ExploreIndexPage(Page):
    """
    Index page for explore options.
    This is more complex than other index pages on the bakery demo site as we've
    included pagination. We've separated the different aspects of the index page
    to be discrete functions to make it easier to follow
    """
    # Can only have BreadPage children
    subpage_types = ['ExplorePage']

    def children(self):
        return self.get_children().specific().live()


class PaymenOptionPage(Page):
    """
    Detail view for a specific Explore options
    """
    
    options = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('options'),
    ]

    parent_page_types = ['PaymenOptionIndexPage']

class PaymenOptionIndexPage(Page):
    """
    Index page for payment options.
    This is more complex than other index pages on the bakery demo site as we've
    included pagination. We've separated the different aspects of the index page
    to be discrete functions to make it easier to follow
    """

    classname = models.CharField(
        max_length=255,
        help_text='classname',
        blank=True
        )

    # Can only have BreadPage children
    subpage_types = ['PaymenOptionPage']

    def children(self):
        return self.get_children().specific().live()
