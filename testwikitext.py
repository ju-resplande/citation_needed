from treatwikitext import treat_wikitext
f = open("test markups.txt","r")
text = f.read()
text = treat_wikitext(text)
print text
