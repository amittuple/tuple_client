print ('Redirect Output')

zz <- file('/home/ubuntu/tuple_client/R_Logs/R_Log.txt', open = "wt")
sink(zz)
sink(zz, type = "message")
