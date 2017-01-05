print ('Churn_Trans_Score')

################################## 
#
# Reading Data 
#
#################################
trans.table = yml.params$table_map$TRANSACTION_MASTER


event <- as.data.table(dbGetQuery(conn, 
                                  variableSQL("SELECT * from $trans.table", trans.table, stringsAsFactors = FALSE)))

#print(head(trans))

colnames(event)[which(colnames(event)== yml.params$column_map$TRANSACTION_MASTER$cust_id)] = 'cust_id'
colnames(event)[which(colnames(event)== yml.params$column_map$TRANSACTION_MASTER$revenue)] = 'revenue'
colnames(event)[which(colnames(event)== yml.params$column_map$TRANSACTION_MASTER$prod_id)] = 'prod_id'
colnames(event)[which(colnames(event)== yml.params$column_map$TRANSACTION_MASTER$timestamp)] = 'timestamp'

print(head(event))


############################################# BTYD ##########################################

trans.load = event[,names(event) %in% c('cust_id','timestamp'), with = FALSE]
trans.load$date = as.Date(trans.load$timestamp)
trans.load$sales = event$revenue
trans.load = trans.load[,c('cust_id','date','sales'), with = FALSE]

print(head(trans.load))

names(trans.load) = c('cust', 'date', 'sales')

elog = trans.load %>%
  group_by(cust, date) %>%
  summarise(sales = sum(sales))

print(head(elog))

elog$cust = as.integer(elog$cust)

#########################################################

## FULL MODEL  ##

#########################################################

end.of.cal.period = as.Date(min(elog$date) + as.vector(max(elog$date) - min(elog$date)))

dc.SplitUpElogForRepeatTrans = function(elog) {
  elog <- elog[order(elog$date),]
  elog <- elog[order(elog$cust),]
  
  dc.WriteLine("Started Creating Repeat Purchases")
  unique.custs <- unique(elog$cust)
  
  x <- data.table(elog)
  x$i <- 1:nrow(elog)
  keycols <- c('cust', 'date')
  setkeyv(x, keycols)
  first <- x[J(unique(cust)), mult='first']
  first <- as.data.frame(first)
  last <- x[J(unique(cust)), mult='last']
  last <- as.data.frame(last)
  
  repeat.trans.elog <- elog[-first$i, ]
  first.trans.data <- as.data.frame(first)
  last.trans.data <- as.data.frame(last)
  
  
  # [-1] is because we don't want to change the column name for custs
  names(first.trans.data)[-1] <- paste("first.", names(first.trans.data)[-1], sep = "")
  names(first.trans.data)[which(names(first.trans.data) == "first.date")] <- "birth.per"
  names(last.trans.data) <- paste("last.", names(last.trans.data), sep = "")
  
  # [-1] is because we don't want to include two custs columns
  cust.data <- data.frame(first.trans.data, last.trans.data[, -1])
  names(cust.data) <- c(names(first.trans.data), names(last.trans.data)[-1])
  
  dc.WriteLine("Finished Creating Repeat Purchases")
  return(list(repeat.trans.elog = repeat.trans.elog, cust.data = cust.data))
}

Sys.time()

pred.fin = data.table(cust = numeric(0), pred.tran= numeric(0), prob.alive = numeric(0))

elog.cal = elog[which(elog$date <= end.of.cal.period),]
elog.cal = elog.cal[order(elog.cal$date),]
elog.cal = elog.cal[order(as.numeric(elog.cal$cust)),]


split.data =  dc.SplitUpElogForRepeatTrans(elog.cal)
clean.elog = split.data$repeat.trans.elog[order(as.numeric(split.data$repeat.trans.elog$cust)),]
freq.cbt = dc.CreateFreqCBT(clean.elog)
tot.cbt = dc.CreateFreqCBT(elog.cal)
cal.cbt = dc.MergeCustomers(tot.cbt, freq.cbt)

## The custom function to speed up Split up mugs the order of the data frames and hence gives an incorrect data frame for cal.cbs
## which never converges. The temporary fix below only works for cust column which is inheretly numeric

birth.periods <- split.data$cust.data[order(as.numeric(split.data$cust.data$cust)),]$birth.per
last.dates <- split.data$cust.data[order(as.numeric(split.data$cust.data$cust)),]$last.date
cal.cbs.dates = data.frame(birth.periods, last.dates, end.of.cal.period)
cal.cbs = dc.BuildCBSFromCBTAndDates(cal.cbt, cal.cbs.dates, per = 'month')

print(head(as.data.frame(cal.cbs)))

