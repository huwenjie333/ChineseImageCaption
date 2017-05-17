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
end = 101000

text = []

payload = {'q': text, 'target': target, 'key' : myKey}
filename += "_" + str(start) + "_" + str(end) + ".json"
k = 0

lastEnd = 0
subStart = 0
subEnd = 0
numTotal = 0
batch = 100
for i in range(start, end, batch):
	# if (i == start):
	# 	subStart = start
	# else:
	# 	subStart = subEnd

	# if(subStart == end):
	# 	break
	# subEnd = subStart + 100
	subStart = i
	subEnd = i + batch
	subfile = "batch_" + str(subStart) + "_" + str(subEnd) + ".json"
	
	payload['q'] = []

	for j in range(subStart,subEnd):

		annotation = datas['annotations'][j]

		text = annotation['caption']
		
		payload['q'].append(text)

	r = requests.get('https://translation.googleapis.com/language/translate/v2', params=payload)
	data = r.json()

	with open(subfile, 'w') as subout:
		json.dump(data, subout)


	m = 0
	
	translationList = data['data']['translations']
	tempList = []
	for k in range(subStart,subEnd):
		annotation = datas['annotations'][k]
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

