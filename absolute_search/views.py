from django.http import JsonResponse, HttpResponse
from elasticsearch import Elasticsearch
from django.template import context, loader
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .nlp.ranking import default_sorting


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

		final_result = {}

		metadata = {
			'total_results': result['hits']['total']['value']
		}

		final_result['metadata'] = metadata
		final_result['results'] = default_sorting(result)


		return JsonResponse(final_result, safe=False)

