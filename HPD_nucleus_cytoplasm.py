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


#use REACTOME for enrichment analysis:
#http://www.reactome.org/PathwayBrowser
#entered 'cyto_nuc_ENSG_list' IDs
#reactome returned 3 files:
#'cyto_nuc_results.csv' - the overrepesentation pathway analysis
#'cyto_nuc_mapping.csv' - the mapping of ENSBL to uniprot ID
#'cyto_nuc_not_found.csv' - 714 IDs not found! (out of 1196! = no good)
#NOTE: there is no place to enter the background
#the background is all genes in HPA 'subcellular_location.csv'
#there is no way to enter the background for this analysis
#therefore useless!

#Using KEGG pathways:
#1. converted ENSMBL IDs to KEGG genes using the biodbnet
#http://biodbnet.abcc.ncifcrf.gov/db/db2db.php
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
print(cyto_nuc_kegg_list[0:9])
cyto_nuc_kegg_list = cyto_nuc_kegg_list[1:] #line[0] is header
print(cyto_nuc_kegg_list[0:9])
print('cyto_nuc_kegg_list:', len(cyto_nuc_kegg_list))



    
#2.find the pathways each gene belongs to using the KEGG API:
#http://rest.kegg.jp/link/pathway/'gene ID eg hsa:10458'
#add path:'hsa04520', hsa04810' to the entry
#for each path in the cyto nuc list, find total number of entries
#find amount in HSA_complete list. Find amount in cyto_nuc_list.





