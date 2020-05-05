# pyenvbuilder

Python Environment Builder

### Prerequisites
 * Python 3.6+

Aditional package requirements are listed in the requirements.txt file.

# Building the Documentation Locally
In order to build the documentation you will need to install some dependencies that are not part of the runtime dependencies of PyEnvBuilder

After cloning this repository do the following:

```bash
pip install -r docs-requirements.txt

cd docs
make html
```
This will generate the HTML documentation for PyEnvBuilder at the `/docs/build/html` folder. 
Locate the `index.html` file and open it with your browser.
