from elasticsearch import Elasticsearch
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from .nlp.ranking import default_sorting, normalize_sorting
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
		size = 100000,
		)

		metadata = {
			'total_results': result['hits']['total']['value'],
			'query': query,
		}

		if(sort == "default"):
			final_result = normalize_sorting(result)
		elif(sort == "hybrid"):
			final_result = default_sorting(result)
		elif(sort == "relevance"):
			final_result = result


		p = Paginator(final_result, 20)

		display_result = p.page(page)

		context = {
			"results": display_result,
			"metadata": metadata,
		}

		return render(request, 'absolute_search/search_results.html', context)

		# POST REQUEST

	elif request.method == 'POST':
		query = request.POST['query']
		return redirect("/q={}".format(query))