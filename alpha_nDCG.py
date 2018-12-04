from math import log
from copy import deepcopy
import numpy as np


class AlphaNDCG(object):
	def __init__(self, query_topics, doc_topics, alpha=0.5):
		self.set_alpha(alpha = alpha)
		self.load_query_topics(query_topics = query_topics)
		self.load_doc_topics(doc_topics = doc_topics)
		self.dcg_values = {}
		self.ndcg_values = {}

	def set_alpha(self, alpha):
		self.alpha = alpha
		 
	def load_query_topics(self, query_topics):
		self.query_topics_dict = query_topics

	def load_doc_topics(self, doc_topics):
		self.doc_topics_dict = doc_topics

	def calculate_Alpha_DCG(self, ranking_query_doc, depth=20):
		local_dcg_values = {}
		for query in ranking_query_doc:
			topics_query = set(self.query_topics_dict[query])
			topics_number_of_occurrences = dict(zip(topics_query, np.zeros(len(topics_query))))

			local_depth = min(depth, len(ranking_query_doc[query]))
			local_dcg_values[query] = np.zeros(local_depth)

			value = 0.0
			for i in range(0,local_depth):
				topics_intersection = (set(self.doc_topics_dict[ranking_query_doc[query][i]]) & topics_query)

				for topic in topics_intersection:
					value += ((1 - self.alpha)**topics_number_of_occurrences[topic]) / log(2+i, 2)
					topics_number_of_occurrences[topic]+=1
				local_dcg_values[query][i] = deepcopy(value)
		return local_dcg_values

	def compute_Alpha_DCG(self, ranking_query_doc, depth=20):
		self.dcg_values = deepcopy( self.calculate_Alpha_DCG(ranking_query_doc = ranking_query_doc, depth = depth) )


	def calculate_Alpha_nDCG(self, ranking_query_doc, depth=20):		
		self.compute_Alpha_DCG(ranking_query_doc = ranking_query_doc, depth = depth)

		for query in ranking_query_doc:
			local_depth = min(depth, len(ranking_query_doc[query]))
			idealRanking = self.get_ideal_ranking(query = query, atual_ranking = ranking_query_doc[query], depth = local_depth)
			auxiliarDict = {}
			auxiliarDict[query] = deepcopy( idealRanking )
			dcg_ideal_ranking = self.calculate_Alpha_DCG(ranking_query_doc = auxiliarDict, depth = local_depth)
			
			self.ndcg_values[query] = np.zeros(local_depth)

			value = 0.0
			for i in range(0,local_depth):
				self.ndcg_values[query][i] = (self.dcg_values[query][i] / dcg_ideal_ranking[query][i])

	def get_ideal_ranking(self, query, atual_ranking, depth):
		ideal_ranking = []
		topics_query = set(self.query_topics_dict[query])
		topics_number_of_occurrences = dict(zip(topics_query, np.zeros(len(topics_query))))

		doc_candidates = set(deepcopy( atual_ranking ))

		while len(doc_candidates)>0 and len(ideal_ranking)<depth:
			bestValue = float("-inf")
			whoIsBest = "noOne"
			topics_of_best = set()

			for document in doc_candidates:
				value = 0.0
				topics_intersection = (set(self.doc_topics_dict[document]) & topics_query)

				for topic in topics_intersection:
					value += ((1 - self.alpha)**topics_number_of_occurrences[topic]) / log(2+len(ideal_ranking), 2)

				if value > bestValue:
					bestValue = deepcopy(value)
					whoIsBest = deepcopy(document)
					topics_of_best = deepcopy(topics_intersection)

			for topic in topics_of_best:
				topics_number_of_occurrences[topic]+=1
			ideal_ranking.append( deepcopy(whoIsBest) )
			doc_candidates.remove(whoIsBest)

		return ideal_ranking


'''
# Implemmenting [Clarke, 2008] example
if __name__ == '__main__':
	
	# Query-Topics Dictionary
	queryDict = {}
	queryDict["QA Example"] = ['85.1', '85.2', '85.3', '85.4', '85.5', '85.6']
	queryDict["QB Example"] = ['85.1', '85.2', '85.3', '85.4', '85.5', '85.6']

	# Doc-Topics Dictionary
	docDict = {}
	docDict["a"] = ['85.2', '85.4']
	docDict["b"] = ['85.2']
	docDict["c"] = ['85.2']
	docDict["d"] = []
	docDict["e"] = ['85.1', '85.6']
	docDict["f"] = ['85.1']
	docDict["g"] = ['85.3']
	docDict["h"] = ['85.1']
	docDict["i"] = []
	docDict["j"] = []

	# Ranking Query-Doc Dictionary
	rankingDict = {}
	rankingDict["QA Example"] = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
	rankingDict["QB Example"] = ['a', 'e', 'g', 'b', 'f', 'c', 'h', 'i', 'j', 'd']


	myAlpha = AlphaNDCG(query_topics = queryDict, doc_topics = docDict)
	myAlpha.calculate_Alpha_nDCG(ranking_query_doc = rankingDict)

	print "DCG Values"
	for query in myAlpha.dcg_values:
		print str(query) + ": " + str(myAlpha.dcg_values[query])
	print "\n\n"

	print "nDCG Values"
	for query in myAlpha.ndcg_values:
		print str(query) + ": " + str(myAlpha.ndcg_values[query])
	print "\n"
'''