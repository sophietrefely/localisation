#process the pathway results to compare cyto_no_nuc, nuc_no_cyto and cyto_nuc transiting proteins.
#From each dataset took the KEGG pathway name and p value from hypergeometric test data in excel

#created text files containing just the pathways copy and pasted for each dataset with newlines between each.

def load_file_as_list_item1(filename):
    file = open(filename)
    line_list = file.read().strip().split('\n')
    path_id_list = []
    for line in line_list:
        entry_list = line.split('\t')
        path_id = entry_list[0]
        percent = entry_list[1]      
        path_id_list.append(path_id)
    return path_id_list

PATH_TO_CYTO = 'cyto_no_nuc_pathways.txt'
PATH_TO_NUC = 'nuc_no_cyto_pathways.txt'
PATH_TO_NUC_CYTO = 'nuc_cyto_pathways.txt'

print(load_file_as_list_item1(PATH_TO_CYTO))
print('============')

cyto_list = load_file_as_list_item1(PATH_TO_CYTO)
nuc_list = load_file_as_list_item1(PATH_TO_NUC)
nuc_cyto_list = load_file_as_list_item1(PATH_TO_NUC_CYTO)

redundant_list = cyto_list + nuc_list + nuc_cyto_list
print(len(redundant_list))
#remove redundancy
complete_list = list(set(redundant_list))
print(len(complete_list))
#sort list
complete_list.sort()
print(complete_list[:5])

#create a dataframe (list of lists) to illustrate all the data as below:
#[[ID1, cyto_p, nuc_p, transit_p], [ID2, cyto_p, nuc_p, transit_p], [ID2, cyto_p, nuc_p, transit_p]…etc ..]

#First load each dataset as a dictionary with key:value = pathway ID: percent
def load_file_as_dict(filename):
    file = open(filename)
    line_list = file.read().strip().split('\n')
    data_dict = {}
    for line in line_list:
        entry_list = line.split('\t')
        path_id = entry_list[0]
        percent = entry_list[1]      
        data_dict[path_id] = percent
    return data_dict

cyto_dict = load_file_as_dict(PATH_TO_CYTO)
nuc_dict = load_file_as_dict(PATH_TO_NUC)
nuc_cyto_dict = load_file_as_dict(PATH_TO_NUC_CYTO)

print(load_file_as_dict(PATH_TO_CYTO))

#go through sorted complete_list and find data from each dataset for each pathway id
PATH_TO_DATA_FRAME = 'dendogram_data_frame.csv'
data_frame = open(PATH_TO_DATA_FRAME, 'w')
headings = ','+'cytoplasm'+','+'nucleus'+','+'nucleus/cytoplasm'+'\n'
data_frame.write(headings)
for path_id in complete_list:
    data_list = []
    data_list.append(path_id)
    if path_id in cyto_dict:
        cyto_percent = cyto_dict[path_id]
        data_list.append(cyto_percent)       
    else:
        cyto_percent = 0
        data_list.append(cyto_percent)
    if path_id in nuc_dict:
        nuc_percent = nuc_dict[path_id]
        data_list.append(nuc_percent)
    else:
        nuc_percent = 0
        data_list.append(nuc_percent)
    if path_id in nuc_cyto_dict:
        nuc_cyto_percent = nuc_cyto_dict[path_id]
        data_list.append(nuc_cyto_percent)
    else:
        nuc_cyto_percent = 0
        data_list.append(nuc_cyto_percent)
    item_to_write = ','.join(map(str, data_list))+'\n'
    data_frame.write(item_to_write)

