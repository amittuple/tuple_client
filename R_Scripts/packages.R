############################################
#
# INSTALL AND LOAD NEEDED PACKAGES
#
############################################
zz <- file('~/R_Logs/R_Log.txt', open = "wt")
sink(zz)
sink(zz, type = "message")
toInstallCandidates <- c("data.table", "RPostgreSQL", "yaml", "BTYD", "Matrix", "gsl", "zoo", "magrittr", "dplyr")
# check if pkgs are already present
toInstall <- toInstallCandidates[!toInstallCandidates%in%library()$results[,1]]
if(length(toInstall)!=0)
{install.packages(toInstall, repos = "http://cran.r-project.org")}
# load pkgs
lapply(toInstallCandidates, library, character.only = TRUE)
