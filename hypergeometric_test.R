#hypergeometric test
#from: http://stackoverflow.com/questions/8382806/r-hypergeometric-test-phyper
#phyper(q, m, n, k, lower.tail = TRUE, log.p = FALSE)

#q vector of quantiles representing the number of white balls drawn
#without replacement from an urn which contains both black and white
#balls.
#m the number of white balls in the urn.
#n the number of black balls in the urn.
#k the number of balls drawn from the urn.

#for my data:
#q = # of genes from chosen list (eg nuc_cyto) in pathway.
#m = # of genes in HPA background in pathway
#n = total # of genes assigned to kegg IDs in HPA background not in pathway (ie 8745-m)
#k = total # of genes assigned to kegg IDs in chosen list (cyto_no_nuc: 1675 , nuc_no_cyto: 2768  , nuc_cyto: 792)

#============================
  #load data file as matrix
#============================
#made a dataframe with pathway and 2 data columns (q,m) in excel and saved as .csv:

data <- read.csv("hypergeo_nuc_cyto_input.csv", comment.char="#")
rnames <- data[,1]                # assign labels in column 1 to "rnames"
input_data <- data.matrix(data)  # transform column 2-> into a matrix
rownames(input_data) <- rnames

#============================
  #apply phyper to matrix
#============================
#use apply function to iterate over every row in the matrix
#http://stackoverflow.com/questions/4236368/how-to-apply-a-function-to-every-row-of-a-matrix-or-a-data-frame-in-r

p_value = apply(input_data, 1, function(x) phyper(x[1], x[2], (8745-x[2]), 792)) #second argument = 1 to loop over rows, 2 for columns

phyper(input_data[1,1], input_data[1,2], (8745-input_data[1,2]), 792)

write.csv(p_value, file = "hypergeo_nuc_cyto_output.csv")