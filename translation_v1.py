import json

# Imports the Google Cloud client library
import string
import requests

myKey = 'AIzaSyC6JQ8SVapwRpzSMQJMgiwfYsmLGWCe3to'

with open('captions_train2014.json') as data_file:    
    datas = json.load(data_file)

output = {}
i = 0
target = 'zh-CN'

output['annotations'] = []
# print (len(data['annotations'])) 414113

filename = "translation"
start = 100000
end = 200000

text = []

payload = {'q': text, 'target': target, 'key' : myKey}
filename += "_" + str(start) + "_" + str(end) + ".json"
k = 0
total_100 = 0
lastEnd = 0
subStart = 0
subEnd = 0
for i in range(start,end):
	if (i == start):
		subStart = start
	else:
		subStart = subEnd

	subEnd = subStart + 100
	
	payload['q'] = []

	for j in range(subStart,subEnd):

		annotation = datas['annotations'][j]

		text = annotation['caption']
		
		payload['q'].append(text)

	r = requests.get('https://translation.googleapis.com/language/translate/v2', params=payload)
	data = r.json()

	m = 0
	#print(type(translated_texts))
	translationList = data['data']['translations']
	tempList = []
	for k in range(subStart,subEnd):
		annotation = datas['annotations'][j]
		translated = {}
		translated['image_id'] = annotation['image_id']
		translated['id'] = annotation['id']
		translated['text'] = annotation['caption']
		translated['caption'] = translationList[m]['translatedText']
		tempList.append(translated)
		m += 1

	output['annotations'].append(tempList)

with open(filename, 'w') as outfile:  
	json.dump(output, outfile)