###################################

params = bgnbd.EstimateParameters(cal.cbs)
params

LL = bgnbd.cbs.LL(params, cal.cbs)
LL

p.matrix = c(params, LL)
for (i in 1:2) {
  params = bgnbd.EstimateParameters(cal.cbs, params)
  LL = bgnbd.cbs.LL(params, cal.cbs)
  p.matrix.row = c(params, LL)
  p.matrix = rbind(p.matrix, p.matrix.row)
}

colnames(p.matrix) = c('r', 'alpha', 'a', 'b', 'LL')
rownames(p.matrix) = 1:3

p.matrix

bgnbd.Expectation(params, t = as.vector(predict.period))

cal.cbs1 = setDT(data.frame(cal.cbs), keep.rownames = TRUE)[]

pred.tran = data.frame(pred.tran= numeric(0), pred.prob = numeric(0))
for (j in 1:nrow(cal.cbs))
{
  x = cal.cbs[j, "x"]
  t.x = cal.cbs[j, "t.x"]
  T.cal = cal.cbs[j, "T.cal"]
  pred.tran[j,1] = bgnbd.ConditionalExpectedTransactions(params, T.star = as.vector(predict.period), x, t.x, T.cal)
  pred.tran[j,2] = bgnbd.PAlive(params, x, t.x, T.cal)
  j = j+1
}
pred.fin = cbind(cal.cbs1[, 'rn', with = FALSE], pred.tran)
colnames(pred.fin) = c('cust', 'pred.tran', 'prob.alive')

print(head(pred.fin,10))

pred.fin$pred.tran = floor(pred.fin$pred.tran)
pred.fin[pred.fin$pred.tran == 0,]$prob.alive = 0

cust.fin = elog %>%
  group_by(cust) %>%
  summarise(visits = length(unique(date)))

cust.fin = as.data.table(cust.fin)

cust.fin$cust = as.character(cust.fin$cust)

keycols = c("cust")
setkeyv(cust.fin, keycols)
setkeyv(pred.fin, keycols)

cust.fin = merge(cust.fin, pred.fin, all.x=TRUE)

cust.fin = f_rep(cust.fin)

cust.fin$churn = ifelse(cust.fin$prob.alive <= 0.5, 1, 0)

engage.quant = as.data.frame(quantile(cust.fin$pred.tran, seq(0,1,by = 0.05)))

cust.fin$engagement = ifelse(cust.fin$pred.tran <= engage.quant['5%',], 'Very Low', NA)
cust.fin[is.na(cust.fin$engagement),]$engagement = ifelse(cust.fin[is.na(cust.fin$engagement),]$pred.tran <= engage.quant['25%',], 'Low', NA)
cust.fin[is.na(cust.fin$engagement),]$engagement = ifelse(cust.fin[is.na(cust.fin$engagement),]$pred.tran <= engage.quant['75%',], 'Medium', NA)
cust.fin[is.na(cust.fin$engagement),]$engagement = ifelse(cust.fin[is.na(cust.fin$engagement),]$pred.tran <= engage.quant['95%',], 'High', 'Very High')
cust.fin$engagement = as.factor(cust.fin$engagement)


cust.fin = as.data.table(cust.fin)
cust.fin$cust = as.integer(cust.fin$cust)


print(head(cust.fin))

#-------------------Percentile-------------------------#

cust.fin = cust.fin %>%
  mutate(percent_churn = percent_rank(cust.fin$pred.tran))

#-------------------------------------------------------
churn.engage = cust.fin[,c(1,5,6,7)]

print(head(churn.engage))

dbWriteTable(conn, "churn_engagement", churn.engage, overwrite = TRUE, row.names = FALSE)

Predict_Period = as.data.frame(predict.period)
names(Predict_Period) = 'period'
dbWriteTable(conn, "predict_period", Predict_Period , overwrite = TRUE, row.names = FALSE)

rm(list = c('cal.cbs', 'cal.cbs.dates', 'cal.cbs1', 'cal.cbt', 'churn.engage', 'clean.elog', 'cust.fin', 'elog', 'elog.cal','engage.quant', 'event', 'p.matrix', 'pred.fin', 'pred.tran', 'trans.load', 'birth.periods', 'end.of.cal.period', 'freq.cbt', 'i', 'j', 'keycols', "last.dates", 'LL', 'p.matrix.row', 'params', 'split.data', 'T.cal', 't.x', 'toInstall', 'toInstallCandidates', 'tot.cbt', 'x', 'Predict_Period'))

