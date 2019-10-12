import re
import requests
import pandas as pd
import mwparserfromhell

session = requests.Session()
URL = "https://en.wikipedia.org/w/api.php"

PARAMS = {
    "action": "parse",
    "prop" : { #timestamp is wikitext
    	"text", "wikitext","revid","displaytitle"
    },
	"disablelimitreport" : "true",
	"disabletoc" : "true",
	"disablestylededuplication" : "true",
    "page": "The Fergies", 
    "format": "json", #Parameters Description Format
}

request = session.get(url=URL, params=PARAMS)
page = request.json()
text = page["parse"]["wikitext"]["*"].encode('utf-8');

text = re.sub("\[\[File.*\]\]","",text) #Remove image links
text = re.sub("<(?!.+ref).+?>","",text) #remove html marks
text = re.sub("'''", "",text) #remove extra quotations marks
text = re.sub("\[\[.+\|(.+?)\]\]", "\\1", text)
#replace link_name that has sinonyms [[Consumer IR|infrared]] 
text = re.sub("\[\[(.+?)\]\]", "\\1", text)
#replace link name w/ no synonims

wikicode = mwparserfromhell.parse(page["parse"]["wikitext"]["*"])
templates = wikicode.filter_templates()
#Adjust Foreign words? model?
#extra quotation marks

for trash in templates:
	text = text.replace(trash.encode('utf-8'), "")

page["parse"]["title"] = re.sub("\s", "_",page["parse"]["title"]) #Put underscores

section_text = re.split("==.*==", text)
section_text.pop()  #Remove References

section_name =  re.findall("==(.*)==", text) #Get sessions ids
section_name.insert(0, "MAIN_SECTION") #insert MAIN_SECTION
for i in range(len(section_name)): #Put underscores
	section_name[i] = re.sub("\s", "_",section_name[i])
section_name.pop() #Remove References

for i in range(len(section_text)): #Generate paragraphs
	section_text[i] = re.split("\n\n", section_text[i])

for i in range(len(section_text)): #Remove empty paragraphs
	while "\n" in section_text[i]:
		section_text[i].remove("\n")
	while "" in section_text[i]:
		section_text[i].remove("")

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

table = []
for i in range(len(section_text)):
	for j in range(len(section_text[i])):
		if type(section_text[i][j]) == list:
			for k in range(len(section_text[i][j])):
				sentence = {}
				sentence["entity_id"] = page["parse"]["pageid"]
				#revision_id
				#timestamp
				sentence["entity_title"] = page["parse"]["title"]
				sentence["section_id"] = i
				sentence["section"] = section_name[i]
				sentence["prg_idx"] = j+1
				sentence["statement"] = section_text[i][j][k]
				sentence["sentence_idx"] = k+1
				sentence["citation"] = citation[i][j][k]
				sentence["statement"] = section_text[i][j][k]
				table.append(sentence)
		else:
			sentence = {}
			sentence["entity_id"] = page["parse"]["pageid"]
			#revision_id
			#timestamp
			sentence["entity_title"] = page["parse"]["title"]
			sentence["section_id"] = i
			sentence["section"] = section_name[i]
			sentence["prg_idx"] = j+1
			sentence["statement"] = section_text[i][j]
			sentence["sentence_idx"] = -1
			sentence["citation"] = citation[i][j]
			sentence["statement"] = section_text[i][j]
			table.append(sentence)

data = pd.DataFrame(table)
data.to_csv("table.txt", sep = "\t", index = False)

