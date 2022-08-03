from socketserver import BaseRequestHandler,StreamRequestHandler,TCPServer


class EchoHandler(BaseRequestHandler):
    def handle(self):
        print('Got connection from ',self.client_address)

        while True:
            msg = self.request.recv(8192)
            if not msg:
                break
            self.request.send(msg)


class EchoHandler2(StreamRequestHandler):
    '''
    默认这种简易的TCP服务器是单线程的，一次只能为一个客户端连接服务，即若有A、B两个socket都绑定了该服务器
    ，则谁先绑定或connect则谁先占有，且之后该服务器只为这个已绑定的的socket做服务，不对其他socket提供服务。
    '''

    def handle(self):
        print('Got connection from ', self.client_address)

        for line in self.rfile:#客户端发来的二进制信息要以"\n"字符结尾以告诉self.rfile终止读取，否则self.rfile将会一直在读取。
            import time
            time.sleep(10)
            print(line)
            self.wfile.write(line)

if __name__ == '__main__':

    serv = TCPServer(('',20000),EchoHandler2)
    serv.serve_forever()