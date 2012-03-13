from setuptools import setup, find_packages
from setuptools import Command
import sys, os

version = '0.1.0b'

class PyTest(Command):
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        import sys,subprocess
        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)

setup(name='kotti_events',
      version=version,
      description="Event collection for Kotti sites",
      long_description="""\
This is an extension to Kotti that allows to add collections of events to your website.
Development happens at https://github.com/chrneumann/kotti_events
""",
      classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "License :: OSI Approved :: BSD License",
        ],
      keywords='kotti contact form',
      author='Christian Neumann',
      author_email='christian@datenkarussell.de',
      url='http://pypi.python.org/pypi/kotti_events',
      license='BSD License',
      packages=['kotti_events'],
      package_data={'kotti_events': [
            'static/*',
            'templates/*.pt',
            'locale/*.*',
            'locale/*/LC_MESSAGES/*.*']},
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'Kotti',
        'Babel',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      message_extractors = { "kotti_events": [
        ("**.py",   "lingua_python", None ),
        ("**.pt",   "lingua_xml", None ),
        ]},
      cmdclass = {'test': PyTest},
      )
