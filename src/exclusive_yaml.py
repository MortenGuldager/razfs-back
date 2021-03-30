import fcntl
import yaml

class exclusive_yaml:
    class Locked(Exception): pass

    def __init__(self, filename):
        self.fd = open(filename, 'a+')
        try:
            fcntl.flock(self.fd.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise self.Locked
        
    def load(self):
        self.fd.seek(0)
        data = yaml.load(self.fd, Loader=yaml.SafeLoader)
        if data is None:
            data = {}
        return data

    def save(self, data):
        self.fd.truncate(0)
        yaml.dump(data, self.fd)

    def __del__(self):
        self.fd.close()
