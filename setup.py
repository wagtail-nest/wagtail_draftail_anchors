import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wagtail_draftail_anchors",
    version="0.6.0",
    author="Wagtail Core Team",
    author_email="hello@wagtail.org",
    description="A Draftail extension to add anchor identifiers to rich text",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wagtail-nest/wagtail_draftail_anchors",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        "wagtail>2.9",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Wagtail :: 2",
        "Framework :: Wagtail :: 3"
        "Framework :: Wagtail :: 4"
        "Framework :: Wagtail :: 5"
        "Framework :: Wagtail :: 6",
    ],
    python_requires=">=3.6",
)
