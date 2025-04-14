from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="fauxmots",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A simple SMTP test server for developers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/username/fauxmots",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Communications :: Email",
        "Topic :: Software Development :: Testing",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "fauxmots=app.cli:main",
        ],
    },
)
