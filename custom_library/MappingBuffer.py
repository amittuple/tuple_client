import yaml

class MappingBuffer:
    def __init__(self, MAP_PATH):
        self.MAP_PATH = MAP_PATH

    def our_table_names(self):
        temp = []
        with open(self.MAP_PATH, 'r') as f:
            data = yaml.load(f)
            if data.has_key('table_map'):
                for key in data['table_map']:
                    temp.append(key)
        return temp

    def is_event_log(self):
        event = None
        with open(self.MAP_PATH, 'r') as f:
            data = yaml.load(f)
            event_log = data['table_map']['EVENT_LOG']
            if event_log == None or event_log == '':
                event = False
            else:
                event = True
        return event

    def is_customer_master(self):
        customer = None
        with open(self.MAP_PATH, 'r') as f:
            data = yaml.load(f)
            customer_master = data['table_map']['CUSTOMER_MASTER']
            if customer_master == None or customer_master == '':
                customer = False
            else:
                customer = True
        return customer

    def connect(self):
        with open('/home/adnan/tuple_client/mappings/MappingBuffer.yml', 'r') as f:
            data = yaml.load(f)
            print data['DATABASE']
            print data['asd']

    def example(self):
        temp = {
            'asd': 'asd',
            'zxc': None,
            'asdasd': [
                'asd',
                'asd',
            ],
            'asz': []
        }
        document = """
                  a: 1
                  b:
                    c: 3
                    d: 4
                  e:
                """
        print yaml.load(document)
        print yaml.dump(temp)



# obj = MappingBuffer('mapping_skeleton.yml')
# print obj.our_table_names()
# print obj.is_event_log()
# print obj.is_customer_master()