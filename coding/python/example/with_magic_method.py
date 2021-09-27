class OpenFile:
    def __init__(self, filename, mode='r'):
        self.fd = open(filename, mode)

    def __enter__(self):
        return self.fd

    def __exit__(self, type, value, trace):
        try:
            if type is None: # 若是沒有發生異常，則為 None 型態
                return
            else:
                self.handle_error(type, value, trace)
        finally:
            self.close_fd()
            return True

    def handle_error(self, type, value, trace):
        print('type:', type)
        print('value:', value)
        print('trace:', trace)

    def close_fd(self):
        self.fd.close()

if __name__ == '__main__':
    with OpenFile('demo.txt') as fd:
        fd.write('Hello World!')