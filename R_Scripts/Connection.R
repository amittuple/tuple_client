############################################
#
# CONNECTION STRING
#
############################################
print ('Connection.R')

drv <- dbDriver("PostgreSQL")

dbname.yaml = yml.params$DATABASE$NAME
host.yaml = yml.params$DATABASE$HOST
port.yaml = yml.params$DATABASE$PORT
user.yaml = yml.params$DATABASE$USER
password.yaml = yml.params$DATABASE$PASSWORD

# # Set up DB connection
conn <- dbConnect(drv, dbname=dbname.yaml, host=host.yaml, port=port.yaml, user=user.yaml, password=password.yaml)



