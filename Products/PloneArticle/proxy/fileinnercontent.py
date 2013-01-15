# -*- coding: utf-8 -*-
## Defines FileInnerContentField
## Copyright (C)2005 Ingeniweb

## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program; see the file COPYING. If not, write to the
## Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
"""
Defines FileInnerContentProxy
"""

__docformat__ = 'restructuredtext'

# Zope imports
from AccessControl import ClassSecurityInfo
from OFS.Image import File
from zope.interface import implements

# CMF imports
from Products.CMFCore import permissions as CCP

# Archetypes imports
from Products.Archetypes.public import StringField, \
    TextAreaWidget, registerType, Schema, ReferenceField, ComputedField, \
    ComputedWidget

# Products imports
try:
    from archetypes.referencebrowserwidget import ReferenceBrowserWidget
except ImportError:
    from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import \
        ReferenceBrowserWidget

from Products.ATContentTypes.interface import IFileContent
from Products.ATContentTypes.content.file import ATFile
from Products.PloneArticle.proxy import BaseFileContentProxy, \
     BaseInnerContentProxySchema
from Products.PloneArticle.interfaces import IFileInnerContentProxy

from Products.PloneArticle.config import PROJECTNAME

from Products.Archetypes.public import FileWidget
from plone.app.blob.field import FileField, BlobWrapper
#import usefull to download blob file
from webdav.common import rfc1123_date
from plone.app.blob.download import handleIfModifiedSince, handleRequestRange
from plone.i18n.normalizer.interfaces import IUserPreferredFileNameNormalizer
from Products.Archetypes.utils import contentDispositionHeader

INLINE_MIME_TYPES = ATFile.inlineMimetypes

# Defines schema
FileInnerContentProxySchema = BaseInnerContentProxySchema.copy() + Schema((
    ComputedField(
        'file',
        primary=True,
        expression="""context.getPrimaryValue('file', 'attachedFile', '')""",
        widget=ComputedWidget(
            label='File',
            label_msgid='label_file',
            i18n_domain='plonearticle',
            ),
        ),
    ReferenceField(
        'referencedContent',
        relationship='article_file',
        keepReferencesOnCopy=True,
        widget=ReferenceBrowserWidget(
            label='Referenced file',
            label_msgid='label_referenced_file',
            i18n_domain='plonearticle',
            ),
        ),
    FileField(
        'attachedFile',
        attached_content=True,
        searchable=True,
        widget=FileWidget(
            label='Attached file',
            label_msgid='label_attached_file',
            i18n_domain='plonearticle',
            ),
        ),
    ))


class FileInnerContentProxy(BaseFileContentProxy):
    """Proxy implementing IFileContent. It means this proxy has a getFile
    method.

    getFile returns attached file by default if existing otherwise returns
    the referenced content.
    """

    implements(IFileInnerContentProxy)
    security = ClassSecurityInfo()

    schema = FileInnerContentProxySchema

    # You can only reference content implementing IFileContent interface
    referenceable_interfaces = (IFileContent,)

    security.declareProtected(CCP.View, 'index_html')
    def index_html(self, REQUEST=None, RESPONSE=None):
        """Make it directly viewable when entering the objects URL.

        We have to reproduce it to keep the same behaviour as usual for files.
        """

        if REQUEST is None:
            REQUEST = self.REQUEST
        if RESPONSE is None:
            RESPONSE = REQUEST.RESPONSE
        field = self.getPrimaryField()
        accessor = field.getAccessor(self)
        data = accessor()

        #if not isinstance(data, File):
        #    return ''

        filename = data.filename
        content_type = data.getContentType()

        if not isinstance(data, BlobWrapper):
            return ''

        mime_type =  data.getContentType()
        if mime_type.startswith('text/'):
            return data

        if mime_type in INLINE_MIME_TYPES:
            content_dispo = 'inline'
        else:
            content_dispo = 'attachment'
        #RESPONSE.setHeader(
        #    'Content-Disposition',
        #    '%s; filename="%s"' % (content_dispo, data.filename or self.getId()))

        #little bit tricky: if we are using reference field, fallback to
        # defautl code, other case, we need to handle the blob file. The code in
        # the else branch is taken directly from plone.app.blob.field.py
        att_field = self.getField('attachedFile')
        if not att_field.get_size(self) > 0:
            RESPONSE.setHeader(
            'Content-Disposition',
            '%s; filename="%s"' % (content_dispo, (filename or self.getId())))
            return data.index_html(REQUEST, RESPONSE)
        else:
            return att_field.index_html(self, REQUEST, RESPONSE)

    def setAttachedFile(self, value, **kwargs):
        """
        Rename proxy according to file name
        """
        field = self.getField('attachedFile')
        field.set(self, value, **kwargs)
        self.renameFromFileName(field)

registerType(FileInnerContentProxy, PROJECTNAME)
