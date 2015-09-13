#this step requires the 2 .txt files generated from biodb conversion
#only the subset being analysed as  'xxxx_ENSG2KEGG.txt' needs to be changed at the very top.
#background HPA_ENSG2KEGG_complete.txt remains the same.
#this step produces 3 files:
#cyto_nuc_kegg_pathways.txt
#cyto_nuc_pathway_genes.json
#pathway_analysis.txt

#convert ENSMBL IDs in 'ENSG_list.csv' to KEGG genes using the biodbnet
#http://biodbnet.abcc.ncifcrf.gov/db/db2db.php
#input = ENSMBL gene ID, output = KEGG gene ID
#taxon ID =9606 (human)
#identifier values have comma = NO
#Remove duplicate input values = NO
#Expand taxon ID to include sub species.. = NO
#save files as: 'xxxx_ENSG2KEGG.txt'
##NOTE must put through the HPA complete list in 3 batches because it is >8000 long
#concatenated 3 files on command line as follows:
#cat biodb_first.txt biodb_second.txt biodb_third.txt | sort | uniq | wc
#named concatenated file 'HPA_ENSG2KEGG.txt'

#NOTE remove title headings in excel

#extract list of kegg ids from chosen list:
chosen_kegg_list = []
path_to_chosen = 'cyto_no_nuc_ENSG2KEGG.txt'
chosen_file = open(path_to_chosen, 'rU')
for line in chosen_file:
    # split creates a list out of the line
    # [0] is gene Ensemble gene identifier (ENSG), [1] is KEGG ID
    stripped_line = line.rstrip()
    split_line = stripped_line.split()
    kegg_id = split_line[1]
    first_kegg_id = kegg_id.rstrip(';') #strip off the ';' from any with more than 1 kegg ID
    if first_kegg_id != '-': #remove ENSG not converted to KEGG ids
        chosen_kegg_list.append(first_kegg_id)
print('chosen_kegg_list:', len(chosen_kegg_list), chosen_kegg_list[:5])
#list looks like this:
#['hsa:2729', 'hsa:81887', 'hsa:8379', 'hsa:79007', etc..]

#extract list of kegg ids from background list 'HPA_ENSG2KEGG'
HPA_background_kegg_list = []
path_to_HPA_kegg = 'HPA_ENSG2KEGG.txt'
HPA_kegg_file = open(path_to_HPA_kegg, 'rU')
for line in HPA_kegg_file:
    # split creates a list out of the line
    # [0] is gene Ensemble gene identifier (ENSG), [1] is KEGG ID
    stripped_line = line.rstrip()
    split_line = stripped_line.split()
    kegg_id = split_line[1]
    strip_kegg_id = kegg_id.rstrip(';') #strip off the ';' from any with more than 1 kegg ID
    if strip_kegg_id != '-': #remove ENSG not converted to KEGG ids
        HPA_background_kegg_list.append(strip_kegg_id)
HPA_background_kegg_list = HPA_background_kegg_list[1:] #line[0] is header
print('HPA_background_kegg_list:', len(HPA_background_kegg_list), HPA_background_kegg_list[:5])

#2.find the pathways each gene belongs to using the KEGG API:
#http://rest.kegg.jp/link/pathway/'gene ID eg hsa:10458'
import urllib.request #allows python to access url 
path_to_chosen_kegg_pathways = 'cyto_no_nuc_kegg_pathways.txt' 
chosen_kegg_pathways = open(path_to_chosen_kegg_pathways, 'w')#write to file

for gene in chosen_kegg_list:
    kegg_gene = str(gene)
    url = "http://rest.kegg.jp/link/pathway/" + kegg_gene
    url_read = urllib.request.urlopen(url).read()   #read url output
    item_to_write = str(url_read, encoding = 'utf8')
    #see http://stackoverflow.com/questions/540342/python-3-0-urllib-parse-error-type-str-doesnt-support-the-buffer-api
    if 'hsa' in item_to_write:#remove empty lines
        chosen_kegg_pathways.write(item_to_write)
chosen_kegg_pathways.close()
#make set to be unique pathways
chosen_pathway_set = set()
path_to_chosen_pathways = 'cyto_no_nuc_kegg_pathways.txt' 
chosen_pathways = open(path_to_chosen_pathways, 'rU')
for line in chosen_pathways:
    # split creates a list out of the line
    # [0] is KEGG gene ID, [1] is KEGG pathway ID
    stripped_line = line.rstrip() #remove '\n'
    split_line = stripped_line.split('\t') #tab separated
    pathway = split_line[1]
    pathway_i = pathway.lstrip('path')#remove prefix to pathway id
    pathway_id = pathway_i.lstrip(':')
    chosen_pathway_set.add(pathway_id)
