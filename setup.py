from distutils.core import setup

setup(
    name='rightshift',
    version='0.1.0',
    packages=['rightshift'],
    url='https://github.com/OOPMan/rightshift',
    license='MIT',
    author='Adam Jorgensen',
    author_email='adam.jorgensen.za@gmail.com',
    description='RightShift is a Python package for writing chained operations in a readable fashion.',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=['future>=0.16.0'],
    tests_require=['hypothesis']
)
