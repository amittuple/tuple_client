from custom_django_library import CreateModel


def init():
    obj = CreateModel.create_model('MasterTable', app_label='dynamic')
