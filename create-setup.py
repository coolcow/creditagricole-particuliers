#!/usr/bin/env python3
import json
import requests
import sys
from pathlib import Path

def get_latest_version():
    """Get the latest version from the original repository."""
    response = requests.get('https://api.github.com/repos/dmachard/creditagricole-particuliers/tags')
    if response.status_code != 200:
        print("[ERROR] Unable to retrieve latest version")
        sys.exit(1)
    
    tags = response.json()
    if not tags:
        print("[ERROR] No tags found")
        sys.exit(1)
    
    latest_tag = tags[0]['name']
    if not latest_tag.startswith('v'):
        print(f"[ERROR] Invalid tag format: {latest_tag}")
        sys.exit(1)
    
    version = latest_tag[1:]  # Remove 'v' prefix
    if not all(part.isdigit() for part in version.split('.')):
        print(f"[ERROR] Invalid version format: {version}")
        sys.exit(1)
    
    return version

def verify_version_exists(version):
    """Verify if the specified version exists in the original repository."""
    response = requests.get('https://api.github.com/repos/dmachard/creditagricole-particuliers/tags')
    if response.status_code != 200:
        print("[ERROR] Unable to verify version")
        sys.exit(1)
    
    tags = response.json()
    version_tag = f"v{version}"
    return any(tag['name'] == version_tag for tag in tags)

def create_setup_py(version):
    """Create setup.py with the given version."""
    setup_content = f'''from setuptools import setup, find_packages

setup(
    name="creditagricole-particuliers",
    version="{version}",
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
'''
    Path('setup.py').write_text(setup_content)
    print(f"[SUCCESS] Created setup.py with version {version}")

def main():
    if len(sys.argv) > 1:
        version = sys.argv[1]
        if not verify_version_exists(version):
            print(f"[ERROR] Version {version} does not exist in the original repository")
            sys.exit(1)
    else:
        print("[INFO] Determining latest version...")
        version = get_latest_version()
    
    create_setup_py(version)

if __name__ == '__main__':
    main() 