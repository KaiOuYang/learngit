


from socketserver import BaseRequestHandler,UDPServer
import time

class TimeHandler(BaseRequestHandler):

    def handle(self):
        print("Got connection from ",self.client_address)
        msg,sock = self.request
        print(msg)
        time.sleep(5)
        resp = time.ctime()
        sock.sendto(msg,self.client_address)


if __name__ == '__main__':
    #虽然说Udp服务器与Tcp服务器简单形式都是一次只能为一个客户端连接服务。但两者之间是有较大区别的，
    #Udp服务器在收发数据前不需要交换控制信息，故不需建立和断开连接步骤，也就意味着一个请求发送到Udp
    #服务器，服务器端执行完成后就直接释放线程即可以接收其他Udp请求，而不需要客户端发送close信号，服务器端
    # 必须指定对应的客户端地址才能反馈。
    #而Tcp服务器需要建立和断开连接步骤，所以首先会与客户端进行连接绑定，在绑定未解除期间(即没有接到客户端发来
    #的close信号期间 )一直是被该客户端连接占用的。
    #所以 udp更直接粗暴，tcp则显得细腻精致

    serv = UDPServer(('',20000),TimeHandler)#一次只能为一个客户端连接服务。
    serv.serve_forever()