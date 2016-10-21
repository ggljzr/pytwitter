from setuptools import setup, find_packages

with open('README') as f:
    long_description = ''.join(f.readlines())

setup(
    name='pytwitter',
    version='0.3',
    description='Finds and displays tweets either in terminal on via web frontend',
    long_description=long_description,
    author='Ondřej Červenka',
    author_email='cerveon3@fit.cvut.cz',
    keywords='twitter, cli, web',
    license='MIT',
    url='https://github.com/ggljzr/pytwitter',
    packages=find_packages(),
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: 3.5',
        'Framework :: Flask',
        'Topic :: Internet :: WWW/HTTP',
        '',
    ],
    entry_points={
        'console_scripts': ['pytwitter = pytwitter.pytwitter:main', ],
    },
)
