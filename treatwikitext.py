import mwparserfromhell       #treats braces
import re                     #treat other markups

def  treat_wikitext(text):
	def remove_braces(text):
		wikicode = mwparserfromhell.parse(text)
		templates = wikicode.filter_templates()
		
		for template in templates:
			if re.search("<( |)nowiki( |)/>", template.encode("utf-8")):
				continue
			if template.name.matches("harv") | \
			   template.name.matches("harvcol") | \
			   template.name.matches("harvnb") | \
			   template.name.matches("harvp") | \
			   template.name.matches("sfn") | \
			   template.name.matches("sfnp") | \
			   template.name.matches("sfnm") | \
			   template.name.matches("ref") | \
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
			elif template.name.matches("harvcoltxt")| \
			     template.name.matches("harvcolnb"):
			     result = template.get(1).value.encode("utf-8")
			     if len(template.params) == 5:
			     						result = result + " & " +  template.get(2).value.encode("utf-8")
			     elif len(template.params) == 6:
					result = result + ", " +  template.get(2).value.encode("utf-8")  + " & " +  template.get(3).value.encode("utf-8")
			     elif  len(template.params) > 6:
			     	result = result + " et al."
			     result = result + " " + "<Ref></Ref>"
			     text = text.replace(template.encode('utf-8'), result)
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
			elif template.name.matches("Thinsp") | \
				 template.name.matches("Plain space"):
				if template.has(1):
					text = text.replace(template.encode('utf-8'), " "+ template.get(1).value.encode('utf-8') + " ")
				else:
					text = text.replace(template.encode('utf-8'), " ")
			elif template.name.matches("thinspace"):
				result = "" 
				for item in template.params:
						result = result + item.encode("utf-8") + " "
				text = text.replace(template.encode('utf-8'), result)
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
			elif (template.name.matches("Hanging indent") |
			template.name.matches("block indent") |
			template.name.matches("font") |
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
			template.name.matches("em") | 
			template.name.matches("white") | 
			template.name.matches("silver (color)") | 
			template.name.matches("gray") | 
			template.name.matches("black") | 
			template.name.matches("hot pink") | 
			template.name.matches("pink") | 
			template.name.matches("red") | 
			template.name.matches("darkRed") | 
			template.name.matches("maroon") | 
			template.name.matches("brown") | 
			template.name.matches("orange") | 
			template.name.matches("gold (color)") | 
			template.name.matches("yellow") | 
			template.name.matches("olive") | 
			template.name.matches("lime") | 
			template.name.matches("green") |
			template.name.matches("aqua") | 
			template.name.matches("cyan") | 
			template.name.matches("teal") | 
			template.name.matches("blue") | 
			template.name.matches("navy (color)") | 
			template.name.matches("purple") | 
			template.name.matches("fuchsia") |
			template.name.matches("magenta") |
			template.name.matches("border") | 
			template.name.matches("outline color") |
			template.name.matches("swatch inline") |
			template.name.matches("smalldiv") |
			template.name.matches("underline") |
			template.name.matches("unline") |
			template.name.matches("undline") |
			template.name.matches("under") |
			template.name.matches("Italics after") |
			template.name.matches("Avoid wrap") |
			template.name.matches("avoidwrap") |
			template.name.matches("awrap")):
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
			elif template.name.matches("nowraplinks"):
				if template.has(1):
					text = text.replace(template.encode('utf-8'), template.get(1).value.encode('utf-8'))
				else:
					text = text.replace(template.encode('utf-8'), "")
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
				 template.name.matches("samp") | \
				 template.name.matches("Pre") | \
				 bool(re.search("xt",template.name.encode('utf-8'))):
				text = text.replace(template.encode('utf-8'), template.get(1).value.encode('utf-8'))
			elif template.name.matches("Pre2"):
				if len(template.params) == 1:
					text = text.replace(template.encode('utf-8'), template.get(1).value.encode('utf-8'))
				else:
					text = text.replace(template.encode('utf-8'), template.get(2).value.encode('utf-8'))
			elif template.name.matches("midsize"):
				if template.has("height"):
					text = text.replace(template.encode('utf-8'), template.params[1].encode('utf-8'))
				else:
					text = text.replace(template.encode('utf-8'), template.get(1).value.encode('utf-8'))
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
				 template.name.matches("color") | \
				 template.name.matches("COLOR") | \
				 template.name.matches("Colored text") | \
				 template.name.matches("COLOUR") | \
				 template.name.matches("Fgcolor") | \
				 template.name.matches("font color") | \
				 template.name.matches("Coloredlink") | \
				 template.name.matches("Background color") | \
				 template.name.matches("center") | \
				 template.name.matches("ISBN"):
				size = len(template.params)
				last = template.get(size).encode('utf-8')
				text = text.replace(template.encode('utf-8'), last)
			elif template.name.matches("--)"):
				text = text.replace(template.encode('utf-8'), " ) ")
			elif template.name.matches("-?"):
				text = text.replace(template.encode('utf-8'), " ? ")
			elif template.name.matches("Querylink"):
				text = text.replace(template.encode('utf-8'), template.params[2].encode("utf-8"))
			elif template.name.matches("bl"):
				if template.has(2):
					text = text.replace(template.encode('utf-8'), template.get(2).value.encode("utf-8"))
				else:
					text = text.replace(template.encode('utf-8'), "")
			else:
				text = text.replace(template.encode('utf-8'), "")
		return text

	def treat_nowiki(text):
		wikicode = mwparserfromhell.parse(text)
		templates = wikicode.filter_templates()
		for template in templates:
			if template.name.matches("nowiki"):
				text = text.replace(template.encode('utf-8'), "<Nowiki>"+ template.get(1).value.encode('utf-8') + "</Nowiki>")
		return text
	
	def replacemarkup(string, sub, text):
		found = re.findall("("+string+")",text)
		for item in found:
			if re.search("\\\\", sub) and type(item) != str:
				if not re.search("<( |)nowiki( |)>", item[0]):
					text = text.replace(item[0],item[-1])
			elif type(item) != str:
				if not re.search("<( |)nowiki( |)>", item[0]):
					text = text.replace(item[0],sub)
			else:
				if not re.search("<( |)nowiki( |)>", item):
					text = text.replace(item,sub)
		return text
	
	text = treat_nowiki(text)
	text = re.split("(<( |)nowiki( |)>[\d\D]*?</( |)nowiki( |)>|<Nowiki>[\d\D]*?</Nowiki>)", text)
	
	for i in range(len(text)):
		if not re.match("<( |)nowiki( |)>[\d\D]*?</( |)nowiki( |)>|<Nowiki>[\d\D]*?</Nowiki>", text[i]):
			text[i] = replacemarkup("(\[\[.+?:\{\{.+?\}\}\|\]\])", "", text[i])
			text[i] = remove_braces(text[i])
			
			#remove tables
			text[i] = replacemarkup("\{\|[\d\D]+?\|\}","",text[i])
			text[i] = replacemarkup("----","",text[i]) #horizontal rule
			#lists, indentation, description -> uses symbols -> ignore
			text[i] = replacemarkup("'''''", "",text[i]) #bold and italics
			text[i] = replacemarkup("'''", "",text[i]) #bold 
			text[i] = replacemarkup("''", "",text[i]) #italics
			
			#html spacing symbols
			text[i] = replacemarkup('(&thinsp|&nbsp|&ensp|&emsp)', ' ',text[i]) 
			
			#ignore special caracters
			#ignore ~~~~~ --> unknown
			#ignore [[de:Plankton]] --> unknown
			
			#remove html markups
			#Not use replace markup because could not work
			#No valid word woulde need <> anyway
			text[i] = re.sub("<math[\d\D]*?>[\d\D]+?</math>","",text[i]) 
			text[i] = re.sub("<hiero[\d\D]*?>[\d\D]+?</hiero>","",text[i])
			text[i] = re.sub("<score[\d\D]*?>[\d\D]+?</score>", "", text[i])
			text[i] = re.sub("<code[\d\D]*?>[\d\D]+?</code>", "", text[i])
			text[i] = re.sub("<table[\d\D]*?>[\d\D]+?</table>", "", text[i])
			text[i] = re.sub("<dl[\d\D]*?>[\d\D]+?</dl>", "", text[i])
			text[i] = re.sub("<ol[\d\D]*?>[\d\D]+?</ol>", "", text[i])
			text[i] = re.sub("<ul[\d\D]*?>[\d\D]+?</ul>", "", text[i])
			text[i] = re.sub("<source.*?>[\d\D]+?</source>","",text[i])
			text[i] = re.sub("<imagemap.*?>[\d\D]+?</imagemap>","",text[i])
			
			#references marked as <ref><\ref> and <Ref><\Ref> 
			text[i] = replacemarkup('<ref name( |)=(\w|\!|\$|\%|\&|\(|\)|\*|\,|\-|\.|\:|\;|<|\@|\[|\|\]|\^|\_|\`|\{|\}|\"|\~| )+?/>','<ref></ref>',text[i])
			text[i] = replacemarkup("\.( *?<ref[\d\D]*?>.*?</ref>)+","<ref></ref>. ",text[i]) #refs
			text[i] = re.sub("\.( *?<Ref></Ref>)+","<Ref></Ref>. ",text[i])
			text[i] = replacemarkup("(?!<ref[\d\D]*?>|</ref>|<Ref>|</Ref>)<.*?>","",text[i]) #other html markups
			
			#links w/ hide 
			text[i] = replacemarkup("\[\[.+?:(.+?)\(.+?\)\|\]\]", "\\1", text[i])
			text[i] = replacemarkup("\[\[.+?:(.+?), .+?\|\]\]", "\\1", text[i])
			text[i] = replacemarkup("\[\[.+?:(.+?)\|\]\]", "\\1", text[i])
			text[i] = replacemarkup("\[\[(.+?)\(.+?\)\|\]\]", "\\1", text[i]) 
			text[i] = replacemarkup("\[\[(.+?), .+?\|\]\]", "\\1", text[i])
			text[i] = replacemarkup("\[\[:.+?:(.+?)\]\]", "\\1", text[i])
			text[i] = replacemarkup("\[\[:(.+?)\]\]", "\\1", text[i])
		
			text[i] = replacemarkup("\[\[(\.\./)+?\]\]", "", text[i])
			text[i] = replacemarkup("\[\[/(\w+?)\]\]", "\\1", text[i])
			text[i] = replacemarkup("\[\[(\.\./)+?(\w+?)\]\]", "\\2", text[i])
			
			text[i] = replacemarkup("\[\[File.+?\]\]","",text[i])
 #image links
			
			text[i] = replacemarkup("\[//.+?\]", "", text[i])
			text[i] = replacemarkup("\[\[.+?\|(.+?)\]\]", "\\1", text[i]) #link w/ synonims
			text[i] = replacemarkup("\[\[#(.+?)\]\]", "\\1", text[i]) 
			text[i] = replacemarkup("\[\[(.+?)\]\]", "\\1", text[i]) #link w/ no synonims
			text[i] = replacemarkup("\[\S+?\]", "<Ref><\Ref>", text[i]) #external link w/ noname
			text[i] = replacemarkup("\[\S+? (.+?)\]", "\\1 <Ref><\Ref>", text[i]) #external link
			
			#Remove lists
			text[i] = replacemarkup("(\*+?.+?\n)+","",text[i])
			text[i] = replacemarkup("(\#+?.+?\n)+","",text[i])
			text[i] = replacemarkup("; \S+ : \S+","",text[i])
			text[i] = replacemarkup("\n; \w+?\n(: .+?\n)+","",text[i])
			
	text = ''.join(text)
	#if there is <nowiki> </nowkiki> inside {}
	text = remove_braces(text)
	text = re.sub("<( |)nowiki( |)>|</( |)nowiki( |)>|<( |)nowiki( |)/>|<Nowiki>|</Nowiki>", "",text)
	return text
