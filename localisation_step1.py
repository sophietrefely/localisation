# using the subcellular localisation data from the human protein atlas
# downloaded at http://www.proteinatlas.org/about/download on 20/8/15.
# Want to find proteins that are in the cytoplasm and nucleus

#this section produces a .csv file required for step 2
#Produces 2 files:
#'ENSG_list.csv' (the selected subset of genes as ENSMBL IDs)**
#'HPA_ENSG_complete_list.csv' (background ENSML gene IDs all in the HPA data)

#**this is the only one that needs to be converted and changed for step 2.

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

#main location in cytoplasm and not in nucleus:
cyto_no_nuc_list = []
for entry in main_cyto_list:
    if entry not in main_nuc_list and entry not in main_cyto_ad_nuc_list:
        cyto_no_nuc_list.append(entry)
print('cyto_no_nuc_list:', len(cyto_no_nuc_list))

#main location in nucleus and not in cytoplasm:
nuc_no_cyto_list = []
for entry in main_nuc_list:
    if entry not in main_cyto_list and entry not in main_nuc_ad_cyto_list:
        nuc_no_cyto_list.append(entry)
print('nuc_no_cyto_list:', len(nuc_no_cyto_list))

#First extract the list of ENSG IDs into a .CSV file
path_to_ENSG = 'cyto_no_nuc_ENSG_list.csv'
ENSG_file = open(path_to_ENSG, 'w') 
for entry in cyto_no_nuc_list:
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

background_list = []
HPA_open = open(path_to_HPA, 'rU')
for line in HPA_open:
    line_str = line.rstrip('\n')
    background_list.append(line_str)
print(background_list[0:10])

in_list = []
for entry in nuc_no_cyto_list[0:10]:
    ENSG = entry[0]
    if ENSG in background_list:
        in_list.append(entry)
print('in_list:', len(in_list))

NOTIN_list = []
for entry in nuc_no_cyto_list[0:10]:
    ENSG = entry[0]
    if entry not in background_list:
        NOTIN_list.append(entry)
print('NOTIN_list:', len(NOTIN_list))
