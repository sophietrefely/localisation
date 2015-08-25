# using the subcellular localisation data from the human protein atlas
# downloaded at http://www.proteinatlas.org/about/download on 20/8/15.
# Want to find proteins that are in the cytoplasm and nucleus

path_to_data = 'subcellular_location.csv'
location_file = open(path_to_data, 'rU') 
#must first convert to a list
location_list = []
for line in location_file:
    # split creates a list out of the line
    # [0] is gene Ensemble gene identifier (ENSG), [1] is main location, [2] is additional location.
    stripped_line = line.rstrip()   # remove the newline from the line, it has one by default
    location_split = stripped_line.split(',') #fields are comma seperated
    location_list.append(location_split)

#everything with main location in cytoplasm or nucleus
main_cyto_list = []
for entry in location_list:
    main = entry[1]
    if 'Cytoplasm' in main:
        main_cyto_list.append(entry)
print('main_cyto_list:', len(main_cyto_list))

main_nuc_list = []
for entry in location_list:
    main = entry[1]
    if 'Nucleus' in main:
        main_nuc_list.append(entry)
print('main_nuc_list:', len(main_nuc_list))

#main in cytoplasm OR nucleus (non-overlapping):
main_cyto_or_nuc_list = []
for entry in main_nuc_list:
    main_cyto_or_nuc_list.append(entry)
for entry in main_cyto_list:
    if entry not in main_cyto_or_nuc_list:
        main_cyto_or_nuc_list.append(entry)
print('main_cyto_or_nuc_list:', len(main_cyto_or_nuc_list))

#main location cytoplasm AND nucleus (overlapping):
main_cyto_and_nuc_list = []
for entry in main_cyto_list:
    main = entry[1]
    if 'Nucleus' in main:
        main_cyto_and_nuc_list.append(entry)
print('main_cyto_and_nuc_list:', len(main_cyto_and_nuc_list))

#test specific gene
for entry in main_nuc_list:
    gene = entry[0]
    if gene =='"ENSG00000170525"':
        print('pfkfb3 in nuclear list') #do this to validate known genes

#everything with main location in cyto an additional location in nucleus
main_cyto_ad_nuc_list = []
for entry in main_cyto_list:
    additional = entry[2]
    if "Nucleus" in additional:
        main_cyto_ad_nuc_list.append(entry)
print('main_cyto_ad_nuc_list:', len(main_cyto_ad_nuc_list))
#everything with main location in nucleus and additional location in cytoplasm
main_nuc_ad_cyto_list = []
for entry in main_nuc_list:
    additional = entry[2]
    if "Cytoplasm" in additional:
        main_nuc_ad_cyto_list.append(entry)
print('main_nuc_ad_cyto_list:', len(main_nuc_ad_cyto_list))
#combine the above 2 lists = nuc_cyto_proteins_list
nuc_cyto_list = []
nuc_cyto_list.extend(main_nuc_ad_cyto_list)
nuc_cyto_list.extend(main_cyto_ad_nuc_list)
print('nuc_cyto_list:', len(nuc_cyto_list))

#First extract the list of ENSG IDs into a .CSV file
path_to_ENSG = 'cyto_nuc_ENSG_list.csv'
ENSG_file = open(path_to_ENSG, 'w') 
for entry in nuc_cyto_list:
    ENSG = entry[0]
    item_to_write = ENSG + '\n'    #unsplits the list
    ENSG_file.write(item_to_write)
ENSG_file.close() #There are 1196 genes
#The Reference list must be the entire list of genes in the human protein atlas
#First must extract the IDs from HPA data:
path_to_HPA = 'HPA_ENSG_complete_list.csv'
HPA_file = open(path_to_HPA, 'w')
for entry in location_list:
    ENSG = entry[0]
    item_to_write = ENSG + '\n'    #unsplits the list
    HPA_file.write(item_to_write)
HPA_file.close()    #There are 8857 genes

#Using KEGG pathways:
#1. convert ENSMBL IDs to KEGG genes using the biodbnet
#http://biodbnet.abcc.ncifcrf.gov/db/db2db.php
#saved files as: cyto_nuc_ENSG2KEGG.txt
#extract list of kegg ids:
cyto_nuc_kegg_list = []
path_to_cyto_kegg = 'cyto_nuc_ENSG2KEGG.txt'
cyto_kegg_file = open(path_to_cyto_kegg, 'rU')
for line in cyto_kegg_file:
    # split creates a list out of the line
    # [0] is gene Ensemble gene identifier (ENSG), [1] is KEGG ID
    stripped_line = line.rstrip()
    split_line = stripped_line.split()
    kegg_id = split_line[1]
    strip_kegg_id = kegg_id.rstrip(';') #strip off the ';' from any with more than 1 kegg ID
    if strip_kegg_id != '-': #remove ENSG not converted to KEGG ids
        cyto_nuc_kegg_list.append(strip_kegg_id)
