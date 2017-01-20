from celery import Celery
from custom_library.RScript import RScript
from tuple_client.settings import MAPPING_PATH, SCRIPT_PATH, BASE_DIR
from custom_library.MappingBuffer import MappingBuffer
import os
import subprocess
app = Celery('tuple_client')

@app.task
def scoring():
    mapping = MappingBuffer(MAPPING_PATH, 'MappingBuffer.yml')
    r_code = RScript(BASE_DIR, 'RScoring.R', mapping.is_event_log(),mapping.is_customer_master())
    r_code.run_scoring()
    command = ['Rscript', os.path.join(SCRIPT_PATH, 'RScoring.R')]
    subprocess.call(command, universal_newlines=True)

@app.task
def training():
    mapping = MappingBuffer(MAPPING_PATH, 'MappingBuffer.yml')
    r_code = RScript(BASE_DIR, 'RTraining.R', mapping.is_event_log(), mapping.is_customer_master())
    r_code.run_training()
    command = ['RScript', os.path.join(SCRIPT_PATH, 'RTraining.R')]
    subprocess.call(command, universal_newlines=True)
