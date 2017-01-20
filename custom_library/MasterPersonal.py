import subprocess


class MasterPersonal:
    def __init__(self):
        self.HOME_PATH = '/home/adnan'
        self.MODEL_PATH = self.HOME_PATH+'/tuple_client/team/models.py'

    def command(self):
        command = 'export WORKON_HOME=~/Envs;'
        command = command + 'source '+self.HOME_PATH+'/.local/bin/virtualenvwrapper.sh;'
        command = command + 'workon envOne;'
        command = command + 'python '+self.HOME_PATH+'/tuple_client/manage.py inspectdb master_table personal_table > ' + self.MODEL_PATH + ';'
        command = command + 'python '+self.HOME_PATH+'/tuple_client/manage.py makemigrations team;'
        return command

    def bash_command(self,command):
        proc = subprocess.Popen(command, shell=True, executable='/bin/bash', stdout=subprocess.PIPE)
        temp = proc.communicate()
        print temp


obj = MasterPersonal()
obj.bash_command(obj.command())