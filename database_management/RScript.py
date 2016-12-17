import os
import subprocess
from tuple_client.settings import BASE_DIR
class RScript:
    def __init__(self, is_event_log, is_customer_master):
        self.BASE_DIR = BASE_DIR
        self.is_event_log = is_event_log
        self.is_customer_master = is_customer_master
        self.SCRIPT_PATH = os.path.join(self.BASE_DIR, 'R_Scripts')
        self.TRAINING_PATH = os.path.join(self.SCRIPT_PATH, 'Training')
        self.SCORING_PATH = os.path.join(self.SCRIPT_PATH, 'Scoring')
        

    def initial(self):
        with open(os.path.join(self.SCRIPT_PATH, 'RScriptTest.R'), 'w+') as f:
            f.writelines('source("' + str(os.path.join(SCRIPT_PATH, 'redirect_output.R')) + '")\n')
            f.writelines('source("' + str(os.path.join(self.SCRIPT_PATH, 'packages.R')) + '")\n')
            f.writelines('source("' + str(os.path.join(self.SCRIPT_PATH, 'utils.R')) + '")\n')
            f.writelines('source("' + str(os.path.join(self.SCRIPT_PATH, 'yml.R')) + '")\n')
            f.writelines('source("' + str(os.path.join(self.SCRIPT_PATH, 'Connection.R')) + '")\n')
            f.writelines('save.image()\n')

    def event_training(self):
        with open(os.path.join(self.SCRIPT_PATH, 'RScriptTest.R'), 'w+') as f:
            f.writelines('load(".RData")\n')
            f.writelines('source("' + str(os.path.join(SCRIPT_PATH, 'redirect_output.R')) + '")\n')
            f.writelines('source("' + str(os.path.join(self.SCRIPT_PATH, 'Training/Event/CLTV_Final_Event.R')) + '")\n')
            f.writelines('source("' + str(os.path.join(self.SCRIPT_PATH, 'Training/Event/Churn_Event.R')) + '")\n')
            f.writelines('save.image()\n')

    def event_customer_training(self):
        with open(os.path.join(self.SCRIPT_PATH, 'RScriptTest.R'), 'w+') as f:
            f.writelines('load(".RData")\n')
            f.writelines('source("' + str(os.path.join(SCRIPT_PATH, 'redirect_output.R')) + '")\n')
            f.writelines('source("' + str(os.path.join(self.SCRIPT_PATH, 'Training/Event/Customer/High_Convertors_Primary.R')) + '")\n')
            f.writelines('source("' + str(os.path.join(self.SCRIPT_PATH, 'Training/Event/Customer/High_Convertors_Secondary.R')) + '")\n')
            f.writelines('source("' + str(os.path.join(self.SCRIPT_PATH, 'Training/Event/Customer/Clustering_H2O.R')) + '")\n')
            f.writelines('save.image()\n')

    def trans_training(self):
        with open(os.path.join(self.SCRIPT_PATH, 'RScriptTest.R'), 'w+') as f:
            f.writelines('load(".RData")\n')
            f.writelines('source("' + str(os.path.join(SCRIPT_PATH, 'redirect_output.R')) + '")\n')
            f.writelines('source("' + str(os.path.join(self.SCRIPT_PATH, 'Training/Trans/CLTV_Final_Trans.R')) + '")\n')
            f.writelines('source("' + str(os.path.join(self.SCRIPT_PATH, 'Training/Trans/Churn_Trans.R')) + '")\n')
            f.writelines('save.image()\n')

    def trans_customer_training(self):
        with open(os.path.join(self.SCRIPT_PATH, 'RScriptTest.R'), 'w+') as f:
            f.writelines('load(".RData")\n')
            f.writelines('source("' + str(os.path.join(SCRIPT_PATH, 'redirect_output.R')) + '")\n')
            f.writelines('source("' + str(os.path.join(self.SCRIPT_PATH, 'Training/Trans/Customer/High_Convertors_Primary.R')) + '")\n')
            f.writelines('source("' + str(os.path.join(self.SCRIPT_PATH, 'Training/Trans/Customer/High_Convertors_Secondary.R')) + '")\n')
            f.writelines('source("' + str(os.path.join(self.SCRIPT_PATH, 'Training/Trans/Customer/Clustering_H2O.R')) + '")\n')
            f.writelines('save.image()\n')

    def event_scoring(self):
        with open(os.path.join(self.SCRIPT_PATH, 'RScriptTest.R'), 'w+') as f:
            f.writelines('load(".RData")\n')
            f.writelines('source("' + str(os.path.join(SCRIPT_PATH, 'redirect_output.R')) + '")\n')
            f.writelines('source("' + str(os.path.join(self.SCRIPT_PATH, 'Scoring/Event/CLTV_Final_Event_Score.R')) + '")\n')
            f.writelines('source("' + str(os.path.join(self.SCRIPT_PATH, 'Scoring/Event/Churn_Event_Score.R')) + '")\n')
            f.writelines('save.image()\n')

    def event_customer_scoring(self):
        with open(os.path.join(self.SCRIPT_PATH, 'RScriptTest.R'), 'w+') as f:
            f.writelines('load(".RData")\n')
            f.writelines('source("' + str(os.path.join(SCRIPT_PATH, 'redirect_output.R')) + '")\n')
            f.writelines('source("' + str(os.path.join(self.SCRIPT_PATH, 'Scoring/Event/Customer/High_Convertors_Scoring.R')) + '")\n')
            f.writelines('source("' + str(os.path.join(self.SCRIPT_PATH, 'Scoring/Event/Customer/Clustering_H2O_Scoring.R')) + '")\n')
            f.writelines('save.image()\n')

    def trans_scoring(self):
        with open(os.path.join(self.SCRIPT_PATH, 'RScriptTest.R'), 'w+') as f:
            f.writelines('load(".RData")\n')
            f.writelines('source("' + str(os.path.join(SCRIPT_PATH, 'redirect_output.R')) + '")\n')
            f.writelines('source("' + str(os.path.join(self.SCRIPT_PATH, 'Scoring/Trans/CLTV_Final_Trans_Score.R')) + '")\n')
            f.writelines('source("' + str(os.path.join(self.SCRIPT_PATH, 'Scoring/Trans/Churn_Trans_Score.R')) + '")\n')
            f.writelines('save.image()\n')

    def trans_customer_scoring(self):
        with open(os.path.join(self.SCRIPT_PATH, 'RScriptTest.R'), 'w+') as f:
            f.writelines('load(".RData")\n')
            f.writelines('source("' + str(os.path.join(SCRIPT_PATH, 'redirect_output.R')) + '")\n')
            f.writelines('source("' + str(os.path.join(self.SCRIPT_PATH, 'Scoring/Trans/Customer/High_Convertors_Scoring.R')) + '")\n')
            f.writelines('source("' + str(os.path.join(self.SCRIPT_PATH, 'Scoring/Trans/Customer/Clustering_H2O_Scoring.R')) + '")\n')
            f.writelines('save.image()\n')
        
    def run(self):
        command = ['Rscript', os.path.join(self.SCRIPT_PATH, 'RScriptTest.R')]
        return subprocess.call(command, universal_newlines=True)