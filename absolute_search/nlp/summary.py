import re
import nltk
import heapq
import os
import json
from scrapyd_api import ScrapydAPI, FINISHED
import uuid
import time

nltk.download('punkt')
scrapyd = ScrapydAPI('http://localhost:6800')


def article_summerizer(urls, num_of_sentences=5, sen_length=40):
  summaries = {}

  for url in urls:
    try:
      id = uuid.uuid1()
      filename = './absolute_search/nlp/{}.json'.format(id)
      setting={
        'FEED_URI': filename,
        }
      
      job_id = scrapyd.schedule('absolute_scrapper', 'article_spider', settings=setting, url=url)
      job_status = scrapyd.job_status('absolute_scrapper', job_id)

      count = 0
      while(True):
        if(job_status == FINISHED and os.path.exists(filename)):
          with open(filename) as json_file:
            data = json.load(json_file)
            text = data['data']
          break
        elif(count > 200):
          raise Exception('Too Freaking Long!! Thats what she said')
        else:
          count += 1
          time.sleep(.05)
          job_status = scrapyd.job_status('absolute_scrapper', job_id)

      sentences = nltk.sent_tokenize(text)

      nltk.download('stopwords')
      stopwords = nltk.corpus.stopwords.words('english')

      token_freq = {}
      for token in nltk.word_tokenize(text):
        if(token not in stopwords):
          if token not in token_freq.keys():
            token_freq[token] = 1
          else:
            token_freq[token] += 1

      max_freq = max(token_freq.values())

      for token in token_freq.keys():
        token_freq[token] = (token_freq[token]/max_freq)

      weight = {}
      for sent in sentences:
        for token in nltk.word_tokenize(sent.lower()):
          if token in token_freq.keys():
            if len(sent.split(" ")) < sen_length:
              if sent not in weight.keys():
                weight[sent] = token_freq[token]
              else:
                weight[sent] += token_freq[token]

      extracted_sentences = heapq.nlargest(num_of_sentences, weight, key=weight.get)
      summary = ' '.join(extracted_sentences)
      summaries[url] = summary

      # Deleting the file
      os.remove(filename)

    except Exception as e:
      summaries[url] = ""
      
  return summaries


def cwe_scrapper(urls):
  reports = {}

  for url in urls:
    id = uuid.uuid1()
    filename = './absolute_search/nlp/{}.json'.format(id)
    setting={
      'FEED_URI': filename,
      }
    
    job_id = scrapyd.schedule('absolute_scrapper', 'cwe_spider', settings=setting, url=url)
    job_status = scrapyd.job_status('absolute_scrapper', job_id)

    count = 0
    while(True):
      if(job_status == FINISHED and os.path.exists(filename)):
        with open(filename) as json_file:
          data = json.load(json_file)
          reports[url] = data
          break
      elif(count > 200):
        raise Exception('Too Freaking Long!! Thats what she said')
      else:
        count += 1
        time.sleep(.05)
        job_status = scrapyd.job_status('absolute_scrapper', job_id)
  
  os.remove(filename)
  
  return reports

