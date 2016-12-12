source('~/tuple_client/R_Scripts/utils.R')
source('~/tuple_client/R_Scripts/yml.R')

############################################
#
# INSTALL AND LOAD NEEDED PACKAGES
#
############################################

toInstallCandidates <- c("data.table", "RPostgreSQL")
# check if pkgs are already present
toInstall <- toInstallCandidates[!toInstallCandidates%in%library()$results[,1]]
if(length(toInstall)!=0)
{install.packages(toInstall, repos = "http://cran.r-project.org")}
# load pkgs
lapply(toInstallCandidates, library, character.only = TRUE)


############################################
#
# CONNECTION STRING
#
############################################

drv <- dbDriver("PostgreSQL")

dbname.yaml = yml.params$DATABASE$NAME
host.yaml = yml.params$DATABASE$HOST
port.yaml = yml.params$DATABASE$PORT
user.yaml = yml.params$DATABASE$USER
password.yaml = yml.params$DATABASE$PASSWORD

# # Set up DB connection
conn <- dbConnect(drv, dbname=dbname.yaml, host=host.yaml, port=port.yaml, user=user.yaml, password=password.yaml)

users <- as.data.table(dbGetQuery(conn, 
                  variableSQL(" SELECT * from users ", stringsAsFactors = FALSE)))
