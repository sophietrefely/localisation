Localisation Project:

AIM: To find pathways enriched in proteins that are localised to both the cytoplasm and the nucleus. 
1. Used the subcellular localisation data from the human protein atlas downloaded at: 
http://www.proteinatlas.org/about/download on 20/8/15. 
Data includes the main and additional location of each protein. 
Filtered the list of proteins to find proteins that are localised in the cytoplasm and nucleus. 
Summary: 
main location cytoplasm: 2572 genes 
main location nucleus: 4331 
main location cytoplasm or nucleus: 6297 
main location in cytoplasm and nucleus: 606  
*main location cytoplasm, additional location nucleus (transiting proteins?): 275 
*main location nucleus, additional location cytoplasm (transiting proteins?): 922 
**cytoplasmic_nuclear (combination of *): 1197 
**main location cytoplasmic with no main or additional  location in nucleus (cyto_no_nuc_list: 1691)
**main location in nucleus with no main or additional location in cytoplasm (nuc_no_cyto_list: 2803)

Background_list (complete list of proteins in the HPA data is the ‘background' gene set): 8857 genes 

2. Converted ENSBL gene IDs from step 1 to KEGG IDs using the biodbnet at: 
http://biodbnet.abcc.ncifcrf.gov/db/db2db.php
There were some genes not converted: 
cytoplasmic_nuclear: KEGG IDs = 1179 (18 not found from 1197 ENSMBL IDs) 
background: KEGG IDs =  4466 (? not found from 8857 ENSMBL IDs) 
  
3. Mapped cytoplasmic_nuclear genes to pathways using the KEGG API: 
url = "http://rest.kegg.jp/link/pathway/" + kegg_geneID 
Made a list of unique pathways (i.e. remove duplicates) = 244 pathways 

4. Used the TOGOWS (http://togows.dbcls.jp) API that links to KEGG to obtain the genes in each pathway. 
reference: 
Toshiaki Katayama, Mitsuteru Nakao and Toshihisa Takagi: TogoWS: integrated SOAP and REST APIs for interoperable bioinformatics Web services.Nucleic Acids Research 2010, 38:W706-W711. doi:10.1093/nar/gkq386, PMID:20472643 (NAR Web Server Issue 2010)

5. For each pathway found the #cytoplasmic_nuclear proteins/#background proteins as %. 

6. Used TOGOWS API to get pathway name from pathway_ID list: 
http://togows.org/entry/kegg-pathway/'pathway_ID'/name.json

7. Assigned pathways to Class using TOGOWS API: 
http://togows.org/entry/kegg-pathway/'pathway_ID'/classes.json
Returns primary class: 
Metabolism, Genetic Information Processing, Environmental Information Processing, Cellular Processing, Organismal Systems, Human Diseases, Drug Development 
And secondary class. 

8. Ranked pathways according to % in excel 
9. Coloured according to class and counted amount in each class in excel 

>>Repeated analysis on proteins with main location in nucleus not in cyto and main location in cytoplasm not in nun and compared class/pathway results. 
-% of pathways belonging to Class = Metabolism for each data set 
