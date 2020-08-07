import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wagtail_draftail_anchors",
    version="0.2.0",
    author="Jacob Topp-Mugglestone, Quoc Duan",
    author_email="jacobtm@torchbox.com",
    description="A Draftail extension to add anchor identifiers to rich text",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jacobtoppm/wagtail_draftail_anchors",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=["wagtail>2.9",],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
