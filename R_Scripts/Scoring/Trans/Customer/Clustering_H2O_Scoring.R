source('~/tuple_client/R_Scripts/Connection.R')
############################################
#
# INSTALL AND LOAD NEEDED PACKAGES
#
############################################

print ('Clustering H20 Scoring')

Sys.time()



toInstallCandidates <- c("BTYD", "data.table", "RPostgreSQL", "Matrix", "gsl", "zoo", "dplyr")
# check if pkgs are already present
toInstall <- toInstallCandidates[!toInstallCandidates%in%library()$results[,1]] 
if(length(toInstall)!=0)
{install.packages(toInstall, repos = "http://cran.r-project.org")}
# load pkgs
lapply(toInstallCandidates, library, character.only = TRUE)

################################## 
#
# Reading Data 
#
#################################
customer.table = yml.params$table_map$CUSTOMER_MASTER
fb.table = yml.params$table_map$CUSTOMER_SECONDARY

users <- as.data.table(dbGetQuery(conn, 
                                  variableSQL("SELECT * from $customer.table", customer.table, stringsAsFactors = FALSE)))

fb <- as.data.table(dbGetQuery(conn, 
                               variableSQL("SELECT * from $fb.table", fb.table, stringsAsFactors = FALSE)))


head(users)

colnames(users)[which(colnames(users)== yml.params$column_map$CUSTOMER_MASTER$cust_id)] = 'cust_id'

colnames(fb)[which(colnames(fb)== yml.params$column_map$CUSTOMER_SECONDARY$cust_id)] = 'cust_id'

head(users)
head(fb)

################################## 
#
# Is Factor Conversion
#
#################################

users.factors = yml.params$is_factor$CUSTOMER_MASTER

for (i in 1:(ncol(users))) {
  l1.name = names(users)[i]
  l1.class = class(users[[i]])
  print(l1.name)
  if (l1.name %in% users.factors){
    users[[i]] = as.character(users[[i]])
  } 
}

fb.factors = yml.params$is_factor$CUSTOMER_SECONDARY

for (i in 1:(ncol(fb))) {
  l1.name = names(fb)[i]
  l1.class = class(fb[[i]])
  print(l1.name)
  if (l1.name %in% fb.factors){
    fb[[i]] = as.character(fb[[i]])
  } 
}

head(users)

## This code needs to be changed and proper logic for birthday and create dates should be included

users$birthday = as.Date(users$bdate)
users$create_date = as.Date(users$cdate)

head(fb)

keycols = c("cust_id")
setkeyv(users, keycols)
setkeyv(fb, keycols)

users.cluster.score.fin = merge(users, fb, by="cust_id", all.x=TRUE)

head(users.cluster.score.fin)

users.cluster.score.fin$age = round(as.vector((Sys.Date() - users.cluster.score.fin$birthday)/365),0)

users.cluster.score.fin$birthday = NULL
users.cluster.score.fin$create_date = NULL

str(users.cluster.score.fin)

users.cluster.score.fin$bdate = NULL
users.cluster.score.fin$cdate = NULL

users.cluster.score.fin = users.cluster.score.fin[,names(users.cluster.score.fin) %in% cluster.name.for.scores, with = FALSE]

users.cluster.num.score = data.table(rep(NA, nrow(users.cluster.score.fin)))
users.cluster.fac.score = data.table(rep(NA, nrow(users.cluster.score.fin)))

cust_id = users.cluster.score.fin$cust_id
users.cluster.score.mod = users.cluster.score.fin[,-1, with = FALSE]

for (i in 1:(ncol(users.cluster.score.mod))) {
  l1.name = names(users.cluster.score.mod)[i]
  l1.class = class(users.cluster.score.mod[[i]])
  print(l1.name)
  if (!l1.class %in% c('integer', 'numeric', 'matrix')){
    users.cluster.fac.score = cbind(users.cluster.fac.score, users.cluster.score.mod[[i]])
    colnames(users.cluster.fac.score)[[ncol(users.cluster.fac.score)]] = l1.name
  } else {
    users.cluster.num.score = cbind(users.cluster.num.score, users.cluster.score.mod[[i]])
    colnames(users.cluster.num.score)[[ncol(users.cluster.num.score)]] = l1.name
  }
}

