from socket import socket,AF_INET,SOCK_STREAM

import hmac
import os


#明显是 对称性加密认证，双方都知道同一个密钥，用同一个密钥结合随机文本生成鉴权密文
#client与server端都已预置同样的密钥，server先启动等待，client随后与server建立连接后等待server发送鉴权信息(在server_authenticate模块)，
# server随后随机生成文本发送给正在等待的client，并自身开始根据密钥生成密文，随后与client反馈回来密文相比较确认
# 鉴权是否成功，若成功则双方建立信任开始明文通信。若失败，则直接断开连接。


#服务器的用法与 RPC服务器的用法基本一致，即server中做好连接建立，将连接委托给处理器，处理器进行鉴权以及业务逻辑

def server_authenticate(connection,secret_key):
    message = os.urandom(32)
    connection.send(message)
    hash = hmac.new(secret_key,message)
    digest = hash.digest()
    response = connection.recv(len(digest))
    return hmac.compare_digest(digest,response)

secret_key = b'peekaboo'

def echo_handler(client_sock):
    if not server_authenticate(client_sock,secret_key):
        client_sock.close()
        return
    print("通过验证...")
    while True:
        msg = client_sock.recv(8192)
        print("服务端接收到信息: ")
        print( msg)
        if not msg:
            break
        client_sock.sendall(msg)


def echo_server(address):
    s = socket(AF_INET,SOCK_STREAM)
    s.bind(address)
    s.listen(5)
    while True:
        c,a = s.accept()
        echo_handler(c)

if __name__ == '__main__':
    print("listen 18000...")
    echo_server(('',18000))