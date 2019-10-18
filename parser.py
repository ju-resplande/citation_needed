import re                     #treat wikitext
import requests               #parse wikipedia
import pandas as pd           #generate table
import mwparserfromhell       #treats {}
import nltk.data              #break into sentences

session = requests.Session()
URL = "https://en.wikipedia.org/w/api.php"
page = "The Fergies"

QUERY = {
    "action": "query",
    "prop" : "revisions", 
	"rvlimit": "1",
	"rvprop": "ids|timestamp", 
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

#Work on wikitext markups
wikicode = mwparserfromhell.parse(text)
templates = wikicode.filter_templates()

def remove_cases(templates, text):
	for template in templates:
		if template.name.matches("pad"):
			text = text.replace(template.encode('utf-8'), " ")
		elif re.search("IPAC",template.name.encode('utf-8'), flags=re.IGNORECASE):
			text = text.replace(template.encode('utf-8'), "")
		elif template.name.matches("fullurl"):
			text = text.replace(template.encode('utf-8'), "")
		elif template.name.matches("clear") | \
			 template.name.matches("break") | \
			 template.name.matches("-"):
			text = text.replace(template.encode('utf-8'), "\n")
		elif template.name.matches("As of"):
			text = text.replace(template.encode('utf-8'), "")
		elif template.name.matches("color") | \
			 template.name.matches("font color") | \
			 bool(re.search("xt",template.name.encode('utf-8'), flags=re.IGNORECASE)) | \
			 template.name.matches("strike") | \
			 template.name.matches("stack") | \
			 template.name.matches("ISBN"):
			text = text.replace(template.param[len(template.param)-1].encode('utf-8'), "")
			#make recursion
		else:
			text = text.replace(template.encode('utf-8'), "")
	return text

text = remove_cases(templates, text)

text = re.sub("\{\|[\d\D]+?\|\}", "", text)
#--->test #REDIRECT [[United States]]

text = re.sub("----","",text) #horizontal rule
#lists, indentation, description -> uses symbols -> ignore
text = re.sub("'''''", "",text) #bold and italics
text = re.sub("'''", "",text) #bold 
text = re.sub("''", "",text) #italics
text = re.sub('&nbsp', '\s',text) #non-breaking space
#ignore special caracters
text = re.sub("<math>.+?</math>","",text) #math symbols
text = re.sub("<hiero>.+?</hiero>","",text) #hieroglyphs
#links w/ hide 
text = re.sub("\[\[(.+?)\(.+?\)\|\]\]", "\\1", text) 
text = re.sub("\[\[(.+?), .+?\|\]\]", "\\1", text)
text = re.sub("\[\[Wikipedia:(.+?)\(.+?\)\|\]\]", "\\1", text) 
text = re.sub("\[\[Wikipedia:(.+?)\|\]\]", "\\1", text)
#ignore [[de:Plankton]] --> unknown
text = re.sub("\[\[:Category:(.+?)\|\]\]", "\\1", text)
text = re.sub("\[\[:Category:(.+?)\]\]", "Category:\\1", text)
text = re.sub("\[\[Category:.+?\]\]", "", text)
text = re.sub("\[\[media:.+?\|.+?\|\]\]", "\\1", text)
text = re.sub("<score>.+?</scores>", "", text) #musical notation
text = re.sub("\[\[File.+?\]\]","",text) #image links
text = re.sub("\[\[Media:.+?\|(.+?)\]\]", "\\1", text)
text = re.sub("<table>{.\n}+?<table>", "", text)
#ignore ~~~~~ --> unknown
text = re.sub("\[\[media:.+?\]\]", "", text)
text = re.sub("\[//.+?\]", "", text)
text = re.sub("\[\[Special:.+?\]\]", "", text)
text = re.sub("<!--.+?-->", "", text)
text = re.sub("\[\[.+\\|(.+?)\]\]", "\\1", text) #link w/ synonims
text = re.sub("\[\[(.+?)\]\]", "\\1", text) #link w/ no synonims
text = re.sub("\.(<ref></ref>)+","<ref></ref>. ",text)
text = re.sub("^(?!<ref></ref>. )<.+?>","",text) #other html markups

page["parse"]["title"] = re.sub("\s", "_",page["parse"]["title"]) #Put underscores

section_text = re.split("==.*==", text) #Generate sections
section_name = re.findall("==(.*)==", text) #Get sessions ids
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

for i in range(len(section_text)): #break into paragraphs
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

#break into sentences
nltk.download('punkt')
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
for i in range(len(section_text)):
	for j in range(len(section_text[i])):
			section_text[i][j] = tokenizer.tokenize(section_text[i][j])

#get citation booleans
citation = []
for i in range(len(section_text)):
	paragraph = []
	for j in range(len(section_text[i])):
		sentence = []
		for k in range(len(section_text[i][j])):
			if re.findall("<ref></ref>", section_text[i][j][k]):
				section_text[i][j][k] = re.sub("<ref></ref>", "", section_text[i][j][k])
				if re.findall("\w", section_text[i][j][k]):
					sentence.append(True)
				else:
					sentence[len(sentence)-1] = True
					section_text[i][j].remove(section_text[i][j][k])
					k = k - 1
			else:
				sentence.append(False)
			
		paragraph.append(sentence)
	citation.append(paragraph)

pageid = unicode(page["parse"]["pageid"])
timestamp = revision["query"]["pages"][pageid]["revisions"][0]["timestamp"]

table = []
for i in range(len(section_text)):
	for j in range(len(section_text[i])):
			for k in range(len(section_text[i][j])):
				sentence = {}
				sentence["entity_id"] = page["parse"]["pageid"]
				sentence["revision_id"] = page["parse"]["revid"]
				sentence["timestamp"] = timestamp
				sentence["entity_title"] = page["parse"]["title"]
				sentence["section_id"] = i
				sentence["section"] = section_name[i]
				sentence["prg_idx"] = j
				sentence["sentence_idx"] = k
				sentence["statement"] = section_text[i][j][k]
				sentence["citation"] = citation[i][j][k]
				table.append(sentence)

data = pd.DataFrame(table, 
	columns=["entity_id","revision_id","timestamp","entity_title",
	"section_id","section", "prg_idx", "sentence_idx", "statement", "citation"])
data.to_csv("table.txt", sep = "\t", index = False)

