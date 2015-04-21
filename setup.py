from distutils.core import setup

setup(name='markdown_toclify',
      version='0.1.7',
      description='A Python module to adda a Table of Contents with internal section-links to Markdown documents.',
      author='Sebastian Raschka',
      author_email='se.raschka@gmail.com',
      url='https://github.com/rasbt/markdown-toclify',
      packages=['markdown_toclify',
                ],
      data_files = [('', ['LICENSE']),
                    ('', ['README.md']),
                    ('', ['CHANGELOG.txt']),
                   ],
      license='GPLv3',
      platforms='any',
      classifiers=[
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Development Status :: 5 - Production/Stable',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 2',
      ],
      long_description="""

A Python module to adda a Table of Contents with internal section-links to Markdown documents.


Contact
=============

If you have any questions or comments about mlxtend, please feel free to contact me via
eMail: se.raschka@gmail.com
or Twitter: https://twitter.com/rasbt

This project is hosted at https://github.com/rasbt/markdown-toclify

""",
    )
