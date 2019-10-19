import mwparserfromhell       #treats braces
import re                     #treat other markups

def  treat_wikitext(text):
	#nowiki and pre
	#magic words and variables
	#template.name.matches("plainlist") | \
	#template.name.matches("unbullet list") | \
	#template.name.matches("quote") | \
	#template.name.matches("colbegin") | \
	#template.name.matches("defn")

	def remove_braces(text):
		wikicode = mwparserfromhell.parse(text)
		templates = wikicode.filter_templates()
		
		if not templates:
			return text
		
		for template in templates:
			if template.name.matches("pad"):
				text = text.replace(template.encode('utf-8'), " ")
			elif re.search("IPAC",template.name.encode('utf-8'), flags=re.IGNORECASE):
				text = text.replace(template.encode('utf-8'), "")
			elif template.name.matches("fullurl") | \
				template.name.matches("edit") | \
				template.name.matches("outdent") | \
				template.name.matches("outdent2") | \
				template.name.matches("cite book") | \
				template.name.matches("cite web") | \
				template.name.matches("citation needed") | \
				template.name.matches("math"):
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
				 template.name.matches("center") | \
				 template.name.matches("stack") | \
				 template.name.matches("ISBN"):
				size = len(template.param)
				last = template.param[size-1].encode('utf-8')
				last = remove_braces(last)
				text = text.replace(last,template.encode('utf-8'))
			else:
				text = text.replace(template.encode('utf-8'), "")
		return text

	text = remove_braces(text)
	#remove other markups
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

	return text
