import bs4 as bs
import urllib.request
import re
import nltk
nltk.download('punkt')
import heapq
import sys



cwe_domain = 'http://cwe.mitre.org/'

def summerize():

  return 0


def article_summerizer(urls, num_of_sentences=5, sen_length=40):
  summaries = {}

  for url in urls:
    try:
      hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
      req = urllib.request.Request(url, headers=hdr)
      scraped_article = urllib.request.urlopen(req)
      article = scraped_article.read()


      parse_article = bs.BeautifulSoup(article, 'lxml')
      article_para = parse_article.find_all('p')

      text = ''
      for p in article_para:
        text += p.text

      # text = re.sub(r'\[[0-9]*\]', ' ', text)
      # text = re.sub(r'\s', " ", text)

      new_text = text
      # new_text = re.sub(r'\s', " ", new_text)

      sentences = nltk.sent_tokenize(new_text)

      nltk.download('stopwords')
      stopwords = nltk.corpus.stopwords.words('english')

      token_freq = {}
      for token in nltk.word_tokenize(new_text):
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
    except:
      summaries[url] = ""
      
  return summaries


def cwe_scrapper():

  return 0

