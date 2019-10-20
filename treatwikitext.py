import mwparserfromhell       #treats braces
import re                     #treat other markups

def  treat_wikitext(text):
	#As the model passes the text to lower,
	#I didn't modified the labeled template with caps
	
	#nowiki and pre
	#list and variations
	#check some numbers
	#template.name.matches("colbegin") | \
	#template.name.matches("defn")
	#Crossreference
	#Talkquotes blocks (and talkquotes include author)
	#Tweets
	#Quote Box
	#Quote frame
	#RQuote
	#CQuote
	#Redo
	#Check recursion problem - citeweb and get depending on size

	def remove_braces(text):
		wikicode = mwparserfromhell.parse(text)
		templates = wikicode.filter_templates()
		
		if not templates:
			return text
		
		for template in templates:
			if template.name.matches("pad"):
				text = text.replace(template.encode('utf-8'), " ")
			elif template.name.matches("block indent"):
				if not template.has("text"):
					text = text.replace(template.encode('utf-8'), template.get(1).value.encode('utf-8'))
				else:
					text = text.replace(template.encode('utf-8'), template.get("text").value.encode('utf-8'))
			elif template.name.matches("Cquote") | \
				 template.name.matches("Quote"): #Correct
				reference = "" #correct cquote parameters
				if template.has("author"):
					reference = "\n --" + template.get("author").value.encode('utf-8') #use dash
				if template.has("title"):
					reference =  reference + ",\n" + template.get("title").value.encode('utf-8')
				if template.has("source"):
					reference = reference + ",\n" + template.get("source").value.encode('utf-8')
				if template.has("text"):
					text = text.replace(template.encode('utf-8'), template.get("text").value.encode('utf-8') + reference)
				elif template.has("l"):
					text = text.replace(template.encode('utf-8'), template.get("l").value.encode('utf-8') + reference)
			elif template.name.matches("font"):
				if not template.has("text"):
					text = text.replace(template.encode('utf-8'), template.get(1).value.encode('utf-8'))
				else:
					text = text.replace(template.encode('utf-8'), template.get("text").value.encode('utf-8'))
			elif template.name.matches("font color"):
				if not template.has("text"):
					text = text.replace(template.encode('utf-8'), template.get(2).value.encode('utf-8'))
				else:
					text = text.replace(template.encode('utf-8'), template.get("text").value.encode('utf-8'))
			elif template.name.matches("strong") | \
			template.name.matches("tq") | \
			template.name.matches("tqq") | \
			template.name.matches("tqi") | \
			template.name.matches("tqqi") | \
			template.name.matches("noitalic") | \
			template.name.matches("nobold") | \
			template.name.matches("yesitalic") | \
			template.name.matches("yesbold") | \
			template.name.matches("nocaps") | \
			template.name.matches("noitalic") | \
			template.name.matches("Smallcaps") | \
			template.name.matches("sc1") | \
			template.name.matches("SC") | \
			template.name.matches("Smallcaps2") | \
			template.name.matches("sc2") | \
			template.name.matches("sc") | \
			template.name.matches("Smallcaps all") | \
			template.name.matches("em"):
				if not template.has("l"):
					text = text.replace(template.encode('utf-8'), template.get(1).value.encode('utf-8'))
				else:
					text = text.replace(template.encode('utf-8'), template.get("text").value.encode('utf-8'))
			elif template.name.matches("lang") | \
				template.name.matches("Verse translation") | \
				template.name.matches("script"):
				text = text.replace(template.encode('utf-8'), template.get(2).value.encode('utf-8'))
			elif template.name.matches("section link"):
				result = ""
				for item in template.params:
					result = result + ", " + item.encode('utf-8')
					#remove last comma
					#put an end
					#special parameters
				text = text.replace(template.encode('utf-8'), result)
			elif template.name.matches("smallcaps all") | \
			template.name.matches("caps") | \
			template.name.matches("not a typo") | \
			template.name.matches("typo"):
				if len(template.params) == 2:
					text = text.replace(template.encode('utf-8'), template.get(1).value.encode('utf-8')+template.get(2).value.encode('utf-8'))
				else:
					text = text.replace(template.encode('utf-8'), template.get(1).value.encode('utf-8'))
			elif template.name.matches("text"):
				result = ""
				for item in template.params:
					result = result + item.encode('utf-8')
				text = text.replace(template.encode('utf-8'), result)
			elif template.name.matches("See above"):
				if len(template.params) == 0:
					text = text.replace(template.encode('utf-8'), "(see above)")
				elif len(template.params) == 1:
					text = text.replace(template.encode('utf-8'), "(see "+ template.get(1).value.encode('utf-8')+")")
			elif template.name.matches("See below"):
				if len(template.params) == 0:
					text = text.replace(template.encode('utf-8'), "(see below)")
				elif len(template.params) == 1:
					text = text.replace(template.encode('utf-8'), "(see "+ template.get(1).value.encode('utf-8')+")")
			elif template.name.matches("strikethrough") | \
				template.name.matches ("Strikethrough color") | \
				 template.name.matches("highlight") | \
				 template.name.matches("highlight round") | \
				 template.name.matches("abbr") | \
				 template.name.matches("subst:poem") | \
				 template.name.matches("small") | \
				 template.name.matches("smaller") | \
				 template.name.matches("larger") | \
				 template.name.matches("big") | \
				 template.name.matches("huge") | \
				 template.name.matches("midsize"):
				text = text.replace(template.encode('utf-8'), template.get(1).value.encode('utf-8'))
			elif template.name.matches("transl") | \
			template.name.matches("resize") | \
			template.name.matches("user link") | \
			template.name.matches("help link") | \
			template.name.matches("u"):
				size = len(template.params)
				text = text.replace(template.encode('utf-8'), template.get(size).value.encode('utf-8'))
			elif re.search("IPAC",template.name.encode('utf-8'), flags=re.IGNORECASE):
				text = text.replace(template.encode('utf-8'), "")
			elif template.name.matches("fullurl") | \
				template.name.matches("unichar") | \
				template.name.matches("Edit") | \
				template.name.matches("Ed right") | \
				template.name.matches("Ed section") | \
				template.name.matches("Ed sup") | \
				template.name.matches("Navbar") | \
				template.name.matches("Vedit") | \
				template.name.matches("About") | \
				template.name.matches("sic") | \
				template.name.matches("float") | \
				template.name.matches("stack") | \
				template.name.matches("multiple image") | \
				template.name.matches("superimpose") | \
				template.name.matches("superimpose2") | \
				template.name.matches("outdent") | \
				template.name.matches("outdent2") | \
				template.name.matches("Color contrast ratio") | \
				bool(re.search("subst:(?!poem)",template.name.encode('utf-8'), flags=re.IGNORECASE)) | \
				template.name.matches("rp") | \
				template.name.matches("cite book") | \
				template.name.matches("cite web") | \
				template.name.matches("citation needed") | \
				template.name.matches("val") | \
				template.name.matches("frac") | \
				template.name.matches("coord") | \
				template.name.matches("closed-open") | \
				template.name.matches("open-open") | \
				template.name.matches("mvar") | \
				template.name.matches("sqrt") | \
				template.name.matches("radic") | \
				template.name.matches("sfrac") | \
				template.name.matches("intmath") | \
				template.name.matches("overset") | \
				template.name.matches("underset") | \
				template.name.matches("bra") | \
				template.name.matches("ket") | \
				template.name.matches("bra-ket") | \
				template.name.matches("math"):
					text = text.replace(template.encode('utf-8'), "")
			elif template.name.matches("clear") | \
				 template.name.matches("clear2") | \
				 template.name.matches("break") | \
				 template.name.matches("-"):
				text = text.replace(template.encode('utf-8'), "\n")
			elif template.name.matches("bracket"):
				if not template.params:
					text = text.replace(template.encode('utf-8'), '[')
				else:
					text = text.replace(template.encode('utf-8'), '['+ template.get(1).value.encode('utf-8') + ']')
				#Treat order
			elif template.name.matches("gaps"):
				result = ""
				for item in template.params:
					result = result + item.encode('utf-8') + " "
				text = text.replace(template.encode('utf-8'), result)
			elif template.name.matches("As of"):
				text = text.replace(template.encode('utf-8'), "")
			elif template.name.matches("color") | \
				 template.name.matches("COLOR") | \
				 template.name.matches("Colored text") | \
				 template.name.matches("COLOUR") | \
				 template.name.matches("Fgcolor") | \
				 template.name.matches("font color") | \
				 template.name.matches("Coloredlink") | \
				 template.name.matches("Background color") | \
				 bool(re.search("xt",template.name.encode('utf-8'), flags=re.IGNORECASE)) | \
				 template.name.matches("strike") | \
				 template.name.matches("center") | \
				 template.name.matches("ISBN"):
				size = len(template.params)
				last = template.get(size).encode('utf-8')
				last = remove_braces(last)
				text = text.replace(template.encode('utf-8'), last)
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
	#ignore ~~~~~ --> unknown
	#ignore [[de:Plankton]] --> unknown
	
	#html markups
	text = re.sub("<math.+?>.+?</math>","",text) #math symbols
	text = re.sub("<hiero.+?>.+?</hiero>","",text) #hieroglyphs
	text = re.sub("<score.+?>.+?</scores>", "", text) #musical notation
	text = re.sub("<table.+?>{.\n}+?<table>", "", text) #table
	text = re.sub("\.(<ref>.+?</ref>)+","<ref></ref>. ",text) #refs
	#can have some incorrect space
	#treat <ref>somet text</ref>
	#incorrect space after dot
	#treat <ref name =...>
	#efn refn variations noteTag last one generates refs ref ref label
	#quote
	text = re.sub("<source.*?>[\d\D]+?</source>","",text)
	text = re.sub("<imagemap.*?>[\d\D]+?</imagemap>","",text)
	text = re.sub("(?!<ref>|</ref>)<.+?>","",text) #other html markups
	
	#links w/ hide 
	text = re.sub("\[\[.+?:(.+?)\(.+?\)\|\]\]", "\\1", text)
	text = re.sub("\[\[.+?:(.+?)\|\]\]", "\\1", text)
	text = re.sub("\[\[(.+?)\(.+?\)\|\]\]", "\\1", text) 
	text = re.sub("\[\[(.+?), .+?\|\]\]", "\\1", text)
	text = re.sub("\[\[:.+?:(.+?)\]\]", "\\1", text)
	text = re.sub("\[\[:(.+?)\]\]", "\\1", text)
	text = re.sub("\[\[/(.+?)/\]\]", "\\1", text)
	#reverse pipe
	
	#square brakets markups
	text = re.sub("\[\[Category:.+?\]\]", "", text)
	text = re.sub("\[\[media:.+?\|.+?\|\]\]", "\\1", text)
	text = re.sub("\[\[Media:.+?\|(.+?)\]\]", "\\1", text)
	text = re.sub("\[\[media:.+?\]\]", "", text)
	text = re.sub("\[\[File.+?\]\]","",text) #image links
	text = re.sub("\[\[Special:.+?\]\]", "", text)
	
	
	text = re.sub("\[//.+?\]", "", text)
	text = re.sub("\[\[.+?\|(.+?)\]\]", "\\1", text) #link w/ synonims
	text = re.sub("\[\[#(.+?)\]\]", "\\1", text) 
	text = re.sub("\[\[(.+?)\]\]", "\\1", text) #link w/ no synonims
	text = re.sub("\[\S+?\]", "", text) #external link w/ noname
	text = re.sub("\[\S+? (.+?)\]", "\\1", text) #external link
	
	return text
