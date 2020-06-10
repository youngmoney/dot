import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PROJECT",
    version="0.0.1",
    author="Taylor L Money",
    author_email="git@taylorlmoney.com",
    description="",
    long_description=open('README.md').read()
    long_description_content_type="text/markdown",
    url="https://github.com/youngmoney/PROJECT",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
