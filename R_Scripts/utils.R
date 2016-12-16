# ==============================================================================
#' Replaces variables in a SQL statement with values supplied
#'
#' @param query The sql query with the variables to replace
#' @param ... A number of variables to replace
#' @return The sql query with the variables replaced
#' @examples
#' new_query <- variableSQL("SELECT $col_name FROM $table",
#'                          col_name ="customer_key",
#'                          table = "sales.item_fact")
print ("utils.R")

variableSQL <- function(query, ...) {
  
  variables <- as.list(match.call())
  
  if (NROW(variables) > 2) {
    # This could also be done simpler with gsubfn
    # http://stackoverflow.com/questions/17475803/sprintf-format-strings-reference-by-name
    for (i in 3:NROW(variables)) {
      # Check if someone passed in a variable without naming it, if so make the
      # the search string equal to the name of the variable passed in
      # eg variableSQL(query, var) instead of variable(query, var = var)
      if (names(variables)[i] == "") {
        searchStr <- paste0("\\$", variables[[i]])
      } else {
        searchStr <- paste0("\\$", names(variables)[i])
      }
      replaceStr <- eval(variables[[i]], envir = parent.frame() )
      query <- gsub(searchStr, replaceStr, query)
    }
  }
  
  return (query)
}


# ==============================================================================
#' Replace a with another if it is does not exists
#'
#' @param x A string of representing the name of the object to check if it exists
#' @param y The value to replace \code{x} with if it does not exists
#' @return The value of the object of x if it exists, otherwise y
#' @examples
#' db_name <- ifExists("aster_settings$db_name", "my_db")
ifExists <- function(x, y) {
  
  if (typeof(x) != "character") stop("first argument must be a character")
  
  return (
    tryCatch({
      x <- eval(parse(text = x))
      ifelse(is.null(x), y, x)
    }, warning = function(w) {
      y
    }, error = function(e) {
      y
    })
  )
  
}

# This function checks if a table exists in Teradata server and drops it if it exists
# ensure that all the users can see it


multiplot <- function(..., plotlist=NULL, file, cols=1, layout=NULL) {
  library(grid)
  
  # Make a list from the ... arguments and plotlist
  plots <- c(list(...), plotlist)
  
  numPlots = length(plots)
  
  # If layout is NULL, then use 'cols' to determine layout
  if (is.null(layout)) {
    # Make the panel
    # ncol: Number of columns of plots
    # nrow: Number of rows needed, calculated from # of cols
    layout <- matrix(seq(1, cols * ceiling(numPlots/cols)),
                     ncol = cols, nrow = ceiling(numPlots/cols))
  }
  
  if (numPlots==1) {
    print(plots[[1]])
    
  } else {
    # Set up the page
    grid.newpage()
    pushViewport(viewport(layout = grid.layout(nrow(layout), ncol(layout))))
    
    # Make each plot, in the correct location
    for (i in 1:numPlots) {
      # Get the i,j matrix positions of the regions that contain this subplot
      matchidx <- as.data.frame(which(layout == i, arr.ind = TRUE))
      
      print(plots[[i]], vp = viewport(layout.pos.row = matchidx$row,
                                      layout.pos.col = matchidx$col))
    }
  }
}

vif_func<-function(in_frame,thresh=5,trace=T, ...){
  require(fmsb)
  #get initial vif value for all comparisons of variables
  vif_init <- NULL
  for(val in names(in_frame))
  {
    form_in  <- formula(paste(val,' ~ .'))
    vif_init <- rbind(vif_init,c(val,VIF(lm(form_in,data=in_frame,...))))
  }
  vif_max <- max(as.numeric(vif_init[,2]))
  if(vif_max < thresh)
  {
    if(trace==T)
    { #print output of each iteration
      prmatrix(vif_init,collab=c('var','vif'),rowlab=rep('',nrow(vif_init)),quote=F)
      cat('\n')
      cat(paste('All variables have VIF < ', thresh,', max VIF ',round(vif_max,2), sep=''),'\n\n')
    }
    return(names(in_frame))
  }
  else
  {
    in_dat<-in_frame
    #backwards selection of explanatory variables, stops when all VIF values are below 'thresh'
    while(vif_max >= thresh)
    {
      vif_vals<-NULL
      
      for(val in names(in_dat))
      {
        form_in<-formula(paste(val,' ~ .'))
        vif_add<-VIF(lm(form_in,data=in_dat,...))
        vif_vals<-rbind(vif_vals,c(val,vif_add))
      }
      
      max_row<-which(vif_vals[,2] == max(as.numeric(vif_vals[,2])))[1]
      vif_max<-as.numeric(vif_vals[max_row,2])
      
      if(vif_max<thresh) break
      if(trace==T)
      { #print output of each iteration
        prmatrix(vif_vals,collab=c('var','vif'),rowlab=rep('',nrow(vif_vals)),quote=F)
        cat('\n')
        cat('removed: ',vif_vals[max_row,1],vif_max,'\n\n')
        flush.console()
      }
      in_dat<-in_dat[,!names(in_dat) %in% vif_vals[max_row,1]]
    }
    return(names(in_dat))
  }
}


export <- function(conn, data, target_table) {
  for (i in 1:nrow(data)) {
    statement <- variableSQL("insert into $target_table values (", target_table)
    for (j in 1:ncol(data)) {
      if(is.numeric(data[,j]) | is.logical(data[,j]) | is.numeric(data[,j])) {
        statement <- paste(statement ,data[i,j], sep = ", ")
      } else {
        statement <- paste(statement ,"'",data[i,j],"', ", sep="")
      }
    }
    statement <- paste(gsub(", ,", ",", statement),")", sep="")
    dbSendQuery(conn, variableSQL( " $statement ", statement))
  }
}

dropifexists <- function(data) {
  
  options(show.error.messages= FALSE) # Change settings so that error message for try function is not displayed
  
  if(class(try(length(conn))) == "try-error" && class(try(length(con))) == "try-error" ) {
    print("Connection is not established")
    options(show.error.messages= TRUE) 
  } else if (class(try(length(conn))) == "try-error") {
    conn <- con
    if(class(try(dbSendQuery(conn, variableSQL("DROP TABLE $data", data)))) == "try-error")
      cat('Table doesnt exist')
  } else  {
    if (class(try(dbSendQuery(conn, variableSQL("DROP TABLE $data", data)))) == "try-error") 
      cat('Table doesnt exist')
  } 
  options(show.error.messages= TRUE)
}
