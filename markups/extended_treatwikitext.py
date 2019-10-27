import mwparserfromhell       #treats braces
import re                     #treat other markups

def  treat_wikitext(text):
	#Ignore caps -> model only uses lower case
	#Ignore quotation -> model only uses sentence by sentence
	#Ignore crossreference
	#Ignore term and defn
	#Html markups-> default get what is inside
	
	#nowiki and pre
	#Check recursion problem - citeweb and get depending on size
	#check numbers and encoding (if possible)

	def remove_braces(text):
		wikicode = mwparserfromhell.parse(text)
		templates = wikicode.filter_templates()
		
		if not templates:
			return text
		
		for template in templates:
			if re.search("<nowiki />",template.encode('utf-8')):
				continue 
			
			if template.name.matches("ref") | \
			   template.name.matches("Ref") | \
			   template.name.matches("refn") | \
			   template.name.matches("efn") | \
			   template.name.matches("efn-lr") | \
			   template.name.matches("efn-la") | \
			   template.name.matches("efn-ua") | \
			   template.name.matches("efn-ur") | \
			   template.name.matches("efn-lg") | \
			   template.name.matches("ref label"):
				text = text.replace(template.encode('utf-8'), "<Ref></Ref>") #standard for the citations
			elif  template.name.matches("pad") | \
				  template.name.matches("in5") | \
				  template.name.matches("indent") | \
				  template.name.matches("px2") | \
				  template.name.matches("vpad") | \
				  template.name.matches("spaces") | \
				  template.name.matches("Nb10") | \
				  template.name.matches("Nb5") | \
				  template.name.matches("fs") | \
				  template.name.matches("quad") | \
				  template.name.matches("zwj") | \
				  template.name.matches("ns") | \
				  template.name.matches("nnbsp"):
				text = text.replace(template.encode('utf-8'), " ")
			elif template.name.matches("Hair space"):
				if template.has("none"):
					text = text.replace(template.encode('utf-8'), "")
				else:
					text = text.replace(template.encode('utf-8'), " ")
			elif template.name.matches("Thinsp"):
				if template.has("l"):
					text = text.replace(template.encode('utf-8'), " "+ template.get(1).value.encode('utf-8') + " ")
				else:
					text = text.replace(template.encode('utf-8'), " ")
			elif template.name.matches("block indent"):
				if not template.has("text"):
					text = text.replace(template.encode('utf-8'), template.get(1).value.encode('utf-8'))
				else:
					text = text.replace(template.encode('utf-8'), template.get("text").value.encode('utf-8'))
