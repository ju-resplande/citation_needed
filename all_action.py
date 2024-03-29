from parser import *
from run_citation_need_model import text_to_word_list, construct_instance_reasons
from keras.models import load_model

URL = "https://en.wikipedia.org/w/api.php"
model = "models/model.h5"
word_dict = "dicts/word_dict.pck"
section_dict = "dicts/section_dict.pck"
table = "output_folder/table.txt"
output ="output_folder/need_citation.txt"

name = raw_input("Insert page name: ")

example = Page(URL,name)
example.generate_page()
example.generate_sections()
example.generate_paragraphs()
example.generate_sentences()
example.generate_table(table)
print table + " generated"

model = load_model(model)
max_seq_length = model.input[0].shape[1].value
X, sections, y, encoder,outstring = construct_instance_reasons(table, section_dict, word_dict, max_seq_length)

pred = model.predict([X, sections])

need_citation = []
prediction = []
min_prediction = 0.9

print "Generating " + output + " with min_pediction = " + str(min_prediction)

for idx, y_pred in enumerate(pred):
	if y_pred[0] > min_prediction and str(y[idx]) == '[1. 0.]':
		need_citation.append(outstring[idx])
		prediction.append(y_pred[0])

need_citation = [x for _, x in sorted(zip(prediction,need_citation), key=lambda pair: pair[0])]
prediction = sorted(prediction)
#descending order
need_citation.reverse() 
prediction.reverse()

with open(output, 'wt') as fout:
	for i,v in enumerate(need_citation):
		fout.write(need_citation[i])
		fout.write("\n")