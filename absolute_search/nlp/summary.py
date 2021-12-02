import re
import nltk
import heapq
import os
import json
from scrapyd_api import ScrapydAPI, FINISHED
import uuid
import time
import bs4 as bs
import urllib.request
import ssl

nltk.download('punkt')
scrapyd = ScrapydAPI('http://localhost:6800')
context = ssl.SSLContext()

def article_summarizer(urls, num_of_sentences=5, sen_length=40):
  summaries = {}

  for url in urls:
    try:

      if(url.find(".pdf")):
        summaries[url] = "Can't extract content from non HTML document. Click on the link to vist the page"
        continue

      hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
      req = urllib.request.Request(url, headers=hdr)
      scraped_article = urllib.request.urlopen(req, context=context)
      article = scraped_article.read()

      parse_article = bs.BeautifulSoup(article, "lxml")


      #---------  Certain HTML articles do not have content-type meta tag ---------#
      
      # encode_type = parse_article.select('meta[http-equiv="content-type" i]')
      # content_type = encode_type[0]['content'].split(";")[0]

      # if(content_type != "text/html"):
      #   summaries[url] = "Cant extract content from non HTML document"
      #   continue

      article_para = parse_article.select("body p")

      text = ''
      for p in article_para:
        text += p.text

      sentences = nltk.sent_tokenize(text)
      summary = ""

      if(len(sentences) > num_of_sentences):
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
        summary = "Following articles can't be summarized" if len(extracted_sentences) < num_of_sentences else ' '.join(extracted_sentences)
      
      elif(len(sentences) <= num_of_sentences and len(sentences) > 0):
        summary = ' '.join(sentences)

      else:
        summary = "Following articles can't be summarized" 

      summaries[url] = summary

    except Exception as e:
      summaries[url] = "Following articles can't be summarized"
      
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


#-------------- CODE FOR CWE USING BS4 --------------#

# import re
# import nltk
# import heapq
# from scrapyd_api import ScrapydAPI, FINISHED
# import bs4 as bs
# import urllib.request
# from lxml import etree

# nltk.download('punkt')
# scrapyd = ScrapydAPI('http://localhost:6800')
# hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}

# def cwe_scrapper(urls):
#   reports = {}

#   for url in urls:
#     req = urllib.request.Request("https://cwe.mitre.org/data/definitions/20.html", headers=hdr)
#     scraped_article = urllib.request.urlopen(req)

#     cwe = bs.BeautifulSoup(scraped_article, "lxml")
#     dom = etree.HTML(str(cwe))

#     desc = cwe.select('div#Extended_Description div.indent')[0].contents

#     relations = {}
#     for i in dom.xpath("//div[@id='Relationships']//div[@id='relevant_table']"):
#       key = i.xpath(".//div[@class='reltable']/text()")[0]
#       value = [str(etree.tostring(i))[2:-1] for i in i.xpath(".//div[@class='tabledetail']//td//a")]
#       relations[key] = value


#     related_attack_pattern = [str(etree.tostring(i))[2:-1] for i in dom.xpath("d/a")]
#     created = dom.xpath("((//div[@id='Content_History']//tbody)[1]//tr//td)[1]/text()")[0]
#     modified = dom.xpath("((//div[@id='Content_History']//tbody)[2]//tr)[last() - 1]/td/text()")[0]

#     reports[url] = {
#       'desc': desc,
#       'relations': relations,
#       # 'injection': injection,
#       # 'notes': notes,
#       'related_attack_pattern': related_attack_pattern,
#       'created': created,
#       'modified': modified,
#     }

    
#   return reports

