print('Event Clustering')
print(Sys.time())

################################## 
#
# Reading Data 
#
#################################
event.table = yml.params$table_map$EVENT_LOG
trans.table = yml.params$table_map$TRANSACTION_MASTER
customer.table = yml.params$table_map$CUSTOMER_MASTER
fb.table = yml.params$table_map$CUSTOMER_SECONDARY

event <- as.data.table(dbGetQuery(conn, 
                                  variableSQL("SELECT * from $event.table", event.table, stringsAsFactors = FALSE)))

trans <- as.data.table(dbGetQuery(conn, 
                                  variableSQL("SELECT * from $trans.table", trans.table, stringsAsFactors = FALSE)))

users <- as.data.table(dbGetQuery(conn, 
                                  variableSQL("SELECT * from $customer.table", customer.table, stringsAsFactors = FALSE)))

fb <- as.data.table(dbGetQuery(conn, 
                               variableSQL("SELECT * from $fb.table", fb.table, stringsAsFactors = FALSE)))


print(head(event))
print(head(trans))
print(head(users))

colnames(event)[which(colnames(event)== yml.params$column_map$EVENT_LOG$cust_id)] = 'cust_id'
colnames(event)[which(colnames(event)== yml.params$column_map$EVENT_LOG$action_type)] = 'action_type'
colnames(event)[which(colnames(event)== yml.params$column_map$EVENT_LOG$prod_id)] = 'prod_id'
colnames(event)[which(colnames(event)== yml.params$column_map$EVENT_LOG$timestamp)] = 'timestamp'

colnames(trans)[which(colnames(trans)== yml.params$column_map$TRANSACTION_MASTER$cust_id)] = 'cust_id'
colnames(trans)[which(colnames(trans)== yml.params$column_map$TRANSACTION_MASTER$revenue)] = 'revenue'
colnames(trans)[which(colnames(trans)== yml.params$column_map$TRANSACTION_MASTER$prod_id)] = 'prod_id'
colnames(trans)[which(colnames(trans)== yml.params$column_map$TRANSACTION_MASTER$timestamp)] = 'timestamp'

colnames(users)[which(colnames(users)== yml.params$column_map$CUSTOMER_MASTER$cust_id)] = 'cust_id'

colnames(fb)[which(colnames(fb)== yml.params$column_map$CUSTOMER_SECONDARY$cust_id)] = 'cust_id'

print(head(event))
print(head(trans))
print(head(users))
print(head(fb))

########################################
#
# Taking subset of active customers
#
#######################################

trans.load = event[,names(event) %in% c('cust_id'), with = FALSE]
trans.load = unique(trans.load[,c('cust_id'), with = FALSE])

print(head(trans.load))

names(trans.load) = c('cust')

trans.merge = unique(trans[,c('cust_id'), with = FALSE])
names(trans.merge) = c('cust')
trans.merge$cust = as.integer(trans.merge$cust)

trans.load = rbind(trans.load, trans.merge)

users = subset(users, cust_id %in% (unique(trans.load$cust)))

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

data.row = nrow(users)

cust_id = users$cust_id

users = Filter(function(x) length(unique(x))*100/data.row < 99, users)

users = cbind(cust_id, users)

print(head(users))

## This code needs to be changed and proper logic for birthday and create dates should be included

users$birthday = as.Date(users$bdate)
users$create_date = as.Date(users$cdate)

print(head(fb))

keycols = c("cust_id")
setkeyv(users, keycols)
setkeyv(fb, keycols)

users.cluster.fin = merge(users, fb, by="cust_id", all.x=TRUE)

print(head(users.cluster.fin))

Sys.Date()

## This code needs to be changed and proper logic for birthday and create dates should be included

users.cluster.fin$age = round(as.vector((Sys.Date() - users.cluster.fin$birthday)/365),0)

users.cluster.fin$birthday = NULL
users.cluster.fin$create_date = NULL

trans$cust_id = as.integer(trans$cust_id)

print(head(trans))

trans$convert = 1

trans.dup = trans %>%
  group_by(cust_id) %>%
  summarize(convert = max(convert), revenue = sum(revenue))

print(head(trans.dup))

colnames(trans.dup) = c('cust_id', 'convert', 'revenue')

trans.dup = data.table(trans.dup)

keycols = c("cust_id")
setkeyv(users.cluster.fin, keycols)
setkeyv(trans.dup, keycols)

users.cluster.fin = merge(users.cluster.fin, trans.dup, by="cust_id", all.x=TRUE)

print(head(users.cluster.fin))

