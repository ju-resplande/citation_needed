import re
import requests
import mwparserfromhell
import pandas as pd
import nltk.data

session = requests.Session()
URL = "https://en.wikipedia.org/w/api.php"

PARAMS = {
    "action": "parse",
    "prop" : { #timestamp is wikitext
    	"revid","text","wikitext", "displaytitle",
    },
	"disablelimitreport" : "true",
	"disabletoc" : "true",
	"disablestylededuplication" : "true",
    "page": "Pet door", 
    "format": "json", #Parameters Description Format
}

request = session.get(url=URL, params=PARAMS)
page = request.json()

wikicode = mwparserfromhell.parse(page["parse"]["wikitext"]["*"])
templates = wikicode.filter_templates()
text = page["parse"]["wikitext"]["*"].encode('utf-8');


for trash in templates:
	text = text.replace(trash.encode('utf-8'), "")

text = re.sub("\[\[.*\]\]","",text)
text = re.sub("<.*>.*</.*>","",text)
text = re.sub("''","'", text)
#Find more trash removers nltk

section_name =  re.findall("==(.*)==", text) #Get sessions ids
section_name.pop() #Remove References

section_text = re.split("==.*==", text)
section_text.pop()  #Remove References

nltk.download('punkt')
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
for i in range(len(section_text)-1):
	section_text[i] = tokenizer.tokenize(section_text[i])
 
table = []
for i in range(len(section_text)-1):
	for j in range(len(section_text[i])):
		sentence = {}
		sentence["entity_id"] = page["parse"]["pageid"]
		#revision_id
		#timestamp
		sentence["entity_title"] = page["parse"]["title"]
		sentence["section_id"] = i
		if i == 0:
			sentence["section"] = "MAIN_SECTION"
		else:
			sentence["section"] = section_name[i-1]
		#prg_idx
		#sentence_idx
		sentence["statement"] = section_text[i][j]
		table.append(sentence)


data = pd.DataFrame(table)
data.to_csv("ex.txt", sep = "\t", index = False)

