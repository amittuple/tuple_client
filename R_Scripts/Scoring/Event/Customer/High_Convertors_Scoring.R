source('~/tuple_client/R_Scripts/Connection.R')
############################################
#
# INSTALL AND LOAD NEEDED PACKAGES
#
############################################
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


## This code needs to be changed and proper logic for birthday and create dates should be included

users$birthday = as.Date(users$bdate)
users$create_date = as.Date(users$cdate)

head(fb)

keycols = c("cust_id")
setkeyv(users, keycols)
setkeyv(fb, keycols)

users.fin.score = merge(users, fb, by="cust_id", all.x=TRUE)

head(users.fin.score)

Sys.Date()

## This code needs to be changed and proper logic for birthday and create dates should be included

users.fin.score$age = round(as.vector((Sys.Date() - users.fin.score$birthday)/365),0)

users.fin.score$join_month = lubridate::month(users.fin.score$create_date)

users.fin.score$birthday = NULL
users.fin.score$create_date = NULL

str(users.fin.score)

users.fin.score$bdate = NULL
users.fin.score$cdate = NULL

users.num = data.table(rep(NA, nrow(users.fin.score)))
users.fac = data.table(rep(NA, nrow(users.fin.score)))

cust_id = users.fin.score$cust_id
users.fin.score = users.fin.score[,-1, with = FALSE]

for (i in 1:(ncol(users.fin.score))) {
  l1.name = names(users.fin.score)[i]
  l1.class = class(users.fin.score[[i]])
  print(l1.name)
  if (!l1.class %in% c('integer', 'numeric', 'matrix')){
    users.fac = cbind(users.fac, users.fin.score[[i]])
    colnames(users.fac)[[ncol(users.fac)]] = l1.name
  } else {
    users.num = cbind(users.num, users.fin.score[[i]])
    colnames(users.num)[[ncol(users.num)]] = l1.name
  }
}

str(users.fac)
str(users.num)

users.fac[,1] = NULL
users.num[,1] = NULL

users.fin.score = cbind(cust_id, users.num, users.fac)

users.fin.score = users.fin.score[,names(users.fin.score) %in% name.for.scores, with = FALSE]

##################  Replacing Nulls with 0  ########################

trim <- function (x) gsub("^\\s+|\\s+$", "", x)

for (i in 2:(ncol(users.fin.score))) {
  l1.name = names(users.fin.score)[i]
  l1.class = class(users.fin.score[[i]])
  print(l1.name)
  if (!l1.class %in% c('integer', 'numeric', 'matrix')){
    users.fin.score[[i]] = trim(users.fin.score[[i]])
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

for (i in 2:(ncol(users.fin.score))) {
  l1.name = names(users.fin.score)[i]
  l1.class = class(users.fin.score[[i]])
  print(l1.name)
  if (!l1.class %in% c('integer', 'numeric', 'matrix')){
    users.fin.score[[i]] = f_rep(users.fin.score[[i]])
  } else {
    users.fin.score[[i]] = f_mean_score(users.fin.score[[i]], users.fin.mean[1,i])
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

for (i in 1:(ncol(users.fin.score))) {
  l1.name = names(users.fin.score)[i]
  l1.class = class(users.fin.score[[i]])
  print(l1.name)
  if (!l1.class %in% c('integer', 'numeric', 'matrix')){
    users.fin.score[[i]] = as.factor(users.fin.score[[i]])
  }
}

for (i in 2:(ncol(users.fin.score))) {
  l1.name = names(users.fin.score)[i]
  l1.class = class(users.fin.score[[i]])
  print(l1.name)
  if (l1.class %in% c('integer', 'numeric', 'matrix')){
    users.fin.score[[i]] = as.numeric(scale(users.fin.score[[i]], scale = TRUE, center = TRUE))
    users.fin.score[[i]] = winsor(users.fin.score[[i]])
  }
}


users.num = data.table(rep(NA, nrow(users.fin.score)))
users.fac = data.table(rep(NA, nrow(users.fin.score)))

cust_id = users.fin.score$cust_id
users.fin.score = users.fin.score[,-1, with = FALSE]

for (i in 1:(ncol(users.fin.score))) {
  l1.name = names(users.fin.score)[i]
  l1.class = class(users.fin.score[[i]])
  print(l1.name)
  if (!l1.class %in% c('integer', 'numeric', 'matrix')){
    users.fac = cbind(users.fac, users.fin.score[[i]])
    colnames(users.fac)[[ncol(users.fac)]] = l1.name
  } else {
    users.num = cbind(users.num, users.fin.score[[i]])
    colnames(users.num)[[ncol(users.num)]] = l1.name
  }
}

str(users.fac)
str(users.num)

users.fac[,1] = NULL
users.num[,1] = NULL


users.fac = acm.disjonctif(users.fac)

users.mod.score = cbind(cust_id, users.num, users.fac)
str(users.mod.score)

rm(fb, users, users.fac, users.num)

users.mod.score = users.mod.score[,names(users.mod.score) %in% mod.for.scores, with = FALSE]

##################################################################

h2o.init(nthreads=-1)

score.model = h2o.loadModel(gbm.mod.path)

users.mod.score = as.h2o(users.mod.score)

score.preds <- h2o.predict(score.model, users.mod.score)

head(score.preds)

users.mod.score = as.data.table(users.mod.score)

users.mod.score$score.pred = as.vector(score.preds[,3])

users.mod.score$High.Conv = as.factor(ifelse(users.mod.score$score.pred <= gbm.thresh, 'Low', 'High'))

h2o.shutdown(prompt = FALSE)

high_conv = users.mod.score[,c('cust_id', 'High.Conv'), with = FALSE]

names(high_conv) = c('cust', 'high_conv')

dbWriteTable(conn, "high_conv", high_conv, overwrite = TRUE, row.names = FALSE)

rm('users.fin.score', 'users.mod.score')
