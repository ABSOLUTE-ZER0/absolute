from elasticsearch import Elasticsearch
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from .nlp.ranking import default_sorting, normalize_sorting, preprocess_sorting, date_sorting, date_asc_sorting
from .nlp.summary import article_summarizer, cwe_scrapper
from django.core.paginator import Paginator

es = Elasticsearch("http://public:uKwNfMe4RizebrD@localhost:9200")

@api_view(['GET', 'POST'])
def index(request):

	# GET REQUEST

	if request.method == 'GET':
		context = {}
		return render(request, 'absolute_search/index.html', context)

	# POST REQUEST

	elif request.method == 'POST':
		query = request.POST['query']
		return redirect("/q={}".format(query))


@api_view(['GET', 'POST'])
def search_results(request, query, page=1, sort="default"):

	# GET REQUEST

	if request.method == 'GET':
		search_query = {
				"query_string":
				{
					"query": query
				}
			}

		result = es.search(index = "nvd_index", 
		query = search_query, 
		size = 1000000,
		)

		metadata = {
			'total_results': result['hits']['total']['value'],
			'query': query,
			'sort': sort,
			"path": request.path.split("&page")[0]
		}

		if(sort == "default"):
			final_result = normalize_sorting(result)
		elif(sort == "hybrid"):
			final_result = default_sorting(result)
		elif(sort == "relevance"): 
			final_result = preprocess_sorting(result) 
		elif(sort == "date"): 
			final_result = date_sorting(result) 
		elif(sort == "date_asc"): 
			final_result = date_asc_sorting(result) 


		p = Paginator(final_result, 15)

		display_result = p.page(page)

		if(page > 5 and page < (p.num_pages -5 )):
			page_range = range(page-5, page+6)
		elif(page <= 5):
			page_range = range(1, 11)
		elif(page >= (p.num_pages - 5 )):
			page_range = range((p.num_pages - 10 ), (p.num_pages+1))

		pagination = {
			"current": page,
			"max": p.num_pages,
			"next": display_result.next_page_number() if display_result.has_next() else None,
			"previous": display_result.previous_page_number() if display_result.has_previous() else None,
			"range": page_range,
			"has_previous": display_result.has_previous(),
			"has_next": display_result.has_next(),
		}

		context = {
			"results": display_result,
			"metadata": metadata,
			"pagination": pagination,
		}

		return render(request, 'absolute_search/search_results.html', context)

		# POST REQUEST

	elif request.method == 'POST':
		query = request.POST['query']
		return redirect("/q={}".format(query))



def doc(request, index, id):
	# try:
		if(index == "nvd"):
			result = es.get(index="nvd_index", id=id.upper())
			display_result = result['_source']

			reference_links = display_result['further_details']
			cwe_links = display_result['cwe_links']

			reference_summaries = "" 
			cwe_data = ""

			if reference_links:
				reference_summaries = article_summarizer(reference_links, 5, 35)

			if cwe_links: 
				cwe_data = cwe_scrapper(cwe_links)
			
			metadata = {  
				'summaries': {
					'article': reference_summaries, 
					'cwe': cwe_data, 
					} 
			}

			context = {
				"metadata": metadata,
				"result": display_result, 
			}
			return render(request, 'absolute_search/doc_cve.html', context)

	# except:
	# 	return redirect("/q={}".format(id))