import mwparserfromhell       #treats braces    
import re                     #treat other markups

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
                result += " & " +  template.get(2).value.encode("utf-8")
            elif len(template.params) == 6:
                result += ", " +  template.get(2).value.encode("utf-8")  + " & " +  template.get(3).value.encode("utf-8")
            elif  len(template.params) > 6:
                result += " et al."
            result += " " + "<Ref></Ref>"
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
                    result += item.encode("utf-8") + " "
            text = text.replace(template.encode('utf-8'), result)
        elif template.name.matches("lang") | \
            template.name.matches("align") | \
            template.name.matches("Verse translation") | \
            template.name.matches("script"):
                text = text.replace(template.encode('utf-8'), template.get(2).value.encode('utf-8'))
        elif (template.name.matches("Hanging indent") |
        template.name.matches("block indent") |
        template.name.matches("font") |
        template.name.matches("Nowrap") |
        template.name.matches("strong") |
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
        template.name.matches("awrap") |
        template.name.matches("strikethrough") |
        template.name.matches("Strike") |
        template.name.matches("S") |
        template.name.matches("Strikethrough color") |
        template.name.matches("highlight") | 
        template.name.matches("highlight round") |
        template.name.matches("abbr") | 
        template.name.matches("subst:poem") |
        template.name.matches("small") | 
        template.name.matches("smaller") | 
        template.name.matches("larger") | 
        template.name.matches("bigger") | 
        template.name.matches("big") | 
        template.name.matches("huge") | 
        template.name.matches("samp") |
        template.name.matches("Pre") |
        bool(re.search("(!|)(b|m|)xt(d|n)",template.name.encode('utf-8')))):
            if template.has("text"):
                text = text.replace(template.encode('utf-8'), template.get("text").value.encode('utf-8'))
            else:
                text = text.replace(template.encode('utf-8'), template.get(1).value.encode('utf-8'))
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
                        result += ", "
                    result += param[i+1].encode('utf-8')
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
                result += item.encode('utf-8')
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
        elif template.name.matches("gaps"):
            result = ""
            for item in template.params:
                result += item.encode('utf-8') + " "
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
#If there is [[ ]] inside [[]] then that is not only a link
def remove_nonlink_brackets(text):
    _open = 0 #how many open brackets [[ 
    _close = 0 #how many close brackets ]]
    _open_index = 0 #when the sequence started
    j = 0
    while j < len(text)-1:
        new_length = len(text) #update length
        if j >= new_length-1:
            break

        if text[j] == "[" and text[j+1] == "[": 
            if _open == 0:
                _open_index = j
            _open = _open+1
            j=j+1
        elif text[j] == "]" and text[j+1] == "]":
            _close = _close+1
            if _open == _close:
                if _open > 1: #if not only a link
                    erase = text[_open_index:j+2]
                    text = text.replace(erase,"")
                    j = _open_index
                _open = 0
                _close = 0
                _open_index = 0
            j = j+1
        j = j+1
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