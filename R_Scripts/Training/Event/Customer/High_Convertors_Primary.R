print('Event HCP')
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

users.fin = merge(users, fb, by="cust_id", all.x=TRUE)

print(head(users.fin))

Sys.Date()

## This code needs to be changed and proper logic for birthday and create dates should be included

users.fin$age = round(as.vector((Sys.Date() - users.fin$birthday)/365),0)

users.fin$join_month = lubridate::month(users.fin$create_date)

users.fin$birthday = NULL
users.fin$create_date = NULL

trans$cust_id = as.integer(trans$cust_id)

print(head(trans))

trans$convert = 1

trans.dup = trans %>%
  group_by(cust_id) %>%
  summarize(convert = max(convert))

print(head(trans.dup))

colnames(trans.dup) = c('cust_id', 'convert')

trans.dup = data.table(trans.dup)

keycols = c("cust_id")
setkeyv(users, keycols)
setkeyv(trans.dup, keycols)

users.fin = merge(users.fin, trans.dup, by="cust_id", all.x=TRUE)

print(head(users.fin))

str(users.fin)

users.fin$bdate = NULL
users.fin$cdate = NULL

users.num = data.table(rep(NA, nrow(users.fin)))
users.fac = data.table(rep(NA, nrow(users.fin)))

cust_id = users.fin$cust_id
convert = users.fin$convert
users.fin = users.fin[,-c(1, ncol(users.fin)), with = FALSE]

for (i in 1:(ncol(users.fin))) {
  l1.name = names(users.fin)[i]
  l1.class = class(users.fin[[i]])
  print(l1.name)
  if (!l1.class %in% c('integer', 'numeric', 'matrix')){
    users.fac = cbind(users.fac, users.fin[[i]])
    colnames(users.fac)[[ncol(users.fac)]] = l1.name
  } else {
    users.num = cbind(users.num, users.fin[[i]])
    colnames(users.num)[[ncol(users.num)]] = l1.name
  }
}

str(users.fac)
str(users.num)

users.fac[,1] = NULL
users.num[,1] = NULL

users.fac = Filter(function(x) length(unique(x)) <= 100, users.fac)
users.fac = Filter(function(x) length(unique(x))*100/data.row < 5, users.fac)

users.fin = cbind(cust_id, users.num, users.fac, convert)

##################  Replacing Nulls with 0  ########################

trim <- function (x) gsub("^\\s+|\\s+$", "", x)

