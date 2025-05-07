from setuptools import setup, find_packages

setup(
    name="creditagricole-particuliers",
    version="0.14.3",
    description="Client Python pour la banque Crédit agricole - Particuliers",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Original: dmachard, Fork: coolcow",
    url="https://github.com/coolcow/creditagricole-particuliers",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
        "beautifulsoup4>=4.9.3",
        "lxml>=4.9.0",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
