# alpha-nDCG
Python implementation of alpha-nDCG

## Dependencies
	* numpy
	* math
	* copy

## Usage (Example from [Clarke, 2008])

Query-Topics Dictionary [A dictionary of topics relevants per query]
```python
queryDict = {}
queryDict["QA Example"] = ['85.1', '85.2', '85.3', '85.4', '85.5', '85.6']
queryDict["QB Example"] = ['85.1', '85.2', '85.3', '85.4', '85.5', '85.6']
```
Doc-Topics Dictionary [A dictionary of topics relevants per document]
```python
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
```

Ranking Query-Doc Dictionary [A dictionary of ranking to calculate the alphaNDCG per query]
```python
rankingDict = {}
rankingDict["QA Example"] = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
rankingDict["QB Example"] = ['a', 'e', 'g', 'b', 'f', 'c', 'h', 'i', 'j', 'd']
```

Returns score
```python
from alpha_nDCG import AlphaNDCG
myAlpha = AlphaNDCG(query_topics = queryDict, doc_topics = docDict, alpha=0.5)
myAlpha.calculate_Alpha_nDCG(ranking_query_doc = rankingDict, depth=10)

print "nDCG Values"
for query in myAlpha.ndcg_values:
	print str(query) + ": " + str(myAlpha.ndcg_values[query])
print "\n"
```

## References
Clarke, Charles LA, et al. "Novelty and diversity in information retrieval evaluation." Proceedings of the 31st annual international ACM SIGIR conference on Research and development in information retrieval. ACM, 2008. [\[pdf\]](http://plg.uwaterloo.ca/~gvcormac/novelty.pdf)
