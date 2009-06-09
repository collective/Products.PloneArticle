from setuptools import setup, find_packages
import os

version = '4.1.4'

setup(name='Products.PloneArticle',
      version=version,
      description="A Plone document including images, attachments and links, with a free choice of layout.",
      long_description=open(os.path.join("Products", "PloneArticle", "README.txt")).read() + "\n\n",
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Ingeniweb',
      author_email='support@ingeniweb.com',
      url='http://plone.org/products/plonearticle',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
