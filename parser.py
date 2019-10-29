import re                     
import requests               #parse wikipedia
import pandas as pd           #generate table
import nltk.data              #break into sentences
from treatwikitext import treat_wikitext 

class Page:
	def __init__(self, URL, name):
		self.name = name
		self.URL = URL

	def generate_page(self):
		session = requests.Session()
		
		PARSE = {
			"action": "parse",
			"prop" : "wikitext|revid|sections", 
			"format": "json", #Parameters Description Format
		}

		PARSE["page"] = self.name
		request2 = session.get(url=self.URL, params=PARSE)
		page = request2.json()
		
		try:	
			redirect = re.search("\#REDIRECT \[\[(.+?)\]\]" ,page["parse"]["wikitext"]["*"])
		except:
			print "Page "+ self.name + " doesn't exist. (Case sensitive)"
			exit()
		
		if redirect:
			self.name = redirect.groups()[0]
			PARSE["page"] = self.name
			request2 = session.get(url=self.URL, params=PARSE)
			page = request2.json()

		text = page["parse"]["wikitext"]["*"].encode('utf-8') #get text
		
		QUERY = {
			"action": "query",
			"prop" : "revisions", 
			"rvlimit": "1",
			"rvprop": "timestamp", 
			"format": "json", #Parameters Description Format
		}

		QUERY["titles"] = self.name
		request1 = session.get(url=self.URL, params=QUERY)
		revision = request1.json() #get timestamp revision info

		self.text = treat_wikitext(text)
		self.page = page
		self.revision = revision
	def generate_sections(self):
		self.page["parse"]["title"] = re.sub("\s", "_",self.page["parse"]["title"]) #Put underscores
		section_text = re.split("==.+==", self.text)
		section_name = re.findall("==(.+?)==", self.text)
		for i,v in enumerate(section_name):
			section_name[i] = re.sub("=", "", section_name[i])
		section_name.insert(0, "MAIN_SECTION") #insert MAIN_SECTION
		
		#Remove unecessary sections
		ignore_sections = ["See also", "References", "External links", "Further reading"]
		
		for name in ignore_sections:
			for key in section_name:
				if re.search(name, key):
					index = section_name.index(key)
					section_text.remove(section_text[index])
					section_name.remove(key)

		for i, v in enumerate(section_name): #Put underscores
			section_name[i] = re.sub(" ", "_", section_name[i])
		
		self.section_name = section_name
		self.section_text = section_text
		return section_name, section_text

	def generate_paragraphs(self):
		for i,v in enumerate(self.section_text): #break into paragraphs
			self.section_text[i] = re.split("\n\n", self.section_text[i])

		#Remove empty paragraphs
		for i,v in enumerate(self.section_text): 
			while "\n" in self.section_text[i]:
				self.section_text[i].remove("\n")
			while "" in self.section_text[i]:
				self.section_text[i].remove("")

		#Remove \n in paragraphs
		for i,v in enumerate(self.section_text):
			for j,w in enumerate(self.section_text[i]):
				self.section_text[i][j] = re.sub("\n", "", self.section_text[i][j])

	def generate_sentences(self):
		#break into sentences
		nltk.download('punkt')
		tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
		for i,v in enumerate(self.section_text):
			for j,w in enumerate(self.section_text[i]):
					self.section_text[i][j] = tokenizer.tokenize(self.section_text[i][j].decode("utf-8"))

		#get citation booleans
		citation = []
		for i,v in enumerate(self.section_text):
			paragraph = []
			for j,w in enumerate(self.section_text[i]):
				sentence = []
				for k,t in enumerate(self.section_text[i][j]):
					#if len(self.section_text[i][j][k].split(" ")) <= 2:
						#self.section_text[i][j].remove(self.section_text[i][j][k])
						#continue
					
					if re.findall("<ref>[\d\D]*?</ref>|<Ref>[\d\D]*?</Ref>", self.section_text[i][j][k]):
						self.section_text[i][j][k] = re.sub("<ref>[\d\D]*?</ref>|<Ref>[\d\D]*?</Ref>", "", self.section_text[i][j][k])

						if re.findall("\w", self.section_text[i][j][k]):
							sentence.append(True)
						else:
							if sentence:
								sentence[-1] = True
							self.section_text[i][j].remove(self.section_text[i][j][k])
							k = k - 1
					else:
						sentence.append(False)
				paragraph.append(sentence)
			citation.append(paragraph)
		self.citation = citation


	def generate_table(self, txt):
		pageid = unicode(self.page["parse"]["pageid"])
		timestamp = self.revision["query"]["pages"][pageid]["revisions"][0]["timestamp"]

		table = []
		for i,v in enumerate(self.section_text):
			for j,w in enumerate(self.section_text[i]):
					for k,t in enumerate(self.section_text[i][j]):
						sentence = {}
						sentence["entity_id"] = self.page["parse"]["pageid"]
						sentence["revision_id"] = self.page["parse"]["revid"]
						sentence["timestamp"] = timestamp
						sentence["entity_title"] = self.page["parse"]["title"]
						sentence["section_id"] = i
						sentence["section"] = self.section_name[i]
						sentence["prg_idx"] = j
						sentence["sentence_idx"] = k
						sentence["statement"] = self.section_text[i][j][k]
						sentence["citations"] = self.citation[i][j][k]
						table.append(sentence)

		data = pd.DataFrame(table, 
			columns=["entity_id","revision_id","timestamp","entity_title",
			"section_id","section", "prg_idx", "sentence_idx", "statement", "citations"])
		data.to_csv(txt, sep = "\t", index = False, encoding= "utf-8")
