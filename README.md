# IGFollowers
IGFollowers is an Instagram crawler to get followers based on account. You just need to provide Account List to be crawled and your personal account as a crawler.
> <b>NOTE:</b> IGFollowers is not a library, it is an application that runs based on configuration files.

### Requirements

 - Docker
 - Git
 - MongoDB
 - Python 3.5.2

### Configuration
Before you try to run the application, you need to specify config files inside `/config/*.cfg` folder.

 - account.cfg: You personal account. This account act as crawler

#### account.cfg
```ini
[account_1]
username = xxx
password = xxx
```
username and password are string.

### Installation
Please make sure you have all configuration set. If you don't you can follow this installation setup below. 
> Note: This installation steps assume that you are using Linux

 - `docker pull franziz/igfollowers:new-logic`
 - `git clone http://github.com/franziz/igfollowers`
 - `cd igfollowers`
 - `mkdir config`
 - `touch account.cfg`
 - `git checkout new-logic`
 - `docker run -it --name igfollowers -v $(pwd):/root/app -w /root/app franziz/igfollowers:new-logic python run.py`