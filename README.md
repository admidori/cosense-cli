# cosense-cli
[![CI](https://github.com/admidori/cosense-cli/actions/workflows/ci.yaml/badge.svg)](https://github.com/admidori/cosense-cli/actions/workflows/ci.yaml)
[![PyPI version](https://badge.fury.io/py/cosense.svg)](https://badge.fury.io/py/cosense)
[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/admidori/cosense-cli/blob/main/LICENSE)

The unofficial CLI reader of the Cosense.  
This project uses [Cosense API](https://scrapbox.io/help-jp/API).

![](/docs/gif/gif1.gif)

## Installation
```sh
pip install cosense
```

### For Windows users
If you install the CLI tool created by Python for the first time, this program may not be operational.  
Please execute the below on your PowerShell before executing this program.  
```sh
$env:PATH += ";" + (Get-Item (python -m site --user-site)).parent.fullname + "\Scripts"
```
(Reference: https://zenn.dev/kumazo/articles/35215498b86939)

#### Note
Windows support is not enough. So sometimes the layout is broken.  
If you are a Windows hacker, please contribute to our repository ;)  

## Basic Use
### Commandline
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
### Check your token
1. Access your Cosense project page
2. Check Cookies information (In Chrome, press F12 and show the "Application" tab)
3. Copy the value of `connect.sid`
  
![](/docs/img/img1.png)

### Commandline
```sh
# Replace the "your token" with "connect.sid"
cosense search "your project name" --auth "your token"
```

### Use Cosense API in Python
```python
import cosense

# Define sid on the value of "connect.sid"
sid = "s%3Ag8zuk3JlDhp1t2o45eE5Aj3kK3yHkT_N.ipbmkRVRIP..."
your_project_name = "project"
client = cosense.Client(sid = sid)
project = client.get(f"/{your_project_name}/")
```

# License
This project is published under the [MIT license](https://github.com/admidori/cosense-cli/blob/main/LICENSE).  
This repository is based on [kaisugi/scrapbox-python](https://github.com/kaisugi/scrapbox-python).  
