import re                     #treat other markups
from aux_treatwikitext import * 

def  treat_wikitext(text):
	text = treat_nowiki(text)
	text = remove_nonlink_brackets(text) 
	#if there is a nowiki in a bracketstructure like that
	#certainly will not be a text 
	text = re.split("(<( |)nowiki( |)>[\d\D]*?</( |)nowiki( |)>|<Nowiki>[\d\D]*?</Nowiki>)", text)
	
	for i,w in enumerate(text):
		if not re.match("<( |)nowiki( |)>[\d\D]*?</( |)nowiki( |)>|<Nowiki>[\d\D]*?</Nowiki>", text[i]):
			text[i] = replacemarkup("(\[\[.+?:\{\{.+?\}\}\|\]\])", "", text[i])
			text[i] = remove_braces(text[i])

			#ignore lists, indentation, description
			#ignore special caracters
			#ignore ~~~~~ --> unknown
			#ignore [[de:Plankton]] --> unknown

			cases = [
				("\{\|[\d\D]+?\|\}",""), #remove tables
				("----",""), #horizontal rule
				("'''''", ""), #bold and italics
				("'''", ""), #bold 
				("''", ""), #italics
				('(&thinsp|&nbsp|&ensp|&emsp)', ' ') #html spacing symbols
			]

			for markup in cases:
				text[i] = replacemarkup(markup[0], markup[1], text[i])

			#Not use replace markup because could not work
			#No valid word woulde need <> anyway
			html = [
				("<math[\d\D]*?>[\d\D]+?</math>",""),
				("<hiero[\d\D]*?>[\d\D]+?</hiero>",""),
				("<score[\d\D]*?>[\d\D]+?</score>", ""),
				("<code[\d\D]*?>[\d\D]+?</code>", ""),
				("<table[\d\D]*?>[\d\D]+?</table>", ""),
				("<dl[\d\D]*?>[\d\D]+?</dl>", ""),
				("<ol[\d\D]*?>[\d\D]+?</ol>", ""),
				("<ul[\d\D]*?>[\d\D]+?</ul>", ""),
				("<source.*?>[\d\D]+?</source>",""),
				("<imagemap.*?>[\d\D]+?</imagemap>","")
			]

			for markup in html:
				text[i] = re.sub(markup[0], markup[1], text[i])

			ref = [
				('<ref name( |)=(\w|\!|\$|\%|\&|\(|\)|\*|\,|\-|\.|\:|\;|<|\@|\[|\|\]|\^|\_|\`|\{|\}|\"|\~| )+?/>','<ref></ref>'),
				("\.( *?<ref[\d\D]*?>[\d\D]*?</ref>)+","<ref></ref>. "), #change sides for marking as citation
				("\.( *?<Ref></Ref>)+","<Ref></Ref>. "), #{ref | } are transformed into <Ref></Ref>
				("<ref[\d\D]*?>[\d\D]*?</ref>","<ref></ref>"), #stardard for ref (avoid nltk breaking inside sentences)
				("(?!<ref.*?>|</ref>|<Ref>|</Ref>)<.*?>","") #remove other markups
			]
			
			for markup in ref:
				text[i] = re.sub(markup[0], markup[1], text[i])

			links = [
				#links w/ hide
				("\[\[.+?:(.+?)\(.+?\)\|\]\]", "\\1"),
				("\[\[.+?:(.+?), .+?\|\]\]", "\\1"),
				("\[\[.+?:(.+?)\|\]\]", "\\1"),
				("\[\[(.+?)\(.+?\)\|\]\]", "\\1"),
				("\[\[(.+?), .+?\|\]\]", "\\1"),
				("\[\[:.+?:(.+?)\]\]", "\\1"),
				("\[\[:(.+?)\]\]", "\\1"),
				("\[\[(\.\./)+?\]\]", ""),
				("\[\[/(\w+?)\]\]", "\\1"),
				("\[\[(\.\./)+?(\w+?)\]\]", "\\2"),
				#image links
				("\[\[File.+?\]\]",""),
				("\[\[Image.+?\]\]",""),

				("\[//.+?\]", ""),
				("\[\[.+?\|(.+?)\]\]", "\\1"), #link w/ synonims
				("\[\[#(.+?)\]\]", "\\1"),
				("\[\[(.+?)\]\]", "\\1"), #link w/ no synonims
				("\[\S+?\]", "<Ref></Ref>"), #external link w/ noname
				("\[\S+? (.+?)\]", "\\1 <Ref></Ref>"), #external link
			]
			
			for markup in links:
				text[i] = replacemarkup(markup[0], markup[1],text[i])
			
			lists = [
				("(\*+?.+?\n)+",""), #unordered list
				("(\#+?.+?\n)+",""), #ordered list
				("; \S+ : \S+",""), #definition list inline
				("\n; \w+?\n(: .+?\n)+","") #definition list
			]
			
			for markup in lists:
				text[i] = replacemarkup(markup[0], markup[1],text[i])
			
	text = ''.join(text)
	#if there is <nowiki> </nowkiki> inside {}
	text = remove_braces(text)
	text = re.sub("<( |)nowiki( |)>|</( |)nowiki( |)>|<( |)nowiki( |)/>|<Nowiki>|</Nowiki>", "",text)
	text = re.sub("(\W);","\\1",text) #Erase remaining ;
	text = re.sub(";(.)","\\1",text) #Erase remaining ;

	return text