for (i in 2:(ncol(users.fin)-1)) {
  l1.name = names(users.fin)[i]
  l1.class = class(users.fin[[i]])
  print(l1.name)
  if (!l1.class %in% c('integer', 'numeric', 'matrix')){
    users.fin[[i]] = trim(users.fin[[i]])
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

for (i in 2:(ncol(users.fin)-1)) {
  l1.name = names(users.fin)[i]
  l1.class = class(users.fin[[i]])
  print(l1.name)
  if (!l1.class %in% c('integer', 'numeric', 'matrix')){
    users.fin[[i]] = f_rep(users.fin[[i]])
  } else {
    users.fin[[i]] = f_mean(users.fin[[i]])
  }
}

users.fin.mean = users.fin
users.fin.mean = as.data.frame(users.fin.mean[0,])

for (i in 2:(ncol(users.fin)-1)) {
  l1.name = names(users.fin.mean)[i]
  l1.class = class(users.fin.mean[[i]])
  print(l1.name)
  if (!l1.class %in% c('integer', 'numeric', 'matrix')){
    users.fin.mean[1,i] = 0
  } else {
    users.fin.mean[1,i] = mean(users.fin[[i]], na.rm = TRUE)
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

for (i in 1:(ncol(users.fin))) {
  l1.name = names(users.fin)[i]
  l1.class = class(users.fin[[i]])
  print(l1.name)
  if (!l1.class %in% c('integer', 'numeric', 'matrix')){
    users.fin[[i]] = as.factor(users.fin[[i]])
  }
}

for (i in 2:(ncol(users.fin)-1)) {
  l1.name = names(users.fin)[i]
  l1.class = class(users.fin[[i]])
  print(l1.name)
  if (l1.class %in% c('integer', 'numeric', 'matrix')){
    users.fin[[i]] = scale(users.fin[[i]], scale = TRUE, center = TRUE)
    users.fin[[i]] = winsor(users.fin[[i]])
  }
}

users.fin[[ncol(users.fin)]] = f_rep(users.fin[[ncol(users.fin)]])


users.num = data.table(rep(NA, nrow(users.fin)))
users.fac = data.table(rep(NA, nrow(users.fin)))

cust_id = users.fin$cust_id
convert = users.fin$convert

for (i in 2:(ncol(users.fin)-1)) {
  l1.name = names(users.fin)[i]
  l1.class = class(users.fin[[i]])
  print(l1.name)
  if (!l1.class %in% c('integer', 'numeric', 'matrix')){
    users.fac = cbind(users.fac, users.fin[[i]])
    colnames(users.fac)[[ncol(users.fac)]] = l1.name
  } else {
    users.num = cbind(users.num, users.fin[[i]])
    colnames(users.num)[[ncol(users.num)]] = l1.name
  }
}

str(users.fac)
str(users.num)

users.fac[,1] = NULL
users.num[,1] = NULL


users.fac = acm.disjonctif(users.fac)

users.mod = cbind(cust_id, users.num, users.fac, convert)
str(users.mod)

cust_id = users.mod$cust_id
convert = users.mod$convert
users.mod = users.mod[,-c(1,ncol(users.mod)), with = FALSE]

users.mod = Filter(function(x) sd(x) > 0.01, users.mod)


d_cor <- as.matrix(cor(users.mod))

highlyCor <- findCorrelation(d_cor, cutoff = 0.99)
users.mod = users.mod[,-highlyCor, with = FALSE]

linComb = findLinearCombos(users.mod)
users.mod = users.mod[,-linComb$remove, with = FALSE]

users.mod = cbind(cust_id, users.mod, convert)

name.for.scores = names(users.fin)
mod.for.scores = names(users.mod)

rm(event, fb, users, trans, trans.dup, trans.load, trans.merge, users.fac, users.num)

################  H2O  #########################################

h2o.init(nthreads=-1)

#df = airlines.hex

#df <- h2o.importFile(path = "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data")
#df <- h2o.importFile(path = "https://archive.ics.uci.edu/ml/machine-learning-databases/census-income-mld/census-income.data.gz")
#df = h2o.importFile(path = 'http://math.ucdenver.edu/RTutorial/titanic.txt',sep='\t')
# df = as.h2o(titanicDF)
#names(df) = c('age', 'workclass', 'fnlwgt', 'education', 'education-num', 'marital-status', 'occupation', 'relationship', 'race', 'sex', 'capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'income')

df = as.h2o(users.mod)
dim(df)
print(head(df))
tail(df)

names(df) = c(names(df[,-ncol(df)]), 'response')
## pick a response for the supervised problem
response <- "response"

## the response variable is an integer, we will turn it into a categorical/factor for binary classification
df[[response]] <- as.factor(df[[response]])           

## use all other columns (except for the name) as predictors
predictors <- setdiff(names(df), c('response', 'cust_id')) 

splits <- h2o.splitFrame(
  data = df, 
  ratios = c(0.6,0.2),   ## only need to specify 2 fractions, the 3rd is implied
  destination_frames = c("train.hex", "valid.hex", "test.hex"), seed = 1234
)
train <- splits[[1]]
valid <- splits[[2]]
test  <- splits[[3]]

gbm1 <- h2o.gbm(x = predictors, y = response, training_frame = train)

## Show a detailed model summary
gbm1

## Get the AUC on the validation set
refAUC = h2o.auc(h2o.performance(gbm1, newdata = test))
h2o.auc(h2o.performance(gbm1, newdata = valid)) 

test = as.data.frame(test)

predictorNames <- setdiff(names(df), c('response', 'cust_id', 'revenue'))

# Shuffle predictions for variable importance
AUCShuffle <- NULL
shuffletimes <- 50

Sys.time()

featuresMeanAUCs <- c()
for (feature in predictorNames) {
  featureAUCs <- c()
  shuffledData <- test
  print(feature)
  for (iter in 1:shuffletimes) {
    shuffledData[,feature] <- sample(shuffledData[,feature], length(shuffledData[,feature]))
    featureAUCs <- c(featureAUCs,h2o.auc(h2o.performance(gbm1, newdata = as.h2o(shuffledData))))
  }
  featuresMeanAUCs <- c(featuresMeanAUCs, mean(featureAUCs < refAUC))
}

Sys.time()

test = as.h2o(test)

AUCShuffle <- data.frame('feature'=predictorNames, 'importance'=featuresMeanAUCs)
AUCShuffle <- AUCShuffle[order(AUCShuffle$importance, decreasing=TRUE),]
print(AUCShuffle)

predictor.fin = as.vector(subset(AUCShuffle, importance >= 0.25)$feature)
predictor.fin


####################### GLM ##################################

glm1 = h2o.glm(y = response, x = predictor.fin,
                training_frame = train, family = "binomial")

glm1

h2o.auc(h2o.performance(glm1, newdata = valid)) 

glm2 = h2o.glm(y = response, x = predictor.fin,
                training_frame = train, family = "binomial", standardize=TRUE)

glm2

h2o.auc(h2o.performance(glm2, newdata = valid)) 

alpha_opts = list(list(0), list(.25), list(.5), list(.75), list(1))

hyper_parameters = list(alpha = alpha_opts)

glm.grid <- h2o.grid("glm", hyper_params = hyper_parameters,
                   y = response, x = predictor.fin,
                   training_frame = train, family = "binomial", lambda_search = TRUE, standardize = TRUE, grid_id = 'final_glm')

grid_models <- lapply(glm.grid@model_ids, function(model_id) { model = h2o.getModel(model_id) })


for (i in 1:length(grid_models)) {
  print(sprintf("regularization: %-50s auc: %f", grid_models[[i]]
                   @model$model_summary$regularization, h2o.auc(grid_models[[i]])))
}

sortedGrid.glm <- h2o.getGrid("final_glm", sort_by = "auc", decreasing = TRUE)    
sortedGrid.glm

glm.en.fin <- h2o.getModel(sortedGrid.glm@model_ids[[1]])

h2o.auc(h2o.performance(glm.en.fin, newdata = valid)) 

final.mod = glm.en.fin

#################### Validation ######################################


preds <- h2o.predict(final.mod, test)

print(head(preds))
final.mod@model$validation_metrics@metrics$max_criteria_and_metric_scores

library(pROC)

test = as.data.frame(test)

test$glm.pred = as.vector(preds[,3])

glm.roc = roc(as.vector(test$response), as.vector(preds[,3]))

glm.roc

par(mfrow = c(1,1))

ROCRpred<-prediction(test$glm.pred,test$response)

glm.thresh = coords(glm.roc, x = 'best', ret = 'threshold', best.method = 'closest.topleft')

response.levels = unique(test$response)

test$glm.Alt = ifelse(test$glm.pred <= glm.thresh, as.vector(response.levels[1]), as.vector(response.levels[2]))

library(caret)

glm.cm = confusionMatrix(as.factor(test$glm.Alt), as.factor(test$response))



################# Accuracy & Variable Table #####################

glm.cm

h2o.varimp(final.mod)

################ Accuracy Plots ######################

plot(glm.roc, type = 'S', col = 'firebrick4', legacy.axes = TRUE, main = 'Receiver Operating Curve')
plot(performance(ROCRpred, measure = 'tpr', x.measure = 'fpr'), col = 'orange', main = 'TPR vs. FPR')
plot(performance(ROCRpred, measure = 'prec', x.measure = 'rec'), type = 'S', col = 'blue', legacy.axes = TRUE, main = 'Precision vs. Recall')

test = as.h2o(test)

final.mod.path = h2o.saveModel(final.mod, path = '/home/ubuntu/HighConvertors', force = TRUE)

