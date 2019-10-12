import re
import requests
import pandas as pd
import mwparserfromhell
from bs4 import BeautifulSoup

session = requests.Session()
URL = "https://en.wikipedia.org/w/api.php"
page = "Pet door"

QUERY = {
    "action": "query",
    "prop" : "revisions", 
	"rvlimit": "1",
	"rvprop": "ids|timestamp|sha1", 
    "format": "json", #Parameters Description Format
}

QUERY["titles"] = page
request1 = session.get(url=URL, params=QUERY)
revision = request1.json()
#get timestamp revision info

PARSE = {
    "action": "parse",
    "prop" : "text|wikitext|revid", 
    "format": "json", #Parameters Description Format
}

PARSE["page"] = page
request2 = session.get(url=URL, params=PARSE)
page = request2.json()

text = page["parse"]["wikitext"]["*"].encode('utf-8') #get text
text = unicode(BeautifulSoup(text, "html.parser")).encode('utf-8')
#Remove html symbols

#Work on wikitext symbols
text = re.sub("\[\[File.*\]\]","",text) #Remove image links
text = re.sub("'''", "",text) #remove extra quotations marks
text = re.sub("''", "'",text) #remove double quotations marks
#text = re.sub('""', '"',text) #remove double quotations marks
text = re.sub("\[\[.+\|(.+?)\]\]", "\\1", text)
#replace link_name that has sinonyms [[Consumer IR|infrared]] 
text = re.sub("\[\[(.+?)\]\]", "\\1", text)
#replace link name w/ no synonims


wikicode = mwparserfromhell.parse(text)
templates = wikicode.filter_templates()
for trash in templates: #remove junk
	text = text.replace(trash.encode('utf-8'), "")

page["parse"]["title"] = re.sub("\s", "_",page["parse"]["title"]) #Put underscores

section_text = re.split("==.*==", text) #Generate sections

section_name =  re.findall("==(.*)==", text) #Get sessions ids
section_name.insert(0, "MAIN_SECTION") #insert MAIN_SECTION


#Remove unecessary sections
for key in section_name:
	if re.search("See also", key):
		index = section_name.index(key)
		section_text.remove(section_text[index])
		section_name.remove(key)

for key in section_name:
	if re.search("References", key):
		index = section_name.index(key)
		section_text.remove(section_text[index])
		section_name.remove(key)

for key in section_name:
	if re.search("External links", key):
		index = section_name.index(key)
		section_text.remove(section_text[index])
		section_name.remove(key)

for key in section_name:
	if re.search("Further reading", key):
		index = section_name.index(key)
		section_text.remove(section_text[index])
		section_name.remove(key)

for i in range(len(section_name)): #Put underscores
	section_name[i] = re.sub("\s", "_",section_name[i])

for i in range(len(section_text)): #Generate paragraphs
	section_text[i] = re.split("\n\n", section_text[i])

#Remove empty paragraphs
for i in range(len(section_text)): 
	while "\n" in section_text[i]:
		section_text[i].remove("\n")
	while "" in section_text[i]:
		section_text[i].remove("")

#Remove \n in paragraphs
for i in range(len(section_text)):
	for j in range(len(section_text[i])):
		section_text[i][j] = re.sub("\n", "", section_text[i][j]) 

citation = [] #get citation
for i in range(len(section_text)):
	paragraph = []
	for j in range(len(section_text[i])):
		if re.search("<ref.*>.*</ref>", section_text[i][j]):
			section_text[i][j] = re.split("<ref.*>.*</ref>", section_text[i][j])  #split in sentences
			if len(section_text[i][j]) == 2 and section_text[i][j][1] == "": #has just one cell and other empty cell = whole paragraph cited
				section_text[i][j] = section_text[i][j][0]
				paragraph.append(True)
			else: #needs to be devided in citations
				sentence = []
				for k in range(len(section_text[i][j])):
					sentence.append(True)
				if section_text[i][j][len(section_text[i][j])-1] == '': 
					sentence.append(True)
				else:
					sentence.append(False)
				paragraph.append(sentence)
		else: #whole paragraph not cited
			paragraph.append(False)
	citation.append(paragraph)

#remove others html marks
for i in range(len(section_text)):
	for j in range(len(section_text[i])):
		if type(section_text[i][j]) == list:
			for k in range(len(section_text[i][j])):
				section_text[i][j][k] = re.sub("<.+?>","",section_text[i][j][k])
		else:
			section_text[i][j] = re.sub("<.+?>","",section_text[i][j])

pageid = unicode(page["parse"]["pageid"])
timestamp = revision["query"]["pages"][pageid]["revisions"][0]["timestamp"]

table = []
for i in range(len(section_text)):
	for j in range(len(section_text[i])):
		if type(section_text[i][j]) == list:
			for k in range(len(section_text[i][j])):
				sentence = {}
				sentence["entity_id"] = page["parse"]["pageid"]
				sentence["revision_id"] = page["parse"]["revid"]
				sentence["timestamp"] = timestamp
				sentence["entity_title"] = page["parse"]["title"]
				sentence["section_id"] = i
				sentence["section"] = section_name[i]
				sentence["prg_idx"] = j+1
				sentence["sentence_idx"] = k+1
				sentence["statement"] = section_text[i][j][k]
				sentence["citation"] = citation[i][j][k]
				table.append(sentence)
		else:
			sentence = {}
			sentence["entity_id"] = page["parse"]["pageid"]
			sentence["revision_id"] = page["parse"]["revid"]
			sentence["timestamp"] = timestamp
			sentence["entity_title"] = page["parse"]["title"]
			sentence["section_id"] = i
			sentence["section"] = section_name[i]
			sentence["prg_idx"] = j+1
			sentence["sentence_idx"] = -1
			sentence["statement"] = section_text[i][j]
			sentence["citation"] = citation[i][j]
			table.append(sentence)

data = pd.DataFrame(table, 
	columns=["entity_id","revision_id","timestamp","entity_title",
	"section_id","section", "prg_idx", "sentence_idx", "statement", "citation"])
data.to_csv("table.txt", sep = "\t", index = False)

