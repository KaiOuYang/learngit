

from urllib import request,parse



def urllib_action():
    url_pre = "http://httpbin.org"
    method = lambda x : "get" if x == "g" else "post"
    parms = {
        "name1":"value1",
        "name2":"value2"
    }
    querystring = parse.urlencode(parms)
    #urllib是http客户端的基本内置库，对于简单的GET、POST请求访问HTTP服务端 urllib库就够用了。
    u_get = request.urlopen(parse.urljoin(url_pre,method("g"))+"?"+querystring)
    u_post = request.urlopen(parse.urljoin(url_pre,method("p")),querystring.encode('ascii'))#表单传递的data必须是二进制形式
    resp_p = u_post.read()
    resp_g = u_get.read()
    print(resp_p)
    print(resp_g)


def requests_action():
    import requests
    # 若交互的服务比较复杂，那就用第三方库 requests库，该库有更多高级功能 验证登录等等
    #明显的可以看到，urllib.request中的method都是直接放置在url中的，而requests中，
    #就将method作为了一个个属性方法
    url ='http://httpbin.org/post'
    parms ={
        'name1':'value1',
        'name2':'value2'
    }

    headers ={
        'User-agent':'none/ofyourbusiness',
        'Spam':'Eggs'
    }

    #其次，requests能将返回回来的响应resp转化为多种格式，包库Unicode解码文本(.text)、原始二进制数据(.content)、json格式(.json)
    #而 urllib.request返回的只是二进制类型
    resp = requests.post(url,data=parms,headers=headers)
    print(resp.content)
    text = resp.text
    print(text)






if __name__ == '__main__':
    requests_action()
