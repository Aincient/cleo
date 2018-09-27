from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.core.blocks import (
    CharBlock, ChoiceBlock, RichTextBlock, StreamBlock, StructBlock, TextBlock, URLBlock, PageChooserBlock
)
from django.db import models

from wagtail.core.models import Orderable, Page


class ImageBlock(StructBlock):
    """
    Custom `StructBlock` for utilizing images with associated caption and
    attribution data
    """
    anchor = CharBlock(required=False)
    title = CharBlock(required=False)
    image = ImageChooserBlock(required=True)
    caption = CharBlock(required=False)
    background_color = CharBlock(required=False)
    color = CharBlock(required=False)

    class Meta:
        icon = 'image'
        template = "cms/blocks/image_block.html"


class HeadingBlock(StructBlock):
    """
    Custom `StructBlock` that allows the user to select h2 - h4 sizes for headers
    """
    heading_text = CharBlock(classname="title", required=True)
    size = ChoiceBlock(choices=[
        ('', 'Select a header size'),
        ('h2', 'H2'),
        ('h3', 'H3'),
        ('h4', 'H4')
    ], blank=True, required=False)

    class Meta:
        template = "cms/blocks/heading_block.html"


class BlockQuote(StructBlock):
    """
    Custom `StructBlock` that allows the user to attribute a quote to the author
    """
    text = TextBlock()
    attribute_name = CharBlock(
        blank=True, required=False, label='e.g. Mary Berry')

    class Meta:
        template = "cms/blocks/blockquote.html"

class BlockCTA(StructBlock) :
    """
    Custom CTA block with options
    """
    text = RichTextBlock()
    cta_title = CharBlock(required=True)
    link = URLBlock()
    anchor = CharBlock(required=True)
    image = ImageChooserBlock(required=False)
    
    classname = CharBlock(required=True)

    background_color = CharBlock(required=True)
    color = CharBlock(required=True)

    class Meta:
        template = "cms/blocks/cta_block.html"

class ColumnBlock(StructBlock):
    """
    Custom block
    """
    heading_text = CharBlock(classname="title", required=True)
    sub_text = CharBlock(classname="sub_title", blank=True, required=False)
    
    anchor = CharBlock(required=True)
    
    classname = CharBlock(required=True)

    background_color = CharBlock(required=True)
    color = CharBlock(required=True)

    left_block = RichTextBlock()
    right_block = RichTextBlock()

    class Meta:
        template = "cms/blocks/column_block.html"


class FeaturedBlock(StructBlock):
    """
    Custom block
    """
    heading_text = CharBlock(classname="title", required=True)
    sub_text = CharBlock(classname="sub_title", blank=True, required=False)
    
    featured_section = PageChooserBlock()

    anchor = CharBlock(required=True)
    
    classname = CharBlock(required=True)

    background_color = CharBlock(required=True)
    color = CharBlock(required=True)

    class Meta:
        template = "cms/blocks/featured_block.html"


# StreamBlocks
class BaseStreamBlock(StreamBlock):
    """
    Define the custom blocks that `StreamField` will utilize
    """
    heading_block = HeadingBlock()
    paragraph_block = RichTextBlock(
        template="cms/blocks/paragraph_block.html"
    )
    image_block = ImageBlock()
    block_quote = BlockQuote()
    cta_block = BlockCTA()
    column_block = ColumnBlock()
    featured_block = FeaturedBlock()
    embed_block = EmbedBlock(
        help_text='Insert an embed URL e.g https://www.youtube.com/embed/SGJFWirQ3ks',
        template="cms/blocks/embed_block.html")