from django.http import JsonResponse, HttpResponse
from elasticsearch import Elasticsearch
from django.template import context, loader
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


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
		query = request.headers['query']

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



		template = loader.get_template('absolute_search/index.html')
		context = {

		}

		return JsonResponse(result)