users.cluster.fac.score[,1] = NULL
users.cluster.num.score[,1] = NULL

users.cluster.score.fin = cbind(cust_id, users.cluster.num.score, users.cluster.fac.score)


##################  Replacing Nulls with 0  ########################

trim <- function (x) gsub("^\\s+|\\s+$", "", x)

for (i in 2:(ncol(users.cluster.score.fin))) {
  l1.name = names(users.cluster.score.fin)[i]
  l1.class = class(users.cluster.score.fin[[i]])
  print(l1.name)
  if (!l1.class %in% c('integer', 'numeric', 'matrix')){
    users.cluster.score.fin[[i]] = trim(users.cluster.score.fin[[i]])
  }
}

f_rep <- function(dt) {
  dt[is.na(dt)] <- 0
  return(dt)
}

f_mean_score <- function(dt, dt2) {
  dt[is.na(dt)] <- dt2
  return(dt)
}

for (i in 2:(ncol(users.cluster.score.fin))) {
  l1.name = names(users.cluster.score.fin)[i]
  l1.class = class(users.cluster.score.fin[[i]])
  print(l1.name)
  if (!l1.class %in% c('integer', 'numeric', 'matrix')){
    users.cluster.score.fin[[i]] = f_rep(users.cluster.score.fin[[i]])
  } else {
    users.cluster.score.fin[[i]] = f_mean_score(users.cluster.score.fin[[i]], users.cluster.fin.mean[1,i])
  }
}

winsor = function (x, fraction=.01)
{
  if(length(fraction) != 1 || fraction < 0 ||
     fraction > 0.5) {
    stop("bad value for 'fraction'")
  }
  lim <- quantile(x, probs=c(fraction, 1-fraction))
  x[ x < lim[1] ] <- lim[1]
  x[ x > lim[2] ] <- lim[2]
  x
}

for (i in 2:(ncol(users.cluster.score.fin))) {
  l1.name = names(users.cluster.score.fin)[i]
  l1.class = class(users.cluster.score.fin[[i]])
  print(l1.name)
  if (l1.class %in% c('integer', 'numeric', 'matrix')){
    users.cluster.score.fin[[i]] = as.numeric(scale(users.cluster.score.fin[[i]], scale = TRUE, center = TRUE))
    users.cluster.score.fin[[i]] = winsor(users.cluster.score.fin[[i]])
  }
}


for (i in 2:(ncol(users.cluster.score.fin))) {
  l1.name = names(users.cluster.score.fin)[i]
  l1.class = class(users.cluster.score.fin[[i]])
  print(l1.name)
  if (!l1.class %in% c('integer', 'numeric', 'matrix')){
    users.cluster.score.fin[[i]] = as.factor(users.cluster.score.fin[[i]])
  }
}

users.cluster.score.mod = users.cluster.score.fin[,names(users.cluster.score.fin) %in% cluster.mod.for.scores, with = FALSE]

################  H2O  #########################################

h2o.init(nthreads=-1)

final.clust = h2o.loadModel(cluster.mod.path)

users.cluster.score.mod = as.h2o(users.cluster.score.mod)

users.cluster.score.mod$cluster = h2o.predict(final.clust, users.cluster.score.mod)

head(users.cluster.score.mod)

profile_clusters = as.data.frame(users.cluster.score.mod[,c('cust_id', 'cluster')])

h2o.shutdown(prompt = FALSE)

dbWriteTable(conn, "profile_clusters", profile_clusters, overwrite = TRUE, row.names = FALSE)

rm(list = c(fb', 'profile_clusters', 'users.cluster.fac.score', 'users.cluster.num.score', 'users.cluster.score.fin'))
