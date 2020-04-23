import _pickle as c
import os
from sklearn import *
from collections import Counter

#from spam import d



def load(clf_file):
    with open(clf_file,'rb')as fp:
        clf = c.load(fp)
    return clf
	
def load_dic(dic_file):
	with open(dic_file,'rb') as dic1:
		dic2 = c.load(dic1)
	return dic2

def detect(x):
	i=0
	while True:
		features = []
		#inp = input("input>>>").split()
		#x="good morning"
		y=x.split()

		
		#if inp[0] =="exit":
		#	break
		
		if i==1:
			break
		
		for word in d:
			features.append(y.count(word[0]))
			
			#print(features)
		#print(inp.count(word))
		res =clf.predict([features])
		#print(res)
		#print(["Not Spam","Spam!"][res[0]])
		z=(["Not Spam","Spam!"][res[0]])
		print(z)
		i+=1
		return z

	
clf = load("text-classifier.mdl")	
#d = make_dict()
d=load_dic("dic.txt")
a="have a nice day"
#detect(a)

"""
while True:
	features = []
	#inp = input("input>>>").split()
	x="good morning"
	y=x.split()

	
	#if inp[0] =="exit":
	#	break
	
	if i==1:
		break
	
	for word in d:
		features.append(y.count(word[0]))
		
		#print(features)
	#print(inp.count(word))
	res =clf.predict([features])
	#print(res)
	#print(["Not Spam","Spam!"][res[0]])
	z=(["Not Spam","Spam!"][res[0]])
	print(z)
	i+=1
"""

