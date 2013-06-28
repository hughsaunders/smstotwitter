from setuptools import setup

setup(
    name='smstotwitter',
    version='0.1',
    packages=['smstotwitter'],
    author='Hugh Saunders',
    author_email='hugh@wherenow.org',
    install_requires=open('pip-requires.txt').readlines()
)

