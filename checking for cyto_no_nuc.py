#extract list of kegg ids:

cyto_nuc_kegg_list = []
path_to_cyto_kegg = 'cyto_no_nuc_ENSG2KEGG.txt'
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
for entry in cyto_nuc_kegg_list[0:10]:
    print('cyto_nuc:', entry)

#extract list of kegg ids from background 'HPA_ENSG2KEGG_complete'
HPA_background_kegg_list = []
path_to_HPA_kegg = 'HPA_ENSG2KEGG_complete.txt'
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

for entry in HPA_background_kegg_list[0:10]:
    print('background:', entry)

IN_list = []
for entry in cyto_nuc_kegg_list:
    if entry in HPA_background_kegg_list:
        IN_list.append(entry)
print(len(IN_list))
NOTIN_list = []

for entry in cyto_nuc_kegg_list:
    if entry not in HPA_background_kegg_list:
        NOTIN_list.append(entry)
print(len(NOTIN_list))
