import os
from tuple_client.settings import BASE_DIR

class CombineR:
    def __init__(self, is_event_log, is_customer_master):
        self.is_event_log = is_event_log
        self.is_customer_master = is_customer_master
        self.SCRIPT_PATH = os.path.join(BASE_DIR, 'R_Scripts')
        self.TRAINING_PATH = os.path.join(self.SCRIPT_PATH, 'Training')
        self.SCORING_PATH = os.path.join(self.SCRIPT_PATH, 'Scoring')
        
    
    def combine(self):
        try:
            with open(os.path.join(self.SCRIPT_PATH, 'RScript.R'), 'w+') as f:

                f.write("sink('~/R_Logs/R_Log.txt') \n")
                file = open(os.path.join(self.SCRIPT_PATH, 'Connection.R'), 'r')
                f.writelines(file.readlines())
    
    
                # Training
                if self.is_event_log:
                    file = open(os.path.join(self.SCRIPT_PATH, 'Training/Event/CLTV_Final_Event.R'), 'r')
                    f.writelines(file.readlines())
                    file = open(os.path.join(self.SCRIPT_PATH, 'Training/Event/Churn_Event.R'), 'r')
                    f.writelines(file.readlines())
                    if self.is_customer_master:
                        file = open(os.path.join(self.SCRIPT_PATH, 'Training/Event/Customer/High_Convertors_Primary.R'), 'r')
                        f.writelines(file.readlines())
                        file = open(os.path.join(self.SCRIPT_PATH, 'Training/Event/Customer/High_Convertors_Secondary.R'), 'r')
                        f.writelines(file.readlines())
                        file = open(os.path.join(self.SCRIPT_PATH, 'Training/Event/Customer/Clustering_H2O.R'), 'r')
                        f.writelines(file.readlines())
                else:
                    file = open(os.path.join(self.SCRIPT_PATH, 'Training/Trans/CLTV_Final_Trans.R'), 'r')
                    f.writelines(file.readlines())
                    file = open(os.path.join(self.SCRIPT_PATH, 'Training/Trans/Churn_Trans.R'), 'r')
                    f.writelines(file.readlines())
                    if self.is_customer_master:
                        file = open(os.path.join(self.SCRIPT_PATH, 'Training/Trans/Customer/High_Convertors_Primary.R'), 'r')
                        f.writelines(file.readlines())
                        file = open(os.path.join(self.SCRIPT_PATH, 'Training/Trans/Customer/High_Convertors_Secondary.R'), 'r')
                        f.writelines(file.readlines())
                        file = open(os.path.join(self.SCRIPT_PATH, 'Training/Trans/Customer/Clustering_H2O.R'), 'r')
                        f.writelines(file.readlines())
    
    
                # Scoring
                if self.is_event_log:
                    file = open(os.path.join(self.SCRIPT_PATH, 'Scoring/Event/CLTV_Final_Event_Score.R'), 'r')
                    f.writelines(file.readlines())
                    file = open(os.path.join(self.SCRIPT_PATH, 'Scoring/Event/Churn_Event_Score.R'), 'r')
                    f.writelines(file.readlines())
                    if self.is_customer_master:
                        file = open(os.path.join(self.SCRIPT_PATH, 'Scoring/Event/Customer/High_Convertors_Scoring.R'), 'r')
                        f.writelines(file.readlines())
                        file = open(os.path.join(self.SCRIPT_PATH, 'Scoring/Event/Customer/Clustering_H2O_Scoring.R'), 'r')
                        f.writelines(file.readlines())
                else:
                    file = open(os.path.join(self.SCRIPT_PATH, 'Scoring/Trans/CLTV_Final_Trans_Score.R'), 'r')
                    f.writelines(file.readlines())
                    file = open(os.path.join(self.SCRIPT_PATH, 'Scoring/Trans/Churn_Trans_Score.R'), 'r')
                    f.writelines(file.readlines())
                    if self.is_customer_master:
                        file = open(os.path.join(self.SCRIPT_PATH, 'Scoring/Trans/Customer/High_Convertors_Scoring.R'), 'r')
                        f.writelines(file.readlines())
                        file = open(os.path.join(self.SCRIPT_PATH, 'Scoring/Trans/Customer/Clustering_H2O_Scoring.R'), 'r')
                        f.writelines(file.readlines())
        except Exception as e:
            print e



temp = CombineR(is_event_log=True, is_customer_master=True)
temp.combine()
