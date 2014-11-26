#!/usr/bin/python
import json
import urllib2
import itertools

API_KEY = 'AIzaSyAEXLea9UKrZ1UpJ2JJfVEUCN3IhBWnZsw'
LANG_URL = 'https://www.googleapis.com/language/translate/v2/languages?key=%s'
TRANS_URL = 'https://www.googleapis.com/language/translate/v2?key=%s&source=en&target=%s&q=%s'

NAMES = ['home', 'house', 'thing', 'smart', 'nest', 'sense', 'sensor', 'magic', 'den']

def main():
  result = urllib2.urlopen(LANG_URL % API_KEY).read()
  result = json.loads(result)
  languages = [l['language'] for l in result['data']['languages']]
  print len(languages)

  names = NAMES + list(itertools.permutations(NAMES, 2))

  for lang in languages:
    for name in names:
      try:
        url = TRANS_URL % (API_KEY, lang, name)
        translation = urllib2.urlopen(url).read()
        translation = json.loads(translation)
        for t in translation['data']['translations']:
          print t['translatedText']
      except:
        pass


def munge():
  names = list(x.strip().lower() for x in open('names'))
  tlds = list(x.strip().lower() for x in open('tlds.txt'))
  print names
  print tlds

  for name in names:
    for tld in tlds:
      if tld == name:
        continue
      if name.endswith(tld):
        print '%s.%s' % (name[:-len(tld)], tld)


if __name__ == '__main__':
  main()