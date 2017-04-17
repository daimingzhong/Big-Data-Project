from __future__ import print_function

import sys
from pyspark import SparkContext
from csv import reader

def output(x):
	dic = {}
	for t in x[1]:
		dic[t[0]] = t[1]
	if not dic.has_key('FELONY'):
		dic['FELONY'] = 0
	if not dic.has_key('MISDEMEANOR'):
		dic['MISDEMEANOR'] = 0
	if not dic.has_key('VIOLATION'):
		dic['VIOSLATION'] = 0
	return (x[0], '%s,%s,%s' % (dic['FELONY'], dic['MISDEMEANOR'], dic['VIOLATION']))
		

if __name__ == "__main__":
        sc = SparkContext()
        tuples = sc.textFile(sys.argv[1], 1).mapPartitions(lambda x: reader(x))
        tuples = tuples.filter(lambda x : len(x) > 13).filter(lambda x : x[11] != '' and x[13]!= '')
        pairs = tuples.map(lambda x : ((x[13].strip().upper(), x[11].strip()), 1))
        result = pairs.reduceByKey(lambda x, y : x + y).map(lambda x : (x[0][0], (x[0][1], x[1]))).groupByKey().map(output)
        result = result.map(lambda x: '%s\t%s' % (x[0],  x[1]))
        result.saveAsTextFile("area_level_amount.out")
        sc.stop()

