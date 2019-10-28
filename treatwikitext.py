import re                     #treat other markups
from aux_treatwikitext import * 

def  treat_wikitext(text):
	text = treat_nowiki(text)
	text = remove_nonlink_brackets(text) 
	#if there is a nowiki in a bracketstructure like that
	#certainly will not be a text 
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
			text[i] = re.sub('<ref name( |)=(\w|\!|\$|\%|\&|\(|\)|\*|\,|\-|\.|\:|\;|<|\@|\[|\|\]|\^|\_|\`|\{|\}|\"|\~| )+?/>','<ref></ref>',text[i])
			text[i] = re.sub("\.( *?<ref[\d\D]*?>.*?</ref>)+","<ref></ref>. ",text[i]) #refs
			text[i] = re.sub("<ref[\d\D]*?>","<ref>",text[i])
			text[i] = re.sub("\.( *?<Ref></Ref>)+","<Ref></Ref>. ",text[i])
			text[i] = re.sub("(?!<ref.*?>|</ref>|<Ref>|</Ref>)<.*?>","",text[i]) #other html markups
			
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
			text[i] = replacemarkup("\[\[Image.+?\]\]","",text[i])
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
	text = re.sub("(\W);","\\1",text) #Erase remaining ;
	text = re.sub(";(.)","\\1",text) #Erase remaining ;

	return text
