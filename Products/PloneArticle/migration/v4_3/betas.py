# -*- coding: utf-8 -*-
## 
## Copyright (C) 2008 Ingeniweb

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
Plone Article migration module from 4.2 to 4.3 betas
"""
__version__ = "$Revision:  $"
# $Source:  $
# $Id:  $
__docformat__ = 'restructuredtext'


from Products.PloneArticle import LOG as logger
from plone.app.blob.migrations import migrate as migrateBlob


def stable4110_430beta1(portal):
    portal_types = ['FileInnerContentProxy', 'ImageInnerContentProxy']
    out = []
    logger.info("------------- Starting migrating PloneArticle contents to BLOB -------------")
    from Products.contentmigration.basemigrator.walker import MigrationError
    for portal_type in portal_types:
        logger.info("** migrating %s types **" % portal_type)
        try:
            output = migrateBlob(portal, portal_type, portal_type).splitlines()
            for msg in output:
                logger.info("    %s" % msg)
        except MigrationError:
            logger.warning("Error migrating to BLOB")
    logger.info("Migrated PloneArticle to BLOB")
    out.append("Migrated PloneArticle to BLOB")
    return out
