# cosense-cli
[![CI](https://github.com/admidori/cosense-cli/actions/ci.yaml/badge.svg)](https://github.com/admidori/cosense-cli/actions/ci.yaml)
[![PyPI version](https://badge.fury.io/py/cosense.svg)](https://badge.fury.io/py/cosense)
[![MIT License](https://img.shields.io/github/license/admidori/cosense-cli?label=License)](https://github.com/admidori/cosense-cli/blob/main/LICENCE)

The unofficial CLI reader of the Cosense.
This project uses [Cosense API](https://scrapbox.io/help-jp/API).

## Installation

```sh
pip install cosense
# or `pipenv install cosense`
```

## Basic Use
### commandline
```sh
cosense search help-jp
```

### Use Cosense API in Python
```python
import cosense

client = cosense.Client()
project = client.get("/help-jp/")
```

## Advance Use (For private project)
### Check the your token
1. Access your Cosense project page
2. Check Cookies information (In Chrome, press F12 and show the "Application" tab)
3. Copy value of "connect.sid"
![](/docs/img/img1.png)

### Commandline
```sh
# Replace the "your token" to "connect.sid"
cosense serach "your project name" --auth "your token"
```

### Use Cosense API in Python
```python
import cosense

# Define sid on value of "connect.sid"
sid = "s%3Ag8zuk3JlDhp1t2o45eE5Aj3kK3yHkT_N.ipbmkRVRIP..."
your_project_name = "project"
client = cosense.Client(sid = sid)
project = client.get(f"/{your_project_name}/")
```

# Lisence
This project is published under the [MIT lisence](https://github.com/admidori/cosense-cli/blob/main/LICENCE).
And this repository is based on [kaisugi/scrapbox-python](https://github.com/kaisugi/scrapbox-python).
