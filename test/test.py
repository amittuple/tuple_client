import os
import subprocess

class Test:
    def __init__(self):
        try:
            script_path = '/home/ubuntu/tuple_client/R_Scripts/'
            with open(os.path.join(script_path, 'RScript.R'), 'w+') as f:
                f.writelines('source("'+str(os.path.join(script_path, 'packages.R'))+'")\n')
                f.writelines('source("'+str(os.path.join(script_path, 'utils.R'))+'")\n')
                f.writelines('source("'+str(os.path.join(script_path, 'yml.R'))+'")\n')
                f.writelines('source("'+str(os.path.join(script_path, 'Connection.R'))+'")\n')
                f.writelines('source("'+str(os.path.join(script_path, 'Training/Trans/CLTV_Final_Trans.R'))+'")\n')
                f.writelines('source("'+str(os.path.join(script_path, 'Training/Trans/Churn_Trans.R'))+'")\n')
                f.writelines('source("'+str(os.path.join(script_path, 'Scoring/Trans/CLTV_Final_Trans_Score.R'))+'")\n')
                f.writelines('source("'+str(os.path.join(script_path, 'Scoring/Trans/Churn_Trans_Score.R'))+'")\n')
        except Exception as e:
            print e
    def call(self):
        try:
            script_path = '/home/ubuntu/tuple_client/R_Scripts/'
            command = ['Rscript', os.path.join(script_path, 'RScript.R')]
            subprocess.call(command, universal_newlines=True)
        except Exception as e:
            print e
    # def __init__(self):
    #     try:
    #         script_path = '/home/ubuntu/tuple_client/R_Scripts/'
    #         with open(os.path.join(script_path, 'RScript.R'), 'w+') as f:
    #
    #             file = open(os.path.join(script_path, 'packages.R'), 'r')
    #             f.writelines(file.readlines())
    #             file = open(os.path.join(script_path, 'utils.R'), 'r')
    #             f.writelines(file.readlines())
    #             file = open(os.path.join(script_path, 'yml.R'), 'r')
    #             f.writelines(file.readlines())
    #             file = open(os.path.join(script_path, 'Connection.R'), 'r')
    #             f.writelines(file.readlines())
    #             file = open(os.path.join(script_path, 'Training/Trans/CLTV_Final_Trans.R'), 'r')
    #             f.writelines(file.readlines())
    #             file = open(os.path.join(script_path, 'Training/Trans/Churn_Trans.R'), 'r')
    #             f.writelines(file.readlines())
    #             file = open(os.path.join(script_path, 'Scoring/Trans/CLTV_Final_Trans_Score.R'), 'r')
    #             f.writelines(file.readlines())
    #             file = open(os.path.join(script_path, 'Scoring/Trans/Churn_Trans_Score.R'), 'r')
    #             f.writelines(file.readlines())
    #
    #             command = ['Rscript', os.path.join(script_path, 'RScript.R')]
    #             subprocess.call(command, universal_newlines=True)
    #     except Exception as e:
    #         print e
