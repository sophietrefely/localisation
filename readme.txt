Localisation Project:

AIM: To find pathways enriched in proteins that are localised to both the cytoplasm and the nucleus.
1. Used the subcellular localisation data from the human protein atlas downloaded at:
http://www.proteinatlas.org/about/download on 20/8/15.
Data includes the main and additional location of each protein.
Filtered the list of proteins to find proteins that are localised in the cytoplasm and nucleus.
Summary:
main location cytoplasm: 2572 genes
main location nucleus: 4331
main location cytoplasm or nucleus: 6297
main location in cytoplasm and nucleus: 606
*main location cytoplasm, additional location nucleus (transiting proteins?): 275
*main location nucleus, additional location cytoplasm (transiting proteins?): 922
**cytoplasmic_nuclear (combination of *): 1197
**main location cytoplasmic with no main or additional  location in nucleus (cyto_no_nuc_list: 1691)
**main location in nucleus with no main or additional location in cytoplasm (nuc_no_cyto_list: 2803)

Background_list (complete list of proteins in the HPA data is the ‘background' gene set): 8857 genes

2. Converted ENSBL gene IDs from step 1 to KEGG IDs using the biodbnet at:
http://biodbnet.abcc.ncifcrf.gov/db/db2db.php
There were some genes not converted:
cytoplasmic_nuclear: KEGG IDs = 1179 (18 not found from 1197 ENSMBL IDs)
background: KEGG IDs =  4466 (? not found from 8857 ENSMBL IDs)

3. Mapped cytoplasmic_nuclear genes to pathways using the KEGG API:
url = "http://rest.kegg.jp/link/pathway/" + kegg_geneID
Made a list of unique pathways (i.e. remove duplicates) = 244 pathways

4. Used the TOGOWS (http://togows.dbcls.jp) API that links to KEGG to obtain the genes in each pathway.
reference:
Toshiaki Katayama, Mitsuteru Nakao and Toshihisa Takagi: TogoWS: integrated SOAP and REST APIs for interoperable bioinformatics Web services.Nucleic Acids Research 2010, 38:W706-W711. doi:10.1093/nar/gkq386, PMID:20472643 (NAR Web Server Issue 2010)

5.For each pathway found the #cytoplasmic_nuclear proteins/#background proteins as %.

6. Used TOGOWS API to get pathway name from pathway_ID list:
http://togows.org/entry/kegg-pathway/'pathway_ID'/name.json

7. Assigned pathways to Class using TOGOWS API:
http://togows.org/entry/kegg-pathway/'pathway_ID'/classes.json
Returns primary class:
Metabolism, Genetic Information Processing, Environmental Information Processing, Cellular Processing, Organismal Systems, Human Diseases, Drug Development
And secondary class.

>>>>>>>>>>>>>
Repeat analysis on proteins with main location in nucleus no additional in cyto and main location in cytoplasm no additional in nucleus (i.e.
**main location cytoplasmic with no main or additional  location in nucleus (cyto_no_nuc_list: 1691).
>>>>>>>>>>>>>

- total number of proteins in the dataset (cyto_no_nuc: 1675 , nuc_no_cyto: 2768  , nuc_cyto: 792 )

Hypergeometric test in R:
To assign a p-value for the probability of finding a certain number of genes belonging to a pathway in the dataset, taking into account the background.
Code is in “Hypergeometric_test.R".
Input is the number of genes in chosen list, number of genes in background list for each pathway + total number of genes in background and chosen.
Output is p-value. (<0.05 is significant).
Ranked all pathways according to p value in excel tab “analysis by p-value”:
highlighted significant (p<0.05) pathways:
     - cyto_no_nuc: 82 sig pathways
     - nuc_no_cyto: 30 sig pathways
     - nuc_cyto: 15 sig pathways
Hypergeometric analysis of pathways classes:
Counted total pathways in each class in HPA background in python file “class_analysis_HPA_background.py"
Counted total pathways in each chosen data set, separately, for significant and non-significant pathway lists using excel.
Class hypergeometric test was performed for each data set in “class_hypergeo_chosen.py"

determined q, m, n and k:
q = the number of white balls drawn without replacement from an urn containing both black and white balls.
= significant pathways for each class in chosen list (e.g. cyto_no_nuc)

m = number of white balls in the urn
= total number of HPA background pathways in each class (data generated from ‘class_analysis_HPA_background.py')

n = number of black balls in the urn
=  total number of pathways not in class (number of pathways in HPA background list - q)

k = number of balls drawn from the urn
=  number of pathways in chosen list (cyto_no_nuc = , nuc_cyto = 201, nuc_no_cyto =  )

OR
determined q, m, n and k:
q = the number of white balls drawn without replacement from an urn containing both black and white balls.
= number of significant pathways in each class in chosen list (e.g. cyto_no_nuc pathway list)

m = number of white balls in the urn
= total number of pathways in each class in the chosen list (e.g. cyto_no_nuc pathway list), significant and non-significant.

n = number of black balls in the urn
=  number of pathways not in class (number of pathways in HPA background list - q)

k = number of balls drawn from the urn
=  number of pathways in chosen list (cyto_no_nuc = , nuc_cyto = 201, nuc_no_cyto =  )

Hierarchical clustering:
To compare relatedness of the transiting proteins to nuclear and cytoplasmic proteins.

11. Data preparation in Python:
- From each dataset took the KEGG pathway name and p-value calculated from 'Hypergeometric_test.R'.
- Created a complete list of pathways represented in these 3 lists in python file ‘processing for dendogram.py':
     - combined all 3 KEGG pathway lists into 1 redundant list
     - turned this into a set
     - turned set into a list and ordered = complete pathways list
- created a list of lists to illustrate all the data as below:
     - [[ID1, nuc_%, cyto_%, transit_%], [ID2, nuc_%, cyto_%, transit_%], [ID2, nuc_%, cyto_%, transit_%]…etc ..]
     - print list to file with ‘\n’ between each line

12. hierarchical clustering in R:
Using guide at http://sebastianraschka.com/Articles/heatmaps_in_r.html