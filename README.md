# IGFollowers
IGFollowers is an Instagram crawler to get followers based on account. You just need to provide Account List to be crawled and your personal account as a crawler.
> <b>NOTE:</b> IGFollowers is not a library, it is an application that runs based on configuration files.

## Requirements

 - Docker
 - Git
 - MongoDB
 - Python 3.5.2

## Configuration
Before you try to run the application, you need to specify config files inside `/config/*.cfg` folder.

 - account.cfg: You personal account. This account act as crawler
 - database.cfg: Contains follower and account list database. This database only support MongoDB

### account.cfg
```ini
[account_1]
username = xxx
password = xxx
```
### database.cfg
```ini
[follower]
connectionString = [MongoDB Connection String]
database = xxx
collection = xxx

[crawling_list]
connectionString = [MongoDB Connection String]
database = xxx
collection = xxx
```

## Installation
Please make sure you have all configuration set. If you don't you can follow this installation setup below. 
> Note: This installation steps assume that you are using Linux

 - `docker pull franziz/igfollowers:new-logic`
 - `git clone http://github.com/franziz/igfollowers`
 - `cd igfollowers`
 - `mkdir config`
 - `touch account.cfg`
 - `git checkout new-logic`
 - `docker run -it --name igfollowers -v $(pwd):/root/app -w /root/app franziz/igfollowers:new-logic python run.py`

## Data Structure
### Input
Input data are stored inside the collection specified in `crawling_list` config.

| Key         | Types    | Desc                                      |
|-------------|----------|-------------------------------------------|
| _id         | ObjectId |                                           |
| brandName   | String   |                                           |
| country     | String   | Country of an official account belongs to |
| displayName | String   | Display name of an official account       |
| is_active   | Boolean  | Set it as False to not crawl this account | 
| modelName   | String   |                                           |
| url         | String   | URL that point to the official account    |
| userName    | String   | Username of the official account          |


### Output
Out data are stored inside the collection specified in `follower` config
| Key                       | Types    | Desc                                       |
|---------------------------|----------|--------------------------------------------|
| _id                       | ObjectId |                                            |
| display_name              | String   | Display name of an official account        |
| followers                 | Array    | Array of followers                         |
| followers.XX._insert_time | Date     | When the follower was inserted             |
| followers.XX.display_name | String   | Display name of the follower               | 
| followers.XX.user_link    | String   | URL directly point to the follower         |
| followers.XX.username     | String   | Username of the follower                   |
| logdisplay_name           | String   | I do not know about this                   |
| user_link                 | String   | URL directly point to the official account |
| username                  | String   | Username of the official account           |