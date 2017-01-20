class DatabaseInfo:
    def __init__(self, host, port, database, username, password):
        self.host = host
        self.database = database
        self.port = port
        self.username = username
        self.password = password

    def get_obj(self):
        return self

    def host(self):
        return self.host

    def database(self):
        return self.database

    def username(self):
        return self.username

    def password(self):
        return self.password

    def port(self):
        return self.port