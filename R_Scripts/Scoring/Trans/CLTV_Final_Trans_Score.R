print ('CLTV_Final_Trans_Score')

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

#library(dplyr)


cust.rev = trans.load %>%
  group_by(cust) %>%
  summarise(revenue = sum(sales))

cust.rev = data.table(cust.rev)
names(cust.rev) = c('cust', 'revenue')
cust.rev$cust = as.integer(cust.rev$cust)


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

end.cal.period = max(trans.load$date)
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

pred.cltv$cltv = ifelse(pred.cltv$cltv < 1, 0, pred.cltv$cltv)

cust.val = trans.load %>%
  group_by(cust) %>%
  summarise(sales = sum(sales))

cust.val = as.data.table(cust.val)

keycols = c("cust")
setkeyv(cust.val, keycols)
setkeyv(pred.cltv, keycols)

cltv.value = merge(cust.val, pred.cltv, all.x=TRUE)

print(head(cltv.value))

cltv.value = f_rep(cltv.value)

value.quant = as.data.frame(quantile(cltv.value$cltv, seq(0,1,by = 0.05)))

cltv.value$value = ifelse(cltv.value$cltv <= value.quant['5%',], 'Very Low', NA)
cltv.value[is.na(cltv.value$value),]$value = ifelse(cltv.value[is.na(cltv.value$value),]$cltv <= value.quant['25%',], 'Low', NA)
cltv.value[is.na(cltv.value$value),]$value = ifelse(cltv.value[is.na(cltv.value$value),]$cltv <= value.quant['75%',], 'Medium', NA)
cltv.value[is.na(cltv.value$value),]$value = ifelse(cltv.value[is.na(cltv.value$value),]$cltv <= value.quant['95%',], 'High', 'Very High')
cltv.value$value = as.factor(cltv.value$value)


cltv.value = as.data.table(cltv.value)
cltv.value$cust = as.integer(cltv.value$cust)


print(head(cltv.value))

cltv.value = cltv.value[,c(1,3,4), with = FALSE]

dbWriteTable(conn, "cltv_value", cltv.value, overwrite = TRUE, row.names = FALSE)

print(head(cltv.value))

rm(list = c('cal.cbs1', 'cust.rev', 'cust.val', 'event', 'lookup_numeric', 'm.x.value', 'nowd.cal', 'nowd.cal.spend', 'nowd.hold', 'pred.cltv', 'trans.load', 'value.quant', 'x.vector'))
