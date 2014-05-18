# A dictionary of movie critics and their ratings of a small
# set of movies
critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
 'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 3.5},
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
 'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
 'The Night Listener': 4.5, 'Superman Returns': 4.0,
 'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 2.0},
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}


from math import sqrt

# Eucledian Distance based similarity score for person1 and person2
def sim_distance(prefs, person1, person2):
  # Get list of common items rated by the critics
  common_items = {}
  for item in prefs[person1]:
    if item in prefs[person2]:
      common_items[item] = 1

  # If no common items, the similarity score is 0
  if len(common_items) == 0:
    return 0;

  # Calculate the score
  dissimilarity_score = sum([pow(prefs[person1][item] - prefs[person2][item], 2)
                        for item in common_items])
  # Add 1 to avoi ddivision by zero. Also ensures that the similarity score is
  # always between 0 and 1.
  return 1/(1+dissimilarity_score)

# Pearson Correlation between variables is defined as the following ratio
#           Cov(X,Y) / (\sigma_X * \sigma_Y)
# Gives a better correlation meausre when the scales of ratings are different.
def sim_pearson(prefs, person1, person2):
  # Get list of common items rated by the critics
  common_items = {}
  for item in prefs[person1]:
    if item in prefs[person2]:
      common_items[item] = 1

  # If no common items, the similarity score is 0
  if len(common_items) == 0:
    return 0;

  # Calculate the score
  n = len(common_items)
  sum1 = sum([prefs[person1][item] for item in common_items])
  sum2 = sum([prefs[person2][item] for item in common_items])
  sum1Sq = sum([prefs[person1][item]**2 for item in common_items])
  sum2Sq = sum([prefs[person2][item]**2 for item in common_items])
  pSum = sum([prefs[person1][item]*prefs[person2][item] for item in common_items])
  numerator = pSum - (sum1*sum2/n)
  denomenator = sqrt((sum1Sq-(sum1**2)/n) * (sum2Sq - (sum2**2)/n))
  if denomenator == 0:
    return 0
  return numerator/denomenator


# Get critics similar to a given critic
#   prefs: Dictionary containing the movie ratings of various critics.
#   person: The critic whose best matches need to be found
#   n: integer > 0. Number of best matches to find.
#   similarity: function that gives the similarity between two critics.
def topMatches(prefs, person, n = 5, similarity = sim_pearson):
  scores = sorted([(similarity(prefs, person, other), other) for other in prefs if other != person], key=lambda (a,b): a, reverse=True)
  return scores[:n]


# Get recommendations for a person
def getRecommendations(prefs, person, similarity=sim_pearson):
  totals = {}
  simSum = {}

  for other in prefs:
    if other == person:
      continue
    similarity_score = similarity(prefs, person, other)
    print other, similarity_score
    if similarity_score <= 0 :
      continue

    for movie in prefs[other]:
      if movie not in prefs[person] or prefs[person][movie] == 0:
        print movie, prefs[other][movie]
        totals.setdefault(movie, 0)
        totals[movie] += prefs[other][movie]*similarity_score
        simSum.setdefault(movie, 0)
        simSum[movie] += similarity_score

  return sorted([(totals[movie]/simSum[movie], movie) for movie in totals], reverse=True, key=lambda (a,b): a)


# Transform Prefs to get the movies as keys
def transformPrefs(prefs):
  result = {}
  for person in prefs:
    for movie in prefs[person]:
      result.setdefault(movie, {})
      result[movie][person] = prefs[person][movie]
  return result

# Compute items similar to other items
def calculateSimilarItems(prefs, n=10):
  # Dictionary of items showing which other items they are similar to
  result = {}

  # Get an item centric dictionary
  itemPrefs = transformPrefs(prefs)
  c = 0
  for item in itemPrefs:
    # Status update
    c += 1
    if c%100 == 0: print "%d / %d" % (c, len(itemPrefs))
    result[item] = topMatches(itemPrefs, item, n=n, similarity=sim_pearson)
  return result
