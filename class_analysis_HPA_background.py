#AIM: to find number of genes in each primary and secondary class of pathways in the HPA background list

# NOTE(peter) this caches requests made with the 'requests' library in a local database
import requests
import requests_cache

requests_cache.install_cache('stored_geneid_requests')

#extract list of kegg gene ids from 'HPA_ENSG2KEGG'

path_to_HPA_kegg_ids = 'HPA_kegg_ids.txt'
HPA_kegg_ids = open(path_to_HPA_kegg_ids, 'w')#write to file

HPA_kegg_list = []
path_to_HPA_kegg = 'HPA_ENSG2KEGG.txt'
HPA_kegg_file = open(path_to_HPA_kegg, 'rU')#read file
for line in HPA_kegg_file:
    # split creates a list out of the line
    # [0] is gene Ensemble gene identifier (ENSG), [1] is KEGG ID
    stripped_line = line.rstrip()
    split_line = stripped_line.split()
    kegg_id = split_line[1]
    strip_kegg_id = kegg_id.rstrip(';') #strip off the ';' from any with more than 1 kegg ID
    if strip_kegg_id != '-': #remove ENSG not converted to KEGG ids
        HPA_kegg_list.append(strip_kegg_id)
HPA_kegg_list = HPA_kegg_list[1:] #line[0] is header
for item in HPA_kegg_list[1:]:
    item_to_write = item+'\n'
    HPA_kegg_ids.write(item_to_write)
HPA_kegg_ids.close()

#create list of pathways in HPA background
#using the KEGG API to find the pathways each gene belongs to:
#http://rest.kegg.jp/link/pathway/'gene ID eg hsa:10458'
#remove duplicates -> create HPA_unique_pathway_list

import urllib.request #allows python to access url 
path_to_HPA_kegg_pathways = 'HPA_kegg_pathways.txt' 
HPA_kegg_pathways = open(path_to_HPA_kegg_pathways, 'w')#write to file

for gene in HPA_kegg_list:
    kegg_gene = str(gene)
    url = "http://rest.kegg.jp/link/pathway/" + kegg_gene
    url_read = requests.get(url)   #read url output
    item_to_write = url_read.text
    #see http://stackoverflow.com/questions/540342/python-3-0-urllib-parse-error-type-str-doesnt-support-the-buffer-api
    if 'hsa' in item_to_write:#remove empty lines
        HPA_kegg_pathways.write(item_to_write)
HPA_kegg_pathways.close()

#make set to be unique pathways
HPA_pathway_set = set()
path_to_HPA_pathways = 'HPA_kegg_pathways.txt' 
HPA_pathways = open(path_to_HPA_pathways, 'rU')
for line in HPA_pathways:
    # split creates a list out of the line
    # [0] is KEGG gene ID, [1] is KEGG pathway ID
    stripped_line = line.rstrip() #remove '\n'
    split_line = stripped_line.split('\t') #tab separated
    pathway = split_line[1]
    pathway_i = pathway.lstrip('path')#remove prefix to pathway id
    pathway_id = pathway_i.lstrip(':')
    HPA_pathway_set.add(pathway_id)
HPA_unique_pathway_list = list(HPA_pathway_set)
print('HPA_pathway_set:', len(HPA_pathway_set))
print('HPA_unique_pathway_list:', len(HPA_unique_pathway_list))


#for each pathway in the HPA_unique_pathway_list, find the number of genes in pathway
#using API query
#make dictionary in json file where: {pathway1: [gene1, gene2], pathway:[gene,gene2,gene3]...}

pathway_gene_dict = {}
import json
with open('HPA_pathways_genes.json', 'w') as outfile:#don't need to file.close() when use with
    for entry in HPA_unique_pathway_list:
        pathway = str(entry)
        url = "http://togows.dbcls.jp/entry/pathway/"+pathway+"/genes.json"
        url_read = requests.get(url)  #read url output
        item_str = url_read.text
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
    dict_as_json = json.dumps(pathway_gene_dict) #dumps turns list into a json string
    outfile.write(dict_as_json)

#find number of HPA background list pathways in primary and secondary class
#first create file with columns: KEGG_Primary_class, KEGG_secondary_class, pathway
path_to_analysis = 'class_analysis.txt'
pathway_analysis = open(path_to_analysis, 'w')#write

import json
with open('HPA_pathways_genes.json') as f:
    pathway_dict = json.load(f) #load (not loads, which is for string) does opposite of dumps
    for pathway_ID in pathway_gene_dict:
        #find pathway class using TOGOWS API
        class_url = 'http://togows.org/entry/kegg-pathway/'+pathway_ID+'/classes.json'
        class_url_response = requests.get(class_url)  #read url output
        class_url_str = class_url_response.text 
        class_json = json.loads(class_url_str) #json looks like: [['Organismal Systems', 'Endocrine system']]
        class_list = class_json[0] #take list within list
        primary_class = class_list[0]
        secondary_class = class_list[1]
        genes = pathway_gene_dict[pathway_ID]
        len_genes = str(len(genes))
        item_to_write = primary_class+'\t'+secondary_class+'\t'+pathway_ID+'\n'
        pathway_analysis.write(item_to_write)
    pathway_analysis.close()

#second, add up all the primary class pathways
pathway_analysis_read = open(path_to_analysis, 'rU')

#make cumulative dictionary; {class1:gene_number, etc}
primary_dict = {}
secondary_dict = {}
for line in pathway_analysis_read:
    stripped_line = line.rstrip()
    split_line = stripped_line.split('\t')
    primary_class = split_line[0]
    secondary_class = split_line[1]
    primary_dict[primary_class] = primary_dict.get(primary_class, 0) + 1
    secondary_dict[secondary_class] = secondary_dict.get(secondary_class, 0) + 1
print('Primary class:')
for entry in primary_dict:
    print(entry+'\t'+str(primary_dict[entry]))
print('Secondary class:')
for entry in secondary_dict:
    print(entry+'\t'+str(secondary_dict[entry]))

#make dictionaries for other data sets in 'class_analysis_chosen.py'     
