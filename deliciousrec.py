from pydelicious import get_popular, get_userposts, get_urlposts
import time

# Get the list of users who recently posted a popular link with a specified tag
# The API returns only 30 users who posted a recent link, and thus gather users
# from top 5 links shared.
def initializeUserDict(tag, count=5):
  top_users= {}
  for popular_post in get_popular(tag=tag)[0:count]:
    for post in get_urlposts(popular_post['url']):
      top_users[post['user']] = {}
  return top_users

# Create a dicionary of "ratings", where a user rates a particular link as
# either 1 or 0 depending on if she shared the link or not
def fillItems(users):
  all_posts = {}
  for user in users:
    posts = []
    for i in range(3):
      try:
        posts = get_userposts(user)
        print "Succedded for user " + user + " :)"
        break
      except:
        print "Failed User " + user + ", retrying"
        time.sleep(4)
    for post in posts:
      users[user][post["url"]] = 1.0
      all_posts[post["url"]] = 1

  for ratings in top_users.values():
    for post in all_posts:
      if post not in ratings:
        ratings[post] = 0.0