chosen_unique_pathway_list = list(chosen_pathway_set)
print('chosen_pathway_set:', len(chosen_pathway_set))
print('chosen_unique_pathway_list:', len(chosen_unique_pathway_list))

#3.for each pathway in the chosen_unique_pathway_list, find genes in the pathway
#using API query
#make dictionary in json file where: {pathway1: [gene1, gene2], pathway:[gene,gene2,gene3]...}
pathway_gene_dict = {}
import json
with open('chosen_pathways_genes.json', 'w') as outfile:#don't need to file.close() when use with
    for entry in chosen_unique_pathway_list:
        pathway = str(entry)
        url = "http://togows.dbcls.jp/entry/pathway/"+pathway+"/genes.json"
        url_read = urllib.request.urlopen(url).read()   #read url output
        item_str = str(url_read, encoding = 'utf8')
        item_strip = item_str.lstrip("[\n  {\n").rstrip(" }\n]")
        item_list = item_strip.split(',\n')
        #genes are separated by ',\n'
        #entry in list looks like:
        #'    "23533": "PIK3R5; phosphoinositide-3-kinase, regulatory subunit 5 [KO:K02649]"'
        gene_id_list = []
        for entry in item_list:
            entry_list = entry.split(':') #to separate gene id number from description
            gene = entry_list[0]
            gene_str = gene.strip().rstrip('"').lstrip('"') #strip away blank space on rhs and ""
            if len(gene_str) >1: #don't add 'hsa:' to empty entries
                gene_id = 'hsa:'+gene_str #so we will have the right query format for gene id in next step eg 'hsa:23533'
                gene_id_list.append(gene_id)           
            if len(gene_id_list) >=1: #remove empty pathways
                pathway_gene_dict[pathway] = gene_id_list
    dict_as_json = json.dumps(pathway_gene_id_dict) #dumps turns list into a json string
    outfile.write(dict_as_json) 


#4.Analyse each pathway to find % chosen genes/background HSA genes.
path_to_analysis = 'pathway_analysis.txt'
pathway_analysis = open(path_to_analysis, 'w')#write

headers = 'KEGG_Primary_class\tKEGG_secondary_class\tKEGG_pathway_ID\tpathway_name\t# genes in pathway\tgenes in cyto_nuc\t# genes in chosen\tgenes in HSA_background\t#genes in HSA_background\t%(chosen/HSA_background)\n'
pathway_analysis.write(headers)

import json
with open('cyto_nuc_pathways_genes.json') as f:
    pathway_dict = json.load(f) #load (not loads, which is for string) does opposite of dumps
    for pathway_ID in pathway_dict:
        #find pathway name using TOGOWS API
        url = 'http://togows.org/entry/kegg-pathway/'+pathway_ID+'/name.json'
        url_read = urllib.request.urlopen(url).read()   #read url output
        item_str = str(url_read, encoding = 'utf8')
        pathway_name = item_str.lstrip("[\n").rstrip("\n]")
        print(pathway_name)

        #find pathway class using TOGOWS API
        class_url = 'http://togows.org/entry/kegg-pathway/'+pathway_ID+'/classes.json'
        class_url_response = urllib.request.urlopen(class_url).read()   #read url output
        class_url_str = str(class_url_response, encoding = 'utf8') 
        class_json = json.loads(class_url_str) #json looks like: [['Organismal Systems', 'Endocrine system']]
        class_list = class_json[0] #take list within list
        primary_class = class_list[0]
        secondary_class = class_list[1]
        
        genes_list = pathway_dict[pathway_ID]
        pathway_len = len(genes_list)
        pathway_len_str = str(pathway_len)
        print(pathway_ID)
        print(pathway_len)
        #find chosen KEGG genes in this pathway
        genes_in_chosen = []
        for gene in chosen_kegg_list: #entries look like 'hsa:2729'
            if gene in genes_list:
                genes_in_chosen.append(gene)
        chosen_len = len(genes_in_chosen)
        chosen_len_str = str(chosen_len)
        genes_in_chosen_str = str(genes_in_chosen)
        #find background genes in this pathway
        genes_in_background = []
        for gene in HPA_background_kegg_list:
            if gene in genes_list:
                genes_in_background.append(gene)
        background_len = len(genes_in_background)
        background_len_str = str(background_len)
        genes_in_background_str = str(genes_in_background)
        percent = str((chosen_len/background_len)*100)

        item_to_write = primary_class+'\t'+secondary_class+'\t'+pathway_ID+'\t'+pathway_name+'\t'+pathway_len_str+'\t'+genes_in_chosen_str+'\t'+chosen_len_str+'\t'+genes_in_background_str+'\t'+background_len_str+'\t'+percent+'\n'
        pathway_analysis.write(item_to_write)
    pathway_analysis.close()
