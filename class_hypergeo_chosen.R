#hypergeometric test
#from: http://stackoverflow.com/questions/8382806/r-hypergeometric-test-phyper
#phyper(q, m, n, k, lower.tail = TRUE, log.p = FALSE)

#q the number of white balls drawn without replacement from an urn which contains both black and white balls.
#m the number of white balls in the urn.
#n the number of black balls in the urn.
#k the number of balls drawn from the urn.

#============================
#load data file as matrix
#============================
#made a dataframe with pathway and 4 data columns (q,m,n,k) in excel and saved as .csv files for each dataset:

data <- read.csv("nuc_cyto_classes_for_hyper_test.csv")
rnames <- data[,1]                # assign labels in column 1 to "rnames"
nuc_cyto_input_data <- data.matrix(data)  # transform into a matrix
rownames(nuc_cyto_input_data) <- rnames

#============================
#apply phyper to matrix
#============================
#use apply function to iterate over every row in the matrix
#http://stackoverflow.com/questions/4236368/how-to-apply-a-function-to-every-row-of-a-matrix-or-a-data-frame-in-r

p_value = apply(nuc_cyto_input_data, 1, function(x) phyper(x[2], x[3], x[4], x[5], lower.tail=FALSE))
#second argument = 1 to loop over rows, 2 for columns
#lower.tail = FALSE gives probablility of picking this amount or greater by chance. same as 1-p
write.csv(p_value, file = "class_hypergeo_output.csv")

print(nuc_cyto_input_data[1,1])
print(nuc_cyto_input_data[1,2])
print(nuc_cyto_input_data[1,3])
print(nuc_cyto_input_data[1,4])
print(nuc_cyto_input_data[2,1])
print('all')
print(nuc_cyto_input_data)
print(p_value)

