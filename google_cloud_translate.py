import json

# Imports the Google Cloud client library
import string
import requests

import time


myKey = '' # enter key for google cloud translate api

with open('captions_train2014.json') as data_file:    
    datas = json.load(data_file)

output = {}
i = 0
target = 'zh-CN'

output['annotations'] = []
# print (len(data['annotations'])) 414113

filenameBase = "translation"
start = 20000
end = start + 40000
saveToFileEveryByInterval = 1000
text = []

payload = {'q': text, 'target': target, 'key' : myKey}
filename = "_" + str(start) + "_" + str(end) + ".json"
k = 0

lastEnd = 0
subStart = 0
subEnd = 0
numTotal = 0
batch = 100
totalBatch = 0
start_time = 0
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

	if(totalBatch == 16):
		time_elasped = time.time() - start_time
		time_elasped = int(time_elasped)
		time_sleep = (100 - time_elasped)
		time.sleep(time_sleep)
		totalBatch = 0

	if(totalBatch == 0):
		start_time = time.time()

	for j in range(subStart,subEnd):

		annotation = datas['annotations'][j]

		text = annotation['caption']
		
		payload['q'].append(text)

	r = requests.get('https://translation.googleapis.com/language/translate/v2', params=payload)
	print(r.status_code)
	data = r.json()


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

	output['annotations'].extend(tempList)


	if (subEnd % saveToFileEveryByInterval == 0):
		filename = filenameBase + "_" + str(subEnd-saveToFileEveryByInterval) + "_" + str(subEnd) + ".json"
		with open(filename, 'w') as outfile:  
			json.dump(output, outfile)
		output['annotations'] = []
	totalBatch += 1
