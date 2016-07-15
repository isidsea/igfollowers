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
      engine            = Engine(datum)
      old_user          = engine.get_user(datum["userName"])
      old_followers     = old_user.followers
      current_user      = instagram.goto_user(datum["userName"])
      current_followers = current_user.followers
      new_followers     = [user for user in current_followers if user not in old_followers]
      new_followers     = tqdm(new_followers)
      unfollow_users    = [user for user in old_followers if user not in current_followers]
      unfollow_users    = tqdm(unfollow_users)

      for follower in new_followers:
        new_followers.set_description("[igfollowers][{}] Saving user data...".format(datum["userName"]))
        engine.save(follower)

      for follower in unfollow_users:
        unfollow_users.set_description("[igfollowers][{}] Delete user data...".format(datum["userName"]))
        engine.delete(follower)

    instagram.quit()