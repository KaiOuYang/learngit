


from socket import socket,AF_INET,SOCK_STREAM
import hmac
import os

#简洁说，s端等待c端建立连接后，发送文本并等待c端密文反馈后进行本地校验，判断是否通过。
# 所以鉴权是由s端进行，c端需要建立连接后进行配合。

def client_authenticate(connection,secret_key):

    message = connection.recv(32)#等待
    hash = hmac.new(secret_key,message)
    digest = hash.digest()
    connection.send(digest)#反馈鉴权信息

if __name__ == '__main__':
    secret_key = b'peekaboo'
    s = socket(AF_INET,SOCK_STREAM)
    s.connect(('localhost',18000))
    client_authenticate(s,secret_key)
    s.send(b'Hello yk')
    resp = s.recv(1024)
    print(resp)