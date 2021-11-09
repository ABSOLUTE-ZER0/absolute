from django.http import JsonResponse, HttpResponse
from elasticsearch import Elasticsearch
from django.template import context, loader
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .nlp.ranking import default_sorting, normalize_sorting


es = Elasticsearch("http://public:uKwNfMe4RizebrD@localhost:9200")


@api_view(['GET', 'POST'])
def index(request):

	# GET REQUEST

	if request.method == 'GET':
		template = loader.get_template('absolute_search/index.html')
		context = {

		}

		return HttpResponse(template.render(context, request))

	# POST REQUEST

	elif request.method == 'POST':
		query = request.POST['query']
		return redirect("/q={}".format(query))


def search_results(request, query):
	search_query = {
			"query_string": 
			{
				"query": query
			}
		}

	# sort = {
	#   "modified": "desc" 
	# }

	result = es.search(index = "nvd_index", 
	query = search_query, 
	size = 100000,
	# sort=sort,
	)

	metadata = {
		'total_results': result['hits']['total']['value']
	}

	final_result = normalize_sorting(result)

	context = {
		"results": final_result,
		"metadata": metadata,
	}

	return render(request, 'absolute_search/search_results.html', context)
