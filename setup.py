from setuptools import setup, find_packages


setup(
    name="duoshuo-python-sdk",
    version="0.1.2",
    description="A Python library for using the duoshuo API",
    long_description=open('README.md').read(),
    author="Perchouli",
    author_email="jp.chenyang@gmail.com",
    maintainer="njuaplusplus",
    maintainer_email="njuaplusplus@gmail.com",
    url="https://github.com/njuaplusplus/duoshuo-python-sdk",
    packages=find_packages(),
    package_data={
        'duoshuo' : ['*.json',]
    },
    install_requires=[
        'PyJWT',
        'requests>=0.14.0'
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    include_package_data=True,
    zip_safe=False,
)
