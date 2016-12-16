print ('Churn_Event')
print(Sys.time())

################################## 
#
# Reading Data 
#
#################################
event.table = yml.params$table_map$EVENT_LOG
trans.table = yml.params$table_map$TRANSACTION_MASTER

event <- as.data.table(dbGetQuery(conn, 
                                  variableSQL("SELECT * from $event.table", event.table, stringsAsFactors = FALSE)))

trans <- as.data.table(dbGetQuery(conn, 
                                  variableSQL("SELECT * from $trans.table", trans.table, stringsAsFactors = FALSE)))

print(head(event))
print(head(trans))

colnames(event)[which(colnames(event)== yml.params$column_map$EVENT_LOG$cust_id)] = 'cust_id'
colnames(event)[which(colnames(event)== yml.params$column_map$EVENT_LOG$action_type)] = 'action_type'
colnames(event)[which(colnames(event)== yml.params$column_map$EVENT_LOG$prod_id)] = 'prod_id'
colnames(event)[which(colnames(event)== yml.params$column_map$EVENT_LOG$timestamp)] = 'timestamp'

colnames(trans)[which(colnames(trans)== yml.params$column_map$TRANSACTION_MASTER$cust_id)] = 'cust_id'
colnames(trans)[which(colnames(trans)== yml.params$column_map$TRANSACTION_MASTER$revenue)] = 'revenue'
colnames(trans)[which(colnames(trans)== yml.params$column_map$TRANSACTION_MASTER$prod_id)] = 'prod_id'
colnames(trans)[which(colnames(trans)== yml.params$column_map$TRANSACTION_MASTER$timestamp)] = 'timestamp'

print(head(event))
print(head(trans))


############################################# BTYD ##########################################

trans.load = event[,names(event) %in% c('cust_id','timestamp'), with = FALSE]
trans.load$date = as.Date(trans.load$timestamp)
trans.load$sales = 0
trans.load = trans.load[,c('cust_id','date','sales'), with = FALSE]

print(head(trans.load))

names(trans.load) = c('cust', 'date', 'sales')

print(head(trans.load))

cust.rev = trans %>%
  group_by(cust_id) %>%
  summarise(revenue = sum(revenue))

cust.rev = data.table(cust.rev)
names(cust.rev) = c('cust', 'revenue')
cust.rev$cust = as.integer(cust.rev$cust)

cust.ltd = trans.load %>%
  group_by(cust) %>%
  summarise(ltd = max(date))

cust.ltd = data.table(cust.ltd)
names(cust.ltd) = c('cust', 'ltd')

trans.date = trans.load %>%
  group_by(cust) %>%
  mutate(ltd = max(date))

cust.sltd = trans.date %>%
  filter(date < ltd) %>%
  group_by(cust) %>%
  summarise(sltd = max(date))

names(cust.sltd) = c('cust', 'sltd')
cust.sltd = data.table(cust.sltd)

keycols = c("cust")
setkeyv(cust.ltd, keycols)
setkeyv(cust.sltd, keycols)
setkeyv(cust.rev, keycols)

cust.ltd = merge(cust.ltd,cust.sltd , by="cust", all.x=TRUE)
cust.ltd = merge(cust.ltd,cust.rev , by="cust", all.x=TRUE)

cust.ltd$diff = with(cust.ltd, as.vector(ltd - sltd))

f_rep <- function(dt) {
  dt[is.na(dt)] <- 0
  return(dt)
}

cust.ltd$diff = f_rep(cust.ltd$diff)
cust.ltd$revenue = f_rep(cust.ltd$revenue)

cust.lapsed = cust.ltd %>%
  group_by(diff) %>%
  summarise(cust = length(unique(cust)), rev = sum(revenue))

print(head(cust.lapsed))

cust.lapsed = cust.lapsed %>%
  mutate(cum_cust = cumsum(cust), cum_rev = cumsum(rev))

cust.lapsed = cust.lapsed %>%
  mutate(perc_cust = (cum_cust/max(cum_cust)*100), perc_rev = (cum_rev/max(cum_rev))*100)

predict.period = min(cust.lapsed[cust.lapsed$perc_rev >= 90,]$diff)

library(dplyr)

elog = trans.load %>%
  group_by(cust, date) %>%
  summarise(sales = sum(sales))

print(head(elog))

elog$cust = as.integer(elog$cust)

end.of.cal.period = as.Date(max(elog$date) - predict.period)

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
cal.cbs = dc.BuildCBSFromCBTAndDates(cal.cbt, cal.cbs.dates, per = 'day')

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

elog.val = subset(elog, date > end.of.cal.period)

cust.val = elog %>%
  group_by(cust) %>%
  summarise(visits = length(unique(date)))

cust.val2 = elog.val %>%
  group_by(cust) %>%
  summarise(visits = length(unique(date)))

cust.val = as.data.table(cust.val)
cust.val2 = as.data.table(cust.val2)

keycols = c("cust")
setkeyv(cust.val, keycols)
setkeyv(cust.val2, keycols)

pred.val = merge(cust.val, cust.val2, all.x=TRUE)

print(head(pred.val))

pred.val$cust = as.character(pred.val$cust)


keycols = c("cust")
setkeyv(pred.val, keycols)
setkeyv(pred.fin, keycols)

pred.val = merge(pred.val, pred.fin, all.x=TRUE)

f_rep <- function(dt) {
  dt[is.na(dt)] <- 0
  return(dt)
}

pred.val = f_rep(pred.val)
pred.val$pred.tran = floor(pred.val$pred.tran)
pred.val[pred.val$pred.tran == 0,]$prob.alive = 0

print(head(pred.val, 20))
cor(pred.val$visits.y, pred.val$pred.tran)

rm(list = c('cal.cbs', 'cal.cbs.dates', 'cal.cbs1', 'cal.cbt', 'clean.elog', 'cust.lapsed', 'cust.ltd', 'cust.rev', 'cust.sltd', 'cust.val', 'cust.val2', 'elog', 'elog.cal', 'elog.val', 'event', 'p.matrix', 'pred.fin', 'pred.tran', 'trans', 'trans.date', 'trans.load', 'freq.cbt', 'split.data', 'tot.cbt'))
