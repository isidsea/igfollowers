from lib.instagram.instagram import Instagram
from lib.engine              import Engine
from lib.data                import Data
from tqdm                    import tqdm
import time
import random

if __name__ == "__main__":
    instagram          = Instagram()
    instagram.username = "frans.follower"
    instagram.password = "isidsea123"
    instagram.login()

    data = Data()
    data = tqdm(data.user_list)
    data.set_description("Crawling users...")
    for datum in data:
      user      = instagram.goto_user(datum["userName"])
      followers = user.followers
      followers = tqdm(followers)

      engine = Engine(datum)
      for follower in followers:
          followers.set_description("[igfollowers][{}] Saving user data...".format(datum["userName"]))
          engine.save(follower)        
      #end for
      time.sleep(random.randint(10000,50000)/1000)

    instagram.quit()