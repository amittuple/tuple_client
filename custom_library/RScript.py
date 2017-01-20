import os

class RScript:
    def __init__(self, BASE_DIR, SCRIPT_NAME, is_event_log, is_customer_master):
        self.BASE_DIR = BASE_DIR
        self.is_event_log = is_event_log
        self.is_customer_master = is_customer_master
        self.SCRIPT_PATH = os.path.join(self.BASE_DIR, 'R_Scripts')
        self.TRAINING_PATH = os.path.join(self.SCRIPT_PATH, 'Training')
        self.SCORING_PATH = os.path.join(self.SCRIPT_PATH, 'Scoring')
        self.SCRIPT_NAME = SCRIPT_NAME

    def load_data(self,f):
        f.writelines('load(".RData")\n')

    def save_data(self, f):
        f.writelines('save.image()\n')

    def initial(self, f):
        f.writelines('source("' + str(os.path.join(self.SCRIPT_PATH, 'redirect_output.R')) + '")\n')
        f.writelines('source("' + str(os.path.join(self.SCRIPT_PATH, 'packages.R')) + '")\n')
        f.writelines('source("' + str(os.path.join(self.SCRIPT_PATH, 'utils.R')) + '")\n')
        f.writelines('source("' + str(os.path.join(self.SCRIPT_PATH, 'yml.R')) + '")\n')
        f.writelines('source("' + str(os.path.join(self.SCRIPT_PATH, 'Connection.R')) + '")\n')

    def event_training(self, f):
        f.writelines('source("' + str(os.path.join(self.SCRIPT_PATH, 'Training/Event/CLTV_Final_Event.R')) + '")\n')
        f.writelines('source("' + str(os.path.join(self.SCRIPT_PATH, 'Training/Event/Churn_Event.R')) + '")\n')

    def event_customer_training(self, f):
        f.writelines('source("' + str(os.path.join(self.SCRIPT_PATH, 'Training/Event/Customer/High_Convertors_Primary.R')) + '")\n')
        f.writelines('source("' + str(os.path.join(self.SCRIPT_PATH, 'Training/Event/Customer/High_Convertors_Secondary.R')) + '")\n')
        f.writelines('source("' + str(os.path.join(self.SCRIPT_PATH, 'Training/Event/Customer/Clustering_H2O.R')) + '")\n')

    def trans_training(self, f):
        f.writelines('source("' + str(os.path.join(self.SCRIPT_PATH, 'Training/Trans/CLTV_Final_Trans.R')) + '")\n')
        f.writelines('source("' + str(os.path.join(self.SCRIPT_PATH, 'Training/Trans/Churn_Trans.R')) + '")\n')

    def trans_customer_training(self, f):
        f.writelines('source("' + str(os.path.join(self.SCRIPT_PATH, 'Training/Trans/Customer/High_Convertors_Primary.R')) + '")\n')
        f.writelines('source("' + str(os.path.join(self.SCRIPT_PATH, 'Training/Trans/Customer/High_Convertors_Secondary.R')) + '")\n')
        f.writelines('source("' + str(os.path.join(self.SCRIPT_PATH, 'Training/Trans/Customer/Clustering_H2O.R')) + '")\n')

    def event_scoring(self, f):
        f.writelines('source("' + str(os.path.join(self.SCRIPT_PATH, 'Scoring/Event/CLTV_Final_Event_Score.R')) + '")\n')
        f.writelines('source("' + str(os.path.join(self.SCRIPT_PATH, 'Scoring/Event/Churn_Event_Score.R')) + '")\n')

    def event_customer_scoring(self, f):
        f.writelines('source("' + str(os.path.join(self.SCRIPT_PATH, 'Scoring/Event/Customer/High_Convertors_Scoring.R')) + '")\n')
        f.writelines('source("' + str(os.path.join(self.SCRIPT_PATH, 'Scoring/Event/Customer/Clustering_H2O_Scoring.R')) + '")\n')

    def trans_scoring(self, f):
        f.writelines('source("' + str(os.path.join(self.SCRIPT_PATH, 'Scoring/Trans/CLTV_Final_Trans_Score.R')) + '")\n')
        f.writelines('source("' + str(os.path.join(self.SCRIPT_PATH, 'Scoring/Trans/Churn_Trans_Score.R')) + '")\n')

    def trans_customer_scoring(self, f):
        f.writelines('source("' + str(os.path.join(self.SCRIPT_PATH, 'Scoring/Trans/Customer/High_Convertors_Scoring.R')) + '")\n')
        f.writelines('source("' + str(os.path.join(self.SCRIPT_PATH, 'Scoring/Trans/Customer/Clustering_H2O_Scoring.R')) + '")\n')

    def training(self, f):
        if self.is_event_log:
            self.event_training(f)
            if self.is_customer_master:
                self.event_customer_training(f)
        else:
            self.trans_training(f)
            if self.is_customer_master:
                self.trans_customer_training(f)

    def scoring(self, f):
        if self.is_event_log:
            self.event_scoring(f)
            if self.is_customer_master:
                self.event_customer_scoring(f)
        else:
            self.trans_scoring(f)
            if self.is_customer_master:
                self.trans_customer_scoring(f)

    def run_complete(self):
        with open(os.path.join(self.SCRIPT_PATH, self.SCRIPT_NAME), 'w+') as f:
            self.load_data(f)
            self.initial(f)
            # Training
            self.training(f)
            # Scoring
            self.scoring(f)
            self.save_data(f)

    def run_training(self):
        with open(self.SCRIPT_PATH, self.SCRIPT_NAME) as f:
            self.load_data(f)
            self.initial(f)
            self.training(f)
            self.save_data(f)

    def run_scoring(self):
        with open(self.SCRIPT_PATH, self.SCRIPT_NAME) as f:
            self.load_data(f)
            self.initial(f)
            self.scoring(f)
            self.save_data(f)

# obj = RScript('/home/adnan/tuple_client/', 'RS.R', False, False)
#
# obj.run()