cyto_nuc_kegg_list = cyto_nuc_kegg_list[1:] #line[0] is header
print('cyto_nuc_kegg_list:', len(cyto_nuc_kegg_list))
#list looks like this:
#['hsa:2729', 'hsa:81887', 'hsa:8379', 'hsa:79007', etc..]

#extract list of kegg ids from background 'HPA_ENSG2KEGG_compete'
HPA_background_kegg_list = []
path_to_HPA_kegg = 'HPA_ENSG2KEGG_compete.txt'
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
print('HPA_background_kegg_list:', len(HPA_background_kegg_list))

#2.find the pathways each gene belongs to using the KEGG API:
#http://rest.kegg.jp/link/pathway/'gene ID eg hsa:10458'
import urllib.request #allows python to access url 
path_to_cyto_nuc_pathway = 'cyto_nuc_kegg_pathways.txt' 
cyto_nuc_pathways = open(path_to_cyto_nuc_pathway, 'w')#write to file

for gene in cyto_nuc_kegg_list[0:6]:
    kegg_gene = str(gene)
    url = "http://rest.kegg.jp/link/pathway/" + kegg_gene
    url_read = urllib.request.urlopen(url).read()   #read url output
    item_to_write = str(url_read, encoding = 'utf8')
    #see http://stackoverflow.com/questions/540342/python-3-0-urllib-parse-error-type-str-doesnt-support-the-buffer-api
    if 'hsa' in item_to_write:#remove empty lines
        cyto_nuc_pathways.write(item_to_write)
cyto_nuc_pathways.close()
#make set of find unique pathways
cyto_nuc_pathway_set = set()
path_to_cyto_nuc_pathway = 'cyto_nuc_kegg_pathways.txt' 
cyto_nuc_pathways = open(path_to_cyto_nuc_pathway, 'rU')
for line in cyto_nuc_pathways:
    # split creates a list out of the line
    # [0] is KEGG gene ID, [1] is KEGG pathway ID
    stripped_line = line.rstrip() #remove '\n'
    split_line = stripped_line.split('\t') #tab separated
    pathway = split_line[1]
    pathway_i = pathway.lstrip('path')#remove prefix to pathway id
    pathway_id = pathway_i.lstrip(':')
    cyto_nuc_pathway_set.add(pathway_id)
print('cyto_nuc_pathway_set:', len(cyto_nuc_pathway_set))

#3.for each path in the cyto_nuc_pathway_set, find genes in the pathway
path_to_pathways = 'cyto_nuc_unique_pathways.txt'
cyto_nuc_unique = open(path_to_pathways, 'w')

for entry in cyto_nuc_pathway_set:
    pathway = str(entry)
    url = "http://togows.dbcls.jp/entry/pathway/"+pathway+"/genes.json"
    url_read = urllib.request.urlopen(url).read()   #read url output
    item_str = str(url_read, encoding = 'utf8')
    item_strip = item_str.lstrip("[\n  {\n").rstrip(" }\n]")
    if 'KO' in item_strip: #get rid of empty pathway entries
        item_to_write = pathway+'\n'+item_strip+'\n'
        cyto_nuc_unique.write(item_to_write)
cyto_nuc_unique.close()
#entries are in file like this:
"""hsa04914   "5241": "PGR; progesterone receptor [KO:K08556]",
    "5295": "PIK3R1; phosphoinositide-3-kinase, regulatory subunit 1 (alpha) [KO:K02649]",
    "23533": "PIK3R5; phosphoinositide-3-kinase, regulatory subunit 5 [KO:K02649]",
    "5296": "PIK3R2; phosphoinositide-3-kinase, regulatory subunit 2 (beta) [KO:K02649]",
    "8503": "PIK3R3; phosphoinositide-3-kinase, regulatory subunit 3 (gamma) [KO:K02649]",
etc"""


#4.for each pathway find amount in HSA_complete_list. Find amount in cyto_nuc_list.
path_to_pathways = 'cyto_nuc_unique_pathways.txt'
cyto_nuc_unique = open(path_to_pathways, 'rU')

for entry in cyto_nuc_unique:
    print(entry)


