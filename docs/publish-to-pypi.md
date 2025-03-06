# Publishing LiteAgent to PyPI

This document provides instructions for building and publishing the LiteAgent package to PyPI.

## Prerequisites

1. Create an account on [PyPI](https://pypi.org/)
2. Install the required tools:
   ```bash
   pip install build twine
   ```

## Building the Package

To build the package, run the following command from the project root:

```bash
python -m build
```

This will create distribution files in the `dist/` directory.

## Testing the Package

Before publishing, it's a good idea to test the package by uploading it to the PyPI test server:

```bash
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

Then install it from the test server:

```bash
pip install --index-url https://test.pypi.org/simple/ liteagent
```

## Publishing to PyPI

Once you've confirmed everything works correctly, upload the package to PyPI:

```bash
twine upload dist/*
```

You'll be prompted for your PyPI username and password.

## Setting up GitHub Actions for Automatic Publishing

To automate publishing with GitHub Actions, follow these steps:

1. Create a `.github/workflows/publish.yml` file with the following content:

```yaml
name: Publish Python Package

on:
  release:
    types: [created]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    - name: Build and publish
      env:
        TWINE_USERNAME: ${{ secrets.PYPI_USERNAME }}
        TWINE_PASSWORD: ${{ secrets.PYPI_PASSWORD }}
      run: |
        python -m build
        twine upload dist/*
```

2. Add your PyPI username and password as secrets in your GitHub repository settings (Settings > Secrets > Actions)

3. Create a new release in GitHub, and the workflow will automatically publish the package to PyPI

## Versioning

Remember to update the version number in `liteagent/__init__.py` before creating a new release. 