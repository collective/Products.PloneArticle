# -*- coding: utf-8 -*-

from zope.component import adapts
from zope.interface import implements
from plone.app.blob.field import BlobField

from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.field import ExtensionField

from Products.Archetypes.public import FileWidget
from Products.Archetypes.public import ImageWidget
from Products.PloneArticle.interfaces import IImageInnerContentProxy
from Products.PloneArticle.interfaces import IFileInnerContentProxy


class BlobFileField(ExtensionField, BlobField):
    """ A trivial ImageField """


class BlobImageField(ExtensionField, BlobField):
    """ A trivial File field """


class BaseSchemaExtender(object):

    fields = []

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields


class FileSchemaExtender(BaseSchemaExtender):
    adapts(IFileInnerContentProxy)
    implements(ISchemaExtender)

    fields = [
    BlobFileField(
        'attachedFile',
        attached_content=True,
        searchable=True,
        widget=FileWidget(
            label='Attached file',
            label_msgid='label_attached_file',
            i18n_domain='plonearticle',
            ),
        )
        ]


class ImageSchemaExtender(BaseSchemaExtender):
    adapts(IImageInnerContentProxy)
    implements(ISchemaExtender)
    fields = [
        BlobImageField(
            'attachedImage',
            attached_content=True,
            widget=ImageWidget(
                label='Attached image',
                label_msgid='label_attached_image',
                i18n_domain='plonearticle',
                ),
            ),
]
