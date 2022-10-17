import setuptools

with open("README.md", "r", encoding="utf-8") as fhand:
    long_description = fhand.read()

setuptools.setup(
    name="sync-folders",
    version="0.0.1",
    author="Sanjay Mane",
    author_email="sanjusmane@gmail.com",
    description=("Simple package to sync 2 folders"
                "Synchronization must be one-way and content of the replica folder should be modified to exactly match content of the source folder;."),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sanjaysmane/sync-folders/demo",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "syncfold = syncfold.cli:main",
        ]
    }
)
