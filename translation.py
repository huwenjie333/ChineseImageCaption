import json

# Imports the Google Cloud client library
# from google.cloud import translate
import string
import requests




with open('captions_train2014.json') as data_file:    
    datas = json.load(data_file)

output = {}
i = 0
target = 'zh-CN'
# translate_client = translate.Client()

output['annotations'] = []
# print (len(data['annotations'])) 414113

filename = "translation"
start = 100
end = 200

text = []
myKey = 'AIzaSyC6JQ8SVapwRpzSMQJMgiwfYsmLGWCe3to'
payload = {'q': text, 'target': target, 'key' : myKey}
filename += "_" + str(start) + "_" + str(end) + ".json"
k = 0
for i in range(start,end):
	# if (k == 201):
	#  	break
	annotation = datas['annotations'][i]
	text = annotation['caption']
	translated = {}
	translated['image_id'] = annotation['image_id']
	translated['id'] = annotation['id']
	translated['text'] = text
	payload['q'].append(text)
	#print(text.encode('utf-8'))
	k+=1

	# translation = translate_client.translate(
	# 	text,
	# 	target_language=target)

	# translated['caption'] = translation['translatedText']

	# output['annotations'].append(translated)

r = requests.get('https://translation.googleapis.com/language/translate/v2', params=payload)
data = r.json()
	
print(data['data']['translations'])

for translation in data['data']['translations']:
	print(translation['translatedText'].encode('utf-8'))
# with open(filename, 'w') as outfile:  
# 	json.dump(output, outfile)

    # print (len(data['annotations']))
# Instantiates a client
# translate_client = translate.Client()

# # The text to translate
# text = data['annotations'][0]['caption']
# # The target language
# target = 'zh-CN'

# #Translates some text into Russian
# translation = translate_client.translate(
#     text,
#     target_language=target)

# output = {}
# output['caption'] = translation['translatedText']

# with open('translated.json', 'w') as outfile:  
#     json.dump(output, outfile)

# print(u'Text: {}'.format(text))

# print(translation['translatedText'].encode('utf-8'))


