from configparser import ConfigParser

class Keys:
    def __init__(self):
        with open('lib/privatekey.pem', 'rb') as f:
            self.privatekey = f.read()
        with open("lib/publickey.pem","rb") as f:
            self.publickey=f.read()
        
def configdb(filename='lib/database.env', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename, encoding='UTF-8')
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return db