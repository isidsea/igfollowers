# IGFollowers
This is an app to get follower from given useraccount. The installation can only be done by Docker and Git. This application also uses MongoDB to save all the data.

# How it works,
It will read JSON file from `./data/Data.json` file. With following format
```json
[
    {
        "collectionName": "", 
        "displayName": "", 
        "followers": 0, 
        "following": 0, 
        "posts": 0, 
        "url": "https://www.instagram.com/volkswagenph/", 
        "userId": 0, 
        "userName": "volkswagenph",
        "brand": "",
        "model": ""
    },
]
```

# Docker Image
1. docker pull franziz/igfollowers
2. docker pull mongo

# How to use
If you want to crawl, you can use
```bash
python3 main.py
```
`aggregate_user.py` is a reverse from `main.py`. The script will try to get all the users from database and create new instagram account.

# TODO
Some of todos in here
- Make a config file to specify output places
