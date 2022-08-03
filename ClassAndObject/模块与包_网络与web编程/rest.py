
import cgi


_hello_resp ='''\
<html>
    <head>
        <title>Hello {name}</title>
    </head>
    <body>
        <h1>Hello {name}!</h1>
    </body>
</html>
'''

def hello_world(environ,start_response):#WSGI标准就是约束 handler具体函数的形式，需要接收 environ与返回 response
    start_response('200 OK',[('Content-type','text/html')])
    params = environ['params']
    resp = _hello_resp.format(name=params.get('name'))
    yield resp.encode('utf-8')



def notfound_404(environ,start_response):
    start_response("404 Not Found",[("Content-type","text/plain")])
    return [b'Not Found']

def wsgi_app(environ,start_response):
    start_response('200 OK', [('Content-type', 'text/html')])
    yield b'Goodbye!\n'
#成熟的框架比如django,flask都已经将 server与app之间的交互即dispather之类的设置好了。若
#不想用框架，则自己找个 服务器，再搭个架子即 调度器(dispather)将 服务器与自己的app连接起来。
#但app即应用要符合WSGI标准

#符合WSGI标准，即 服务器与应用之间的交互标准，其实WSGI很重要的一点在于它没有什么地方
#是针对特定web服务器的。因标准对于服务器和框架是中立的，只要是符合该标准的app(即标准是针对app的)，
# 你可以将你的程序放入任何类型服务器中。(这在网络编程模型中处于  reactor中的dispather的尾部)
#即解耦 服务器、调度器、应用 3部分，应用只需注册到调度器中即可，调度器也只需放置到服务器中即可
class PathDispatcher:
    #该类目的是管理 pathmap字典，将(方法，路径)对 映射到处理器函数上。
    def __init__(self):
        self.pathmap = {}

    def __call__(self, environ, start_response):#由server来调用并传入 environ,start_response
        path = environ['PATH_INFO']
        method = environ['REQUEST_METHOD'].lower()#path与method用于定位哪个处理函数

        params = cgi.FieldStorage(environ['wsgi.input'],#请求携带的 参数
                                  environ=environ)

        environ['params'] = {key: params.getvalue(key) for key in params}#重新组织 参数，方便对应处理器提取
        handler = self.pathmap.get((method,path),notfound_404)
        return handler(environ,start_response)#调用对应的 handler

    def register(self,method,path,function):
        self.pathmap[method.lower(),path] = function
        return function


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    #其实不必要用 分派器，直接将符合 WSGI的handler函数传入即可。
    #dispather的作用就是统筹分配 指向多个handler函数。

    dispatcher = PathDispatcher()
    dispatcher.register('GET','/hello',hello_world)#所谓注册，就是保存在字典中
    httpd = make_server('',8080,wsgi_app)
    print("Serving on port 8080...")
    httpd.serve_forever()