str(users.cluster.fin)

users.cluster.fin$bdate = NULL
users.cluster.fin$cdate = NULL

users.cluster.fin.num = data.table(rep(NA, nrow(users.cluster.fin)))
users.cluster.fin.fac = data.table(rep(NA, nrow(users.cluster.fin)))

cust_id = users.cluster.fin$cust_id
convert = users.cluster.fin$convert
revenue = users.cluster.fin$revenue
users.cluster.fin = users.cluster.fin[,-c(1, ncol(users.cluster.fin)-1, ncol(users.cluster.fin)), with = FALSE]

for (i in 1:(ncol(users.cluster.fin))) {
  l1.name = names(users.cluster.fin)[i]
  l1.class = class(users.cluster.fin[[i]])
  print(l1.name)
  if (!l1.class %in% c('integer', 'numeric', 'matrix')){
    users.cluster.fin.fac = cbind(users.cluster.fin.fac, users.cluster.fin[[i]])
    colnames(users.cluster.fin.fac)[[ncol(users.cluster.fin.fac)]] = l1.name
  } else {
    users.cluster.fin.num = cbind(users.cluster.fin.num, users.cluster.fin[[i]])
    colnames(users.cluster.fin.num)[[ncol(users.cluster.fin.num)]] = l1.name
  }
}

str(users.cluster.fin.fac)
str(users.cluster.fin.num)

users.cluster.fin.fac[,1] = NULL
users.cluster.fin.num[,1] = NULL

users.cluster.fin.fac = Filter(function(x) length(unique(x)) <= 100, users.cluster.fin.fac)
users.cluster.fin.fac = Filter(function(x) length(unique(x))*100/data.row < 5, users.cluster.fin.fac)

users.cluster.fin = cbind(cust_id, users.cluster.fin.num, users.cluster.fin.fac, convert, revenue)

##################  Replacing Nulls with 0  ########################

trim <- function (x) gsub("^\\s+|\\s+$", "", x)

for (i in 2:(ncol(users.cluster.fin)-2)) {
  l1.name = names(users.cluster.fin)[i]
  l1.class = class(users.cluster.fin[[i]])
  print(l1.name)
  if (!l1.class %in% c('integer', 'numeric', 'matrix')){
    users.cluster.fin[[i]] = trim(users.cluster.fin[[i]])
  }
}

f_rep <- function(dt) {
  dt[is.na(dt)] <- 0
  return(dt)
}

f_mean <- function(dt) {
  dt[is.na(dt)] <- mean(dt, na.rm = TRUE)
  return(dt)
}

for (i in 2:(ncol(users.cluster.fin)-2)) {
  l1.name = names(users.cluster.fin)[i]
  l1.class = class(users.cluster.fin[[i]])
  print(l1.name)
  if (!l1.class %in% c('integer', 'numeric', 'matrix')){
    users.cluster.fin[[i]] = f_rep(users.cluster.fin[[i]])
  } else {
    users.cluster.fin[[i]] = f_mean(users.cluster.fin[[i]])
  }
}

users.cluster.fin.mean = users.cluster.fin
users.cluster.fin.mean = as.data.frame(users.cluster.fin.mean[0,])

