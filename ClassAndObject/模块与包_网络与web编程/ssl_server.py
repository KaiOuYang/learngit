

from socket import socket,AF_INET,SOCK_STREAM

import ssl

KEYFILE = 'server_key.pem'
CERTFILE = 'server_cert.pem'


def echo_client(s):
    while True:
        data = s.recv(8192)
        if data == b'':
            break
        s.send(data)
    s.close()
    print('Connection closed')

def echo_server(address):
    s = socket(AF_INET,SOCK_STREAM)
    s.bind(address)
    s.listen(1)

    s_ssl = ssl.wrap_socket(s,#ssl模块能直接在底层为 socket添加ssl的支持，只需将socket包裹一层 ssl.wrap_socket即可
                            keyfile=KEYFILE, #私钥
                            certfile=CERTFILE,#公钥，由server发送给 client的 公钥
                            server_side=True)
    while True:
        try:

            c,a = s_ssl.accept()#经过ssl包裹的socket将会 对客户端发来的请求用私钥做非对称性解密，若不通过则
            print('Got connection',c,a)
            echo_client(c)
        except Exception as e:
            print('{}:{}'.format(e.__class__.__name__,e))


if __name__ == '__main__':
    print('listen port 20000...')
    echo_server(('',20000))