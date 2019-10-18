import pandas as pd
out_dir = 'output_folder'
prevision = out_dir + '/' + 'en' + '_predictions_sections.tsv'

statements = pd.read_csv(prevision, sep='\t', index_col=None, error_bad_lines=False, warn_bad_lines=False)

need_citation = []
prediction = []
min_prediction = 0.9

for i in range(len(statements['Citation'])):
	if statements['Citation'][i] == '[1. 0.]' and statements['Prediction'][i]  > min_prediction:
		need_citation.append(statements['Text'][i])
		prediction.append(statements['Prediction'][i])

need_citation = [x for _,x in sorted(zip(prediction, need_citation))]
need_citation.reverse()

for statement in need_citation:
	print statement
