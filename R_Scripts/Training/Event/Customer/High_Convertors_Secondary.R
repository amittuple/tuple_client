print('Event HCS')
gbm1 <- h2o.gbm(x = predictor.fin, y = response, training_frame = train)

## Show a detailed model summary
gbm1

## Get the AUC on the validation set
h2o.auc(h2o.performance(gbm1, newdata = valid)) 

hyper_params = list( max_depth = c(4,6,8,12,16,20) ) ##faster for larger datasets

grid <- h2o.grid(
  ## hyper parameters
  hyper_params = hyper_params,
  
  ## full Cartesian hyper-parameter search
  search_criteria = list(strategy = "Cartesian"),
  
  ## which algorithm to run
  algorithm="gbm",
  
  ## identifier for the grid, to later retrieve it
  grid_id="depth_grid",
  
  ## standard model parameters
  x = predictor.fin, 
  y = response, 
  training_frame = train, 
  validation_frame = valid,
  
  ## more trees is better if the learning rate is small enough 
  ## here, use "more than enough" trees - we have early stopping
  ntrees = 10000,                                                            
  
  ## smaller learning rate is better
  ## since we have learning_rate_annealing, we can afford to start with a bigger learning rate
  learn_rate = 0.05,                                                         
  
  ## learning rate annealing: learning_rate shrinks by 1% after every tree 
  ## (use 1.00 to disable, but then lower the learning_rate)
  learn_rate_annealing = 0.99,                                               
  
  ## sample 80% of rows per tree
  sample_rate = 0.8,                                                       
  
  ## sample 80% of columns per split
  col_sample_rate = 0.8, 
  
  ## fix a random number generator seed for reproducibility
  seed = 1234,                                                             
  
  ## early stopping once the validation AUC doesn't improve by at least 0.01% for 5 consecutive scoring events
  stopping_rounds = 5,
  stopping_tolerance = 1e-4,
  stopping_metric = "AUC", 
  
  ## score every 10 trees to make early stopping reproducible (it depends on the scoring interval)
  score_tree_interval = 10                                                
)

## by default, display the grid search results sorted by increasing logloss (since this is a classification task)
grid                                                                       

## sort the grid models by decreasing AUC
sortedGrid <- h2o.getGrid("depth_grid", sort_by="auc", decreasing = TRUE)    
sortedGrid

## find the range of max_depth for the top 5 models
topDepths = sortedGrid@summary_table$max_depth[1:5]                       
minDepth = min(as.numeric(topDepths))
maxDepth = max(as.numeric(topDepths))
minDepth
maxDepth

hyper_params = list( 
  ## restrict the search to the range of max_depth established above
  max_depth = seq(minDepth,maxDepth,1),                                      
  
  ## search a large space of row sampling rates per tree
  sample_rate = seq(0.2,1,0.01),                                             
  
  ## search a large space of column sampling rates per split
  col_sample_rate = seq(0.2,1,0.01),                                         
  
  ## search a large space of column sampling rates per tree
  col_sample_rate_per_tree = seq(0.2,1,0.01),                                
  
  ## search a large space of how column sampling per split should change as a function of the depth of the split
  col_sample_rate_change_per_level = seq(0.9,1.1,0.01),                      
  
  ## search a large space of the number of min rows in a terminal node
  min_rows = 2^seq(0,log2(nrow(train))-1,1),                                 
  
  ## search a large space of the number of bins for split-finding for continuous and integer columns
  nbins = 2^seq(4,10,1),                                                     
  
  ## search a large space of the number of bins for split-finding for categorical columns
  nbins_cats = 2^seq(4,12,1),                                                
  
  ## search a few minimum required relative error improvement thresholds for a split to happen
  min_split_improvement = c(0,1e-8,1e-6,1e-4),                               
  
  ## try all histogram types (QuantilesGlobal and RoundRobin are good for numeric columns with outliers)
  histogram_type = c("UniformAdaptive","QuantilesGlobal","RoundRobin")       
)

search_criteria = list(
  ## Random grid search
  strategy = "RandomDiscrete",      
  
  ## limit the runtime to 60 minutes
  max_runtime_secs = 3600,         
  
  ## build no more than 100 models
  max_models = 100,                  
  
  ## random number generator seed to make sampling of parameter combinations reproducible
  seed = 1234,                        
  
  ## early stopping once the leaderboard of the top 5 models is converged to 0.1% relative difference
  stopping_rounds = 5,                
  stopping_metric = "AUC",
  stopping_tolerance = 1e-3
)

