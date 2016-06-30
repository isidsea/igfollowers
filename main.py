BIG_MOCK_INPUT = {
    "collectionName": "toyotamotorphfollowers", 
       "displayName": "Toyota Philippines", 
         "followers": 8165, 
         "following": 3, 
             "posts": 163, 
               "url": "https://www.instagram.com/toyotamotorphilippines/", 
            "userId": 1512780643, 
          "userName": "toyotamotorphilippines"
}
SMALL_MOCK_INPUT = {
    "collectionName": "toyotamotorvifollowers", 
    "displayName": "Toyota Vietnam", 
    "followers": 70, 
    "following": 69, 
    "posts": 5, 
    "url": "https://www.instagram.com/toyotavietnam/", 
    "userId": 1718775482, 
    "userName": "toyotavietnam"
  }

from lib.instagram.instagram import Instagram
from lib.engine              import Engine
from tqdm                    import tqdm

if __name__ == "__main__":
    instagram          = Instagram()
    instagram.username = "frans.follower"
    instagram.password = "isidsea123"
    instagram.login()

    user      = instagram.goto_user(BIG_MOCK_INPUT["userName"])
    followers = user.followers
    followers = tqdm(followers)

    engine = Engine(BIG_MOCK_INPUT)
    for follower in followers:
        followers.set_description("[igfollowers] Saving user data...")
        engine.save(follower)        
    #end for

    instagram.quit()