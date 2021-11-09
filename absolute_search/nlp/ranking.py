import datetime
from datetime import date, datetime

 
# default sorting method
# sorts the results in a unique way. 
# Each result has a 'score' using BM25, nad the date it was modified
# Instead of just giving the results using the score, we are showing documents which were modified in the past 3 years and has a resonably good score.
# Then showing all the remaining results sorted via 'score'

def default_sorting(data):

	unsorted_data = data['hits']['hits']
	current_year = date.today().year

	latest_results = []
	old_high_score_results = []

	for i in unsorted_data:
		i['data'] = i.pop("_source")
		i['score'] = i.pop("_score")
		i['index'] = i.pop("_index")
		if(current_year - datetime.strptime(i['data']['modified'], "%Y-%m-%dT%H:%M:%S").year <= 3):
			latest_results.append(i)
		else:
			old_high_score_results.append(i)
		
	final_results = [*latest_results, *old_high_score_results] 

	return final_results

# normalize sorting is where the score is normalized
# this method is a modified version of default sorting
# it normalizes the scores first. then for the results of the past 3 years a value is added to the normalised score
# the value to be added is not fixed as of now and will be changed in the future
# once we have the updated scores, we then sort the results and return them

def normalize_sorting(data):
	sorted_data = data['hits']['hits']

	current_year = date.today().year
	max_score = data['hits']['max_score']

	def get_score(data):
		return data['score']

	for i in sorted_data:
		i['score'] = i.pop("_score")
		i['index'] = i.pop("_index")
		i['data'] = i.pop("_source")
		time_diff = current_year - datetime.strptime(i['data']['modified'], "%Y-%m-%dT%H:%M:%S").year
		i['score'] = (i['score'] / max_score ) # normalization (assuming min value is 0)
			
		if(time_diff < 3):
			i['score'] += (3-time_diff) * 1 / max_score # adding the value 

	sorted_data.sort(key=get_score, reverse=True)
	
	return sorted_data
