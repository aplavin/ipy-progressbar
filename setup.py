from setuptools import setup


try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = ''

setup(name='ipy-progressbar',
      version='1.0.2',
      description='Progressbar for both IPython Notebooks (HTML, CSS, JS) and plain terminals.',
      long_description = long_description,
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: IPython',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: Terminals',
      ],
      keywords='progress progressbar terminal console ipython notebook',
      url='https://hg.plav.in/my_projects/python/ipy-progressbar',
      author='Alexander Plavin',
      author_email='alexander@plav.in',
      license='MIT',
      packages=['ipy_progressbar'],
      zip_safe=False)
