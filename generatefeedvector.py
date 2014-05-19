import feedparser
import re

class ParsingError(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

# Parses the words in the text properly
def getwords(html):
  # Remove HTML tags
  txt = re.compile(r'<[^>]+>').sub('', html)

  # Split words by non-alpha characters
  words = re.compile(r'[^A-Z^a-z]+').split(txt)

  return [word.lower() for word in words if word!='']

# Returns a dictionary of word counts for an RSS feed
def getWordCounts(rss_url):
  parsed = {}
  trial = 0
  while 'feed' not in parsed or 'title' not in parsed.feed :
    if trial > 3:
      raise ParsingError(rss_url)
    parsed = feedparser.parse(rss_url)
    trial += 1

  word_count = {}
  for entry in parsed.entries:
    if 'summary' in entry:
      summary = entry.summary
    else:
      summary = entry.description

    # Extract a list of words
    words = getwords(entry.title + ' ' + summary)
    for word in words:
      word_count.setdefault(word, 0)
      word_count[word] += 1

  return parsed.feed.title, word_count


apcount = {}
wordcounts = {}
feedlist = file('feedlist.txt')
for feed_url in feedlist:
  print "Reading " + feed_url
  try:
    title, wc = getWordCounts(feed_url)
  except ParsingError as e:
    print 'Skipping ' + feed_url + ' as parsing unsuccessful'
  wordcounts[title] = wc
  for word, count in wc.items():
    apcount.setdefault(word,0)
    if count >1:
      apcount[word]+=1

print 'Read ' + len(wordcounts) + ' blogs'

wordlist = []
for w,bc in apcount.items():
  frac = float(bc)/len(wordcounts)
  if frac>0.1 and frac<0.5: wordlist.append(w)

out=file('blogdata.txt','w')
out.write('Blog')
for word in wordlist:
  out.write('\t%s' % word)
out.write('\n')
for blog,wc in wordcounts.items( ):
  out.write(blog)
  for word in wordlist:
    if word in wc: 
      out.write('\t%d' % wc[word])
    else:
      out.write('\t0')
  out.write('\n')
