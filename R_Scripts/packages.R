############################################
#
# INSTALL AND LOAD NEEDED PACKAGES
#
############################################

# install gsl library
# install lubridate library
# install h2o library
# install java jre for h2o library
toInstallCandidates <- c("data.table", "RPostgreSQL", "yaml", "BTYD", "Matrix", "gsl", "zoo", "magrittr", "dplyr", "lubridate", "h2o", "pROC", "caret", "ade4", "ROCR", "e1071")
# check if pkgs are already present
toInstall <- toInstallCandidates[!toInstallCandidates%in%library()$results[,1]]
if(length(toInstall)!=0)
{install.packages(toInstall, repos = "http://cran.r-project.org")}
# load pkgs
lapply(toInstallCandidates, library, character.only = TRUE)
