from lib.instagram.instagram import Instagram
from lib.engine.crawler      import Engine
from lib.data                import Data
from lib.logger              import Logger
# from tqdm                    import tqdm
import time
import random

if __name__ == "__main__":
    logger          = Logger()
    logger.app_name = "igfollowers"

    instagram          = Instagram()
    instagram.username = "frans.follower"
    instagram.password = "isidsea123"
    instagram.login()
    logger.write("Logged in")
    data = Data()
    data = data.user_list
    for datum in data:
      logger.write("Crawling: {}".format(datum["userName"]))
      engine            = Engine(datum)
      old_user          = engine.get_user(datum["userName"])
      old_followers     = old_user.followers
      current_user      = instagram.goto_user(datum["userName"])
      current_followers = current_user.followers
      new_followers     = [user for user in current_followers if user not in old_followers]
      unfollow_users    = [user for user in old_followers if user not in current_followers]

      logger.write("[{}] Saving user data...".format(datum["userName"]))
      for follower in new_followers:
        engine.save(follower)
      logger.write("[{}] Saved...")

      logger.write("[{}] Deleting user data...".format(datum["userName"]))
      for follower in unfollow_users:
        engine.delete(follower)
      logger.write("[{}] Deleted...")

    instagram.quit()