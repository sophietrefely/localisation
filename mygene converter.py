#using mygene to convert IDs
#must install mygene: >>sudo pip3 install mygene
#also install pandas to use datafram: >>sudo pip3 install pandas
#documentation at http://nbviewer.ipython.org/gist/newgene/6771106

import mygene
mg = mygene.MyGeneInfo()
print(mg.metadata['available_fields']) ## returns available query terms
path_to_ENSMBL_file = 'nuc_no_cyto_ENSG_list.csv'
ENSMBL_file = open(path_to_ENSMBL_file)
ENSMBL_list = []
for line in ENSMBL_file:
    line_str = line.replace('\n','') #remove newline
    line_strip = line_str.replace('"', '')
    ENSMBL_list.append(line_strip)
print(ENSMBL_list[:10])
 
xli = ['ENSG00000000003', 'ENSG00000000457',
'ENSG00000000460',
'ENSG00000001036',
'ENSG00000001084']


print(mg.querymany(xli, scopes="ensembl.gene", fields="kegg", species= 9606, as_dataframe=True))
