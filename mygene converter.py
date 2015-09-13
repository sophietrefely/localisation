#using mygene to convert IDs
#must install mygene: >>sudo pip3 install mygene
#also install pandas to use datafram: >>sudo pip3 install pandas
#documentation at http://nbviewer.ipython.org/gist/newgene/6771106

import mygene
mg = mygene.MyGeneInfo()
print(mg.metadata['available_fields']) ## returns available query terms
xli = ['ENSG00000000003', 'ENSG00000000457','ENSG00000000460','ENSG00000001036','ENSG00000001084']
print(mg.querymany(xli, scopes="ensembl.gene", fields="kegg", species= 9606, as_dataframe=True))
