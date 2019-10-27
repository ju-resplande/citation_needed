from treatwikitext import treat_wikitext
name = "case.txt"
f = open(name,"r")
text = f.read()
text = treat_wikitext(text)
f.close()

f = open("out_"+name,"w")
f.write(text)
f.close