for (i in 2:(ncol(users.cluster.fin)-2)) {
  l1.name = names(users.cluster.fin.mean)[i]
  l1.class = class(users.cluster.fin.mean[[i]])
  print(l1.name)
  if (!l1.class %in% c('integer', 'numeric', 'matrix')){
    users.cluster.fin.mean[1,i] = 0
  } else {
    users.cluster.fin.mean[1,i] = mean(users.cluster.fin[[i]], na.rm = TRUE)
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

for (i in 2:(ncol(users.cluster.fin)-2)) {
  l1.name = names(users.cluster.fin)[i]
  l1.class = class(users.cluster.fin[[i]])
  print(l1.name)
  if (l1.class %in% c('integer', 'numeric', 'matrix')){
    users.cluster.fin[[i]] = as.numeric(scale(users.cluster.fin[[i]], scale = TRUE, center = TRUE))
    users.cluster.fin[[i]] = winsor(users.cluster.fin[[i]])
  }
}

users.cluster.fin[[ncol(users.cluster.fin)-1]] = f_rep(users.cluster.fin[[ncol(users.cluster.fin)-1]])
users.cluster.fin[[ncol(users.cluster.fin)]] = f_rep(users.cluster.fin[[ncol(users.cluster.fin)]])

for (i in 2:(ncol(users.cluster.fin)-2)) {
  l1.name = names(users.cluster.fin)[i]
  l1.class = class(users.cluster.fin[[i]])
  print(l1.name)
  if (!l1.class %in% c('integer', 'numeric', 'matrix')){
    users.cluster.fin[[i]] = as.factor(users.cluster.fin[[i]])
  }
}



users.cluster.fin.num = data.table(rep(NA, nrow(users.cluster.fin)))
users.cluster.fin.fac = data.table(rep(NA, nrow(users.cluster.fin)))

cust_id = users.cluster.fin$cust_id
convert = users.cluster.fin$convert
revenue = users.cluster.fin$revenue
users.cluster.fin.mod = users.cluster.fin[,-c(1,ncol(users.cluster.fin)-1, ncol(users.cluster.fin)), with = FALSE]

for (i in 1:(ncol(users.cluster.fin.mod))) {
  l1.name = names(users.cluster.fin.mod)[i]
  l1.class = class(users.cluster.fin.mod[[i]])
  print(l1.name)
  if (!l1.class %in% c('integer', 'numeric', 'matrix')){
    users.cluster.fin.fac = cbind(users.cluster.fin.fac, users.cluster.fin.mod[[i]])
    colnames(users.cluster.fin.fac)[[ncol(users.cluster.fin.fac)]] = l1.name
  } else {
    users.cluster.fin.num = cbind(users.cluster.fin.num, users.cluster.fin.mod[[i]])
    colnames(users.cluster.fin.num)[[ncol(users.cluster.fin.num)]] = l1.name
  }
}

str(users.cluster.fin.fac)
str(users.cluster.fin.num)

users.cluster.fin.fac[,1] = NULL
users.cluster.fin.num[,1] = NULL

users.cluster.fin.num = Filter(function(x) sd(x) > 0.01, users.cluster.fin.num)

users.cluster.fin.mod = cbind(cust_id, users.cluster.fin.num, users.cluster.fin.fac, convert, revenue)

cluster.name.for.scores = names(users.cluster.fin)
cluster.mod.for.scores = names(users.cluster.fin.mod)

################  H2O  #########################################

h2o.init(nthreads=-1)

#df = airlines.hex

#df <- h2o.importFile(path = "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data")
#df <- h2o.importFile(path = "https://archive.ics.uci.edu/ml/machine-learning-databases/census-income-mld/census-income.data.gz")
#df = h2o.importFile(path = 'http://math.ucdenver.edu/RTutorial/titanic.txt',sep='\t')
# df = as.h2o(titanicDF)
#names(df) = c('age', 'workclass', 'fnlwgt', 'education', 'education-num', 'marital-status', 'occupation', 'relationship', 'race', 'sex', 'capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'income')

df = as.h2o(users.cluster.fin.mod)
dim(df)
print(head(df))
tail(df)

## pick a response for the supervised problem
convert <- "convert"

## the response variable is an integer, we will turn it into a categorical/factor for binary classification
df[[convert]] <- as.factor(df[[convert]])           

## use all other columns (except for the name) as predictors
predictors <- setdiff(names(df), c('convert', 'cust_id', 'revenue')) 

splits <- h2o.splitFrame(
  data = df, 
  ratios = c(0.6,0.2),   ## only need to specify 2 fractions, the 3rd is implied
  destination_frames = c("train.hex", "valid.hex", "test.hex"), seed = 1234
)
train <- splits[[1]]
valid <- splits[[2]]
test  <- splits[[3]]

gbm1 <- h2o.gbm(x = predictors, y = convert, training_frame = train)

## Show a detailed model summary
gbm1

## Get the AUC on the validation set
refAUC = h2o.auc(h2o.performance(gbm1, newdata = test))
h2o.auc(h2o.performance(gbm1, newdata = valid)) 

test = as.data.frame(test)

predictorNames <- setdiff(names(df), c('convert', 'cust_id', 'revenue'))

# Shuffle predictions for variable importance
AUCShuffle <- NULL
shuffletimes <- 50

featuresMeanAUCs <- c()
for (feature in predictorNames) {
  featureAUCs <- c()
  shuffledData <- test
  print(feature)
  for (iter in 1:shuffletimes) {
    shuffledData[,feature] <- sample(shuffledData[,feature], length(shuffledData[,feature]))
    featureAUCs <- c(featureAUCs,h2o.auc(h2o.performance(gbm1, newdata = as.h2o(shuffledData))))
  }
  featuresMeanAUCs <- c(featuresMeanAUCs, mean((featureAUCs+(0.01*featureAUCs)) < refAUC))
}

test = as.h2o(test)

AUCShuffle <- data.frame('feature'=predictorNames, 'importance'=featuresMeanAUCs)
AUCShuffle <- AUCShuffle[order(AUCShuffle$importance, decreasing=TRUE),]
print(AUCShuffle)

predictor.cluster.fin = as.vector(subset(AUCShuffle, importance >= 0.05)$feature)
predictor.cluster.fin


#################################################################


prostate.km3 = h2o.kmeans(df, k = 3, standardize = TRUE, init = 'Furthest', estimate_k = FALSE, max_iterations = 2000, 
                         x = predictor.cluster.fin)
prostate.km4 = h2o.kmeans(df, k = 4, standardize = TRUE, init = 'Furthest', estimate_k = FALSE, max_iterations = 2000, 
                         x = predictor.cluster.fin)
prostate.km5 = h2o.kmeans(df, k = 5, standardize = TRUE, init = 'Furthest', estimate_k = FALSE, max_iterations = 2000, 
                         x = predictor.cluster.fin)
prostate.km6 = h2o.kmeans(df, k = 6, standardize = TRUE, init = 'Furthest', estimate_k = FALSE, max_iterations = 2000, 
                          x = predictor.cluster.fin)
prostate.km7 = h2o.kmeans(df, k = 7, standardize = TRUE, init = 'Furthest', estimate_k = FALSE, max_iterations = 2000, 
                          x = predictor.cluster.fin)
prostate.km8 = h2o.kmeans(df, k = 8, standardize = TRUE, init = 'Furthest', estimate_k = FALSE, max_iterations = 2000, 
                          x = predictor.cluster.fin)
prostate.km9 = h2o.kmeans(df, k = 9, standardize = TRUE, init = 'Furthest', estimate_k = FALSE, max_iterations = 2000, 
                          x = predictor.cluster.fin)
prostate.km10 = h2o.kmeans(df, k = 10, standardize = TRUE, init = 'Furthest', estimate_k = FALSE, max_iterations = 2000, 
                          x = predictor.cluster.fin)

km.short = data.frame(name= numeric(0), min_clust = numeric(0), arpu_var = numeric(0))

km.short[1,1] = 'prostate.km3'
km.short[1,2] = min(h2o.cluster_sizes(prostate.km3))
km.short[2,1] = 'prostate.km4'
km.short[2,2] = min(h2o.cluster_sizes(prostate.km4))
km.short[3,1] = 'prostate.km5'
km.short[3,2] = min(h2o.cluster_sizes(prostate.km5))
km.short[4,1] = 'prostate.km6'
km.short[4,2] = min(h2o.cluster_sizes(prostate.km6))
km.short[5,1] = 'prostate.km7'
km.short[5,2] = min(h2o.cluster_sizes(prostate.km7))
km.short[6,1] = 'prostate.km8'
km.short[6,2] = min(h2o.cluster_sizes(prostate.km8))
km.short[7,1] = 'prostate.km9'
km.short[7,2] = min(h2o.cluster_sizes(prostate.km9))
km.short[8,1] = 'prostate.km10'
km.short[8,2] = min(h2o.cluster_sizes(prostate.km10))

km.short$small = ifelse(km.short$min_clust < nrow(df)/100, 0, 1)

arpu_avg = sum(df$revenue)/nrow(df)

for (i in 3:10) {
  df$cluster = h2o.predict(get(paste('prostate.km',i, sep = '')), df)
  xxx = as.data.frame(df) %>%
    group_by(cluster) %>%
    summarise(arpu = sum(revenue)/length(unique(cust_id)))
  xxx = xxx %>%
    group_by(cluster) %>%
    mutate(arpu_var = (arpu - arpu_avg)^2)
  km.short[i-2,3] = sqrt(sum(xxx$arpu_var)/i)
}

km.final = subset(km.short, small == 1)

final.clust = get(km.final[km.final$arpu_var == max(km.final$arpu_var),1])

h2o.centers(final.clust)

df$cluster = h2o.predict(final.clust, df)

cluster.mod.path = h2o.saveModel(final.clust, path = '/home/ubuntu/ProfileClusters', force = TRUE)

h2o.shutdown(prompt = FALSE)

rm('AUCShuffle', 'event', 'fb', 'km.final', 'km.short', 'shuffledData', 'trans', 'trans.dup', 'users.cluster.fin', 'users.cluster.fin.fac', 'users.cluster.fin.mod', 'users.cluster.fin.num', 'users.cluster.fin', 'trans.load', 'trans.merge', 'users')
