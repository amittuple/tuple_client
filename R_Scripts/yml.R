############################################
#
# INSTALL AND LOAD NEEDED PACKAGES
#
############################################

toInstallCandidates <- c("yaml")
# check if pkgs are already present
toInstall <- toInstallCandidates[!toInstallCandidates%in%library()$results[,1]]
if(length(toInstall)!=0)
{install.packages(toInstall, repos = "http://cran.r-project.org")}
# load pkgs
lapply(toInstallCandidates, library, character.only = TRUE)

yml.params <- yaml.load_file('~/tuple_client/R_Scripts/MappingBuffer.yml')
yml.args <- commandArgs(trailingOnly = TRUE)
