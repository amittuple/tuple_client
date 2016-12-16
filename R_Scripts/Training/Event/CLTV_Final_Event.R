print ('CLTV_Final_Events')
print (Sys.time())

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

trans$date = as.Date(trans$timestamp)
trans.merge = trans[,c('cust_id','date','revenue'), with = FALSE]
names(trans.merge) = c('cust', 'date', 'sales')
trans.merge$cust = as.integer(trans.merge$cust)

trans.load = rbind(trans.load, trans.merge)

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

trans.load[, sales := mean(sales, na.rm=TRUE), by = list(cust, date)]
trans.load = unique(trans.load)

keycols = c("cust", "date")
setkeyv(trans.load, keycols)

# date - period lookup table
min_date = min(trans.load$date)
max_date = max(trans.load$date)

# create period lookup for each transaction date
dates = seq(min_date, max_date, by = "days")
period = as.numeric(dates - min_date)
lookup_numeric = unique(data.table(date=dates, period=period, key="date"))

# label transactions with corresponding periods in timeline
rows = nrow(trans.load)
trans.load = merge(trans.load, lookup_numeric, by="date", all.x=TRUE)
sum(is.na(trans.load[["period"]]))  # should be zero
nrow(trans.load) == rows # should be TRUE
setkeyv(trans.load, c("cust", "period"))

# calculate integer period intervals
trans.load[, period.int := as.integer(period) + 1]

end.cal.period = max(trans.load$date) - predict.period
trans.load = subset(trans.load, sales >=0)

nowd.hold = trans.load[date > end.cal.period, ]
nowd.cal = trans.load[date <= end.cal.period, ]

nowd.cal[, sales := mean(sales), by = list(cust, period)]
nowd.hold[, sales := mean(sales), by = list(cust, period)]
nowd.cal = unique(nowd.cal[, list(cust, sales, period, period.int)])

# consider only repeat transactions. remove txns in first period
nowd.cal[, first_period := min(period), by = cust]
nowd.cal = nowd.cal[period != first_period, ]

# spend model only need no.of txns(x) and average txn value per period
nowd.cal[, ':=' (m.x.value = mean(sales),
                 x.vector = .N), by = cust]
nowd.cal.spend = unique(nowd.cal[, list(cust, m.x.value, x.vector)])

# remove customers who have not made any repeat txns for estimation to
# avoid warnings
nowd.cal.spend = nowd.cal.spend[x.vector > 0,]
m.x.value = nowd.cal.spend[, m.x.value]
x.vector = nowd.cal.spend[, x.vector]

# estimate model parameters
spend.params = spend.EstimateParameters(m.x.value, x.vector)
spend.params
summary(nowd.cal)
summary(m.x.value)

cal.cbs1 = setDT(data.frame(nowd.cal.spend), keep.rownames = TRUE)[]

pred.cltv = data.frame(cltv= numeric(0))
for (j in 1:nrow(nowd.cal.spend))
{
  m.x.value = as.vector(nowd.cal.spend[j, "m.x.value", with = FALSE])
  x.vector = as.vector(nowd.cal.spend[j, "x.vector", with = FALSE])
  pred.cltv[j,1] = spend.expected.value(spend.params, as.numeric(m.x.value), as.numeric(x.vector))
  j = j+1
}
pred.cltv = cbind(cal.cbs1[, 'cust', with = FALSE], pred.cltv)
colnames(pred.cltv) = c('cust', 'cltv')

print(head(pred.cltv,10))

trans.load.val = subset(trans.load, date > end.cal.period)

cust.val = trans.load %>%
  group_by(cust) %>%
  summarise(sales = sum(sales))

cust.val2 = trans.load.val %>%
  group_by(cust) %>%
  summarise(sales = sum(sales))

cust.val = as.data.table(cust.val)
cust.val2 = as.data.table(cust.val2)

keycols = c("cust")
setkeyv(cust.val, keycols)
setkeyv(cust.val2, keycols)

cltv.val = merge(cust.val, cust.val2, all.x=TRUE)

print(head(cltv.val))

cltv.val$cust = as.integer(cltv.val$cust)


keycols = c("cust")
setkeyv(cltv.val, keycols)
setkeyv(pred.cltv, keycols)

cltv.val = merge(cltv.val, pred.cltv, all.x=TRUE)

f_rep <- function(dt) {
  dt[is.na(dt)] <- 0
  return(dt)
}

cltv.val = f_rep(cltv.val)

print(head(cltv.val, 20))
cor(cltv.val$sales.y, cltv.val$cltv)

rm(list = c('cal.cbs1', 'cust.lapsed', 'cust.ltd', 'cust.rev', 'cust.sltd', 'cust.val', 'cust.val2', 'event', 'lookup_numeric', 'm.x.value', 'nowd.cal', 'nowd.cal.spend', 'nowd.hold', 'pred.cltv', 'trans', 'trans.load', 'trans.load.val', 'x.vector', 'trans.date', 'trans.merge'))