#			elif template.name.matches("Unbulleted list"):
#				result = ""
#				for i in range(len(template.params)):
#					if re.search("\=",template.params[i].encode('utf-8')):
#						break
#					result = result + template.params[i].encode('utf-8') + "\n"
#				text = text.replace(template.encode('utf-8'), result)
#			elif template.name.matches("plainlist")|\
#				 template.name.matches("flatlist"):
#				if template.has("1"):
#					text = text.replace(template.encode('utf-8'), template.get("1").value.encode('utf-8'))
#				else:
#					text = text.replace(template.encode('utf-8'), "")
#			elif template.name.matches("Ordered list"):
#				params = template.params()
#				for i in range(len(params)):
#					if string.find(params[i].encode('utf-8'), "="):
#						del params[i]
#						i = i - 1
#				for i in range(len(template.params)):
#					result = result + template.params[i].encode('utf-8') + "\n"
#				text = text.replace(template.encode('utf-8'), result)
#			elif template.name.matches("hlist"):
#				result = ""
#				for i in range(len(template.params)):
#					if re.search("\=",template.params[i].encode('utf-8')):
#						break
#					if i != 0:
#						result = result + ", "
#					result = result + template.params[i].encode('utf-8')
#				text = text.replace(template.encode('utf-8'), result)
#			elif template.name.matches("Div col"):
#				if template.has("content"):
#					text = text.replace(template.encode('utf-8'), template.get("content").value.encode('utf-8'))
#				else:
#					text = text.replace(template.encode('utf-8'), "")
#			elif template.name.matches("talk quote"):
#				reference = ""
#				if template.has("by"):
#					reference = "\n -- User:" + template.get("by").value.encode('utf-8') 
#				if template.has("source"):
#					reference = reference + ", " + template.get("source").value.encode('utf-8')
#				if template.has("text"):
#					text = text.replace(template.encode('utf-8'), template.get("quote").value.encode('utf-8') + reference)
#				elif template.has("1"):
#					text = text.replace(template.encode('utf-8'), template.get("1").value.encode('utf-8') + reference)
#			elif template.name.matches("Cquote"):
#				reference = ""
#				if template.has("author"):
#					reference = "\n --" + template.get("author").value.encode('utf-8') 
#				if template.has("source"):
#					reference = reference + ", " + template.get("source").value.encode('utf-8')
#				if template.has("text"):
#					text = text.replace(template.encode('utf-8'), template.get("quote").value.encode('utf-8') + reference)
#				elif template.has("1"):
#					text = text.replace(template.encode('utf-8'), template.get("1").value.encode('utf-8') + reference)
#			elif template.name.matches("Rquote"):
#				reference = ""
#				if template.has("author"):
#					reference = "\n --" + template.get("author").value.encode('utf-8') 
#				elif template.has("3"):
#					reference = "\n --" + template.get("3").value.encode('utf-8') 
#				if template.has("source"):
#					reference = reference + ", " + template.get("source").value.encode('utf-8')
#				elif template.has("4"):
#					reference = reference + ", " + template.get("4").value.encode('utf-8') 
#				if template.has("quote"):
#					text = text.replace(template.encode('utf-8'), template.get("quote").value.encode('utf-8') + reference)
#				elif template.has("2"):
#					text = text.replace(template.encode('utf-8'), template.get("2").value.encode('utf-8') + reference)
#			elif template.name.matches("Quote"): 
#				reference = ""
#				if template.has("author"):
#					reference = "\n --" + template.get("author").value.encode('utf-8') 
#				if template.has("title"):
#					reference =  reference + ",\n" + template.get("title").value.encode('utf-8')
#				if template.has("source"):
#					reference = reference + ",\n" + template.get("source").value.encode('utf-8')
#				if template.has("text"):
#					text = text.replace(template.encode('utf-8'), template.get("text").value.encode('utf-8') + reference)
#				elif template.has("1"):
#					text = text.replace(template.encode('utf-8'), template.get("1").value.encode('utf-8') + reference)
#			elif template.name.matches("Quote box") | \
#			     template.name.matches("Quote frame"): #Correct
#				reference = ""
#				if template.has("author"):
#					reference = "\n --" + template.get("author").value.encode('utf-8') 
#				elif template.has("2"):
#					reference = "\n --" + template.get("2").value.encode('utf-8')
#				if template.has("title"):
#					reference =  reference + ", " + template.get("title").value.encode('utf-8')
#				elif template.has("3"):
#					text = text.replace(template.encode('utf-8'), template.get("3").value.encode('utf-8') + reference)
#				if template.has("4"):
#					reference = reference + ", " + template.get("4").value.encode('utf-8')
#				if template.has("quote"):
#					text = text.replace(template.encode('utf-8'), template.get("quote").value.encode('utf-8') + reference)
#				elif template.has("1"):
#					text = text.replace(template.encode('utf-8'), template.get("1").value.encode('utf-8') + reference)
#               elif template.name.matches("Poemquote"):
#				reference = ""
#				if template.has("sign"):
#					reference = "\n --" + template.get("sign").value.encode('utf-8') 
#				elif template.has("2"):
#					reference = "\n --" + template.get("2").value.encode('utf-8')
#				if template.has("char"):
#					reference =  reference + ", " + template.get("char").value.encode('utf-8')
#				elif template.has("3"):
#					text = text.replace(template.encode('utf-8'), template.get("3").value.encode('utf-8') + reference)
#				if template.has("source"):
#					reference = reference + ", " + template.get("source").value.encode('utf-8')
#				elif template.has("4"):
#					text = text.replace(template.encode('utf-8'), template.get("4").value.encode('utf-8') + reference)
#				if template.has("quote"):
#					text = text.replace(template.encode('utf-8'), template.get("quote").value.encode('utf-8') + reference)
#				elif template.has("1"):
#					text = text.replace(template.encode('utf-8'), template.get("1").value.encode('utf-8') + reference)
			elif template.name.matches("font color"):
				if not template.has("text"):
					text = text.replace(template.encode('utf-8'), template.get(2).value.encode('utf-8'))
				else:
					text = text.replace(template.encode('utf-8'), template.get("text").value.encode('utf-8'))
			elif (template.name.matches("font") |
			template.name.matches("Nowrap") |
			template.name.matches("strong") |
# template.name.matches("talk quote inline") | \
#			template.name.matches("tq") | \
#			template.name.matches("tqq") | \
#			template.name.matches("tqi") | \
#			template.name.matches("tqqi") | \
			template.name.matches("noitalic") | 
			template.name.matches("nobold") | 
			template.name.matches("yesitalic") | 
			template.name.matches("nocaps") | 
			template.name.matches("noitalic") | 
			template.name.matches("Smallcaps") | 
			template.name.matches("sc1") | 
			template.name.matches("SC") | 
			template.name.matches("Smallcaps2") | 
			template.name.matches("sc2") | 
			template.name.matches("em")):
				if template.has("text"):
					text = text.replace(template.encode('utf-8'), template.get("text").value.encode('utf-8'))
				else:
					text = text.replace(template.encode('utf-8'), template.get(1).value.encode('utf-8'))
			elif template.name.matches("lang") | \
				template.name.matches("align") | \
				template.name.matches("Verse translation") | \
				template.name.matches("script"):
				text = text.replace(template.encode('utf-8'), template.get(2).value.encode('utf-8'))
			elif template.name.matches("section link"):
				result = ""
				if not template.has("2"):
					result = template.get(1).value.encode('utf-8')
				elif not template.has("3"):
					result = template.get(1).value.encode('utf-8') + "#"+ template.get(2).value.encode('utf-8')
				else:
					param = template.params
					result = param[0].encode('utf-8') + ": " 
					for i in range(len(param)-1):
						if i != 0:
							result = result + ", "
						result = result + param[i+1].encode('utf-8')
				text = text.replace(template.encode('utf-8'), result)
			elif  template.name.matches("Smallcaps all") | \
			template.name.matches("sc") | \
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
				 template.name.matches("Strike") | \
				 template.name.matches("S") | \
				 template.name.matches("Strikethrough color") | \
				 template.name.matches("highlight") | \
				 template.name.matches("highlight round") | \
				 template.name.matches("abbr") | \
				 template.name.matches("subst:poem") | \
				 template.name.matches("small") | \
				 template.name.matches("smaller") | \
				 template.name.matches("larger") | \
				 template.name.matches("bigger") | \
				 template.name.matches("big") | \
				 template.name.matches("huge") | \
				 template.name.matches("samp"):
				text = text.replace(template.encode('utf-8'), template.get(1).value.encode('utf-8'))
			elif template.name.matches("midsize"):
				if template.has("height"):
					text = text.replace(template.encode('utf-8'), template.params[1].encode('utf-8'))
				else:
					text = text.replace(template.encode('utf-8'), template.get(1).value.encode('utf-8'))
			elif bool(re.search("IPA",template.name.encode('utf-8'), flags=re.IGNORECASE)) | \
				template.name.matches("Fullurl") | \
				template.name.matches("unichar") | \
				template.name.matches("Div col end") | \
				template.name.matches("endplainlist") | \
				template.name.matches("startflatlist") | \
				template.name.matches("endflatlist") | \
				template.name.matches("Reflist") | \
				template.name.matches("Refbegin") | \
				template.name.matches("Refend") | \
				template.name.matches("rp") | \
				template.name.matches("glossary") | \
				template.name.matches("term") | \
				template.name.matches("defn") | \
				template.name.matches("Edit") | \
				template.name.matches("Ed right") | \
				template.name.matches("Edit section") | \
				template.name.matches("Edit sup") | \
				template.name.matches("Navbar") | \
				template.name.matches("Vedit") | \
				template.name.matches("About") | \
				template.name.matches("sic") | \
				template.name.matches("float") | \
				template.name.matches("stack") | \
				template.name.matches("multiple image") | \
				template.name.matches("Superimpose") | \
				template.name.matches("Superimpose2") | \
				template.name.matches("outdent") | \
				template.name.matches("outdent2") | \
				template.name.matches("Color contrast ratio") | \
				template.name.matches("cite book") | \
				template.name.matches("cite web") | \
				template.name.matches("citation needed") | \
				template.name.matches("Crossreference") | \
				template.name.matches("Quote") | \
				template.name.matches("Poemquote") | \
				template.name.matches("Gbq") | \
				template.name.matches("Cquote") | \
				template.name.matches("Rquote") | \
				template.name.matches("Quote frame") | \
				template.name.matches("Quote box") | \
				template.name.matches("tweet") | \
				template.name.matches("talk quote inline") | \
				template.name.matches("tq") | \
				template.name.matches("tqq") | \
				template.name.matches("tqi") | \
				template.name.matches("tqqi") | \
				template.name.matches("Talk quote block") | \
				template.name.matches("tq2") | \
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
				template.name.matches("math") | \
				template.name.matches("As of") | \
				template.name.matches("Infobox"):
					text = text.replace(template.encode('utf-8'), "")
			elif template.name.matches("clear") | \
				 template.name.matches("clear left") | \
				 template.name.matches("clear right") | \
				 template.name.matches("clear2") | \
				 template.name.matches("break"):
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
			elif template.name.matches("transl") | \
				 template.name.matches("resize") | \
				 template.name.matches("user link") | \
				 template.name.matches("u") | \
				 template.name.matches("help link") | \
				 template.name.matches("color") | \
				 template.name.matches("COLOR") | \
				 template.name.matches("Colored text") | \
				 template.name.matches("COLOUR") | \
				 template.name.matches("Fgcolor") | \
				 template.name.matches("font color") | \
				 template.name.matches("Coloredlink") | \
				 template.name.matches("Background color") | \
				 bool(re.search("xt",template.name.encode('utf-8'), flags=re.IGNORECASE)) | \
				 template.name.matches("center") | \
				 template.name.matches("ISBN"):
				size = len(template.params)
				last = template.get(size).encode('utf-8')
				#last = remove_braces(last)
				text = text.replace(template.encode('utf-8'), last)
			else:
				text = text.replace(template.encode('utf-8'), "")
		return text

	text = remove_braces(text)
	
	#If not inside nowiki or pre
	#For a sequence ignores
	#[[ wp:pagename <nowiki />| page name ]]
	#testar nowiki em cima tbm
	
	#remove tables
	text = re.sub("\{\|[\d\D]+?\|\}", "", text)

	text = re.sub("----","",text) #horizontal rule
	#lists, indentation, description -> uses symbols -> ignore
	text = re.sub("'''''", "",text) #bold and italics
	text = re.sub("'''", "",text) #bold 
	text = re.sub("''", "",text) #italics
	
	text = re.sub('&nbsp', '\s',text) #non-breaking space
	
	#ignore special caracters
	#ignore ~~~~~ --> unknown
	#ignore [[de:Plankton]] --> unknown
	
	#remove html markups
	text = re.sub("<math[\d\D]*?>[\d\D]+?</math>","",text) #math symbols
	text = re.sub("<hiero[\d\D]*?>[\d\D]+?</hiero>","",text) #hieroglyphs
	text = re.sub("<score[\d\D]*?>[\d\D]+?</score>", "", text) #musical notation
	text = re.sub("<table[\d\D]*?>[\d\D]+?<table>", "", text) #table
	text = re.sub("<source.*?>[\d\D]+?</source>","",text)
	text = re.sub("<imagemap.*?>[\d\D]+?</imagemap>","",text)
	
	#references marked as <ref><\ref> and <Ref><\Ref> 
	text = re.sub('<ref name=(\w|\!|\$|\%|\&|\(|\)|\*|\,|\-|\.|\:|\;|<|\@|\[|\]|\^|\_|\`|\{|\||\}|\"|\~)+?/>','<ref></ref>',text)
	text = re.sub("\.( *?<ref[\d\D]*?>.*?</ref>)+","<ref></ref>. ",text) #refs
	text = re.sub("\.( *?<Ref></Ref>)+","<Ref></Ref>. ",text)
	text = re.sub("(?!<ref[\d\D]*?>|</ref>|<Ref>|</Ref>)<.*?>","",text) #other html markups
	
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