gbm.grid <- h2o.grid(
  ## hyper parameters
  hyper_params = hyper_params,
  
  ## hyper-parameter search configuration (see above)
  search_criteria = search_criteria,
  
  ## which algorithm to run
  algorithm = "gbm",
  
  ## identifier for the grid, to later retrieve it
  grid_id = "final_grid", 
  
  ## standard model parameters
  x = predictor.fin, 
  y = response, 
  training_frame = train, 
  validation_frame = valid,
  
  ## more trees is better if the learning rate is small enough
  ## use "more than enough" trees - we have early stopping
  ntrees = 10000,                                                            
  
  ## smaller learning rate is better
  ## since we have learning_rate_annealing, we can afford to start with a bigger learning rate
  learn_rate = 0.05,                                                         
  
  ## learning rate annealing: learning_rate shrinks by 1% after every tree 
  ## (use 1.00 to disable, but then lower the learning_rate)
  learn_rate_annealing = 0.99,                                               
  
  ## early stopping based on timeout (no model should take more than 1 hour - modify as needed)
  max_runtime_secs = 3600,                                                 
  
  ## early stopping once the validation AUC doesn't improve by at least 0.01% for 5 consecutive scoring events
  stopping_rounds = 5, stopping_tolerance = 1e-4, stopping_metric = "AUC", 
  
  ## score every 10 trees to make early stopping reproducible (it depends on the scoring interval)
  score_tree_interval = 10,                                                
  
  ## base random number generator seed for each model (automatically gets incremented internally for each model)
  seed = 1234                                                             
)

## Sort the grid models by AUC
sortedGrid <- h2o.getGrid("final_grid", sort_by = "auc", decreasing = TRUE)    
sortedGrid

for (i in 1:5) {
  gbm3 <- h2o.getModel(sortedGrid@model_ids[[i]])
  print(h2o.auc(h2o.performance(gbm3, valid = TRUE)))
}

gbm4 <- h2o.getModel(sortedGrid@model_ids[[1]])
print(h2o.auc(h2o.performance(gbm4, newdata = test)))

gbm4@parameters

model <- do.call(h2o.gbm,
                 ## update parameters in place
                 {
                   p <- gbm4@parameters
                   p$model_id = NULL          ## do not overwrite the original grid model
                   p$training_frame = df      ## use the full dataset
                   p$validation_frame = NULL  ## no validation frame
                   p$nfolds = 5               ## cross-validation
                   p
                 }
)
model@model$cross_validation_metrics_summary

# for (i in 1:5) {
#   gbm5 <- h2o.getModel(sortedGrid@model_ids[[i]])
#   cvgbm <- do.call(h2o.gbm,
#                    ## update parameters in place
#                    {
#                      p <- gbm5@parameters
#                      p$model_id = NULL          ## do not overwrite the original grid model
#                      p$training_frame = df      ## use the full dataset
#                      p$validation_frame = NULL  ## no validation frame
#                      p$nfolds = 5               ## cross-validation
#                      p
#                    }
#   )
#   print(gbm5@model_id)
#   print(cvgbm@model$cross_validation_metrics_summary[2,]) ## Pick out the "AUC" row
# }

gbm.fin <- h2o.getModel(sortedGrid@model_ids[[1]])


#################### Validation ######################################


preds <- h2o.predict(gbm.fin, test)

head(preds)
gbm.fin@model$validation_metrics@metrics$max_criteria_and_metric_scores

library(pROC)

test = as.data.frame(test)

test$gbm.pred = as.vector(preds[,3])

gbm.roc = roc(as.vector(test$response), as.vector(preds[,3]))

gbm.roc

par(mfrow = c(1,1))

ROCRpred<-prediction(test$gbm.pred,test$response)

gbm.thresh = coords(gbm.roc, x = 'best', ret = 'threshold', best.method = 'closest.topleft')

response.levels = unique(test$response)

test$gbm.Alt = ifelse(test$gbm.pred <= gbm.thresh, as.vector(response.levels[1]), as.vector(response.levels[2]))

library(caret)

gbm.cm = confusionMatrix(as.factor(test$gbm.Alt), as.factor(test$response))



################# Accuracy & Variable Table #####################

gbm.cm

h2o.varimp(gbm.fin)

################ Accuracy Plots ######################

plot(gbm.roc, type = 'S', col = 'firebrick4', legacy.axes = TRUE, main = 'Receiver Operating Curve')
plot(performance(ROCRpred, measure = 'tpr', x.measure = 'fpr'), col = 'orange', main = 'TPR vs. FPR')
plot(performance(ROCRpred, measure = 'prec', x.measure = 'rec'), type = 'S', col = 'blue', legacy.axes = TRUE, main = 'Precision vs. Recall')

gbm.mod.path = h2o.saveModel(gbm.fin, path = '/home/ubuntu/HighConvertors/GBM', force = TRUE)

rm(list = c('AUCShuffle', 'd_cor', 'shuffledData', 'users.mod', 'test', 'users.fin'))

h2o.shutdown(prompt = FALSE)
