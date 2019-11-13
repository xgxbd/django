# 从 django.http 模块中导入 HttpRespose
import json

from django.http import HttpResponse, JsonResponse
# 1.查询字符串传参
from django.shortcuts import redirect


# Create your views here.
from django.views import View


def index(request):
    """
    index视图
    :param request: 包含了请求信息的请求对象
    :return: 响应对象
    """

    print(request.get_full_path())  # /user1/index/?a=1&b=2&a=3
    print(request.GET.get("a"))  # 3
    print(request.GET.get("b"))  # 2
    print(request.GET.getlist("a"))  # [1, 3]

    return HttpResponse("hello the world!")


# 2.路径传参
def weather(request, city, year):
    print("city = ", city)
    print("year = ", year)

    return HttpResponse("天气信息已接收")


# 3.请求体传参
def get_body(request):
    a = request.POST.get("a")
    b = request.POST.get("b")
    c = request.POST.getlist("a")

    print(a)
    print(b)
    print(c)

    return HttpResponse("就收到了")


# 4.请求体非表单形式传参
def no_form(request):
    # 获得请求体
    request_bytes = request.body
    # 对请求数据解码成字符串
    request_str = request_bytes.decode()
    # 字符串转成json格式
    request_data = json.loads(request_str)

    print(request_data["a"])
    print(request_data["b"])

    return HttpResponse("返回数据")


# 请求体其他信息
def information(request):
    print(request.method)  # GET
    print(request.user)  # AnonymousUser   # 匿名用户
    print(request.path)  # /information    # 请求资源路径
    print(request.encoding)  # None
    print(request.FILES)  # <MultiValueDict: {}>

    response = ["fhoehohg", "heoghhe", 100, (190,)]

    return JsonResponse(response, safe=False)  # 默认safe = true， 不允许非字典类型的数据转成json


# 跳转路径
def page(request):
    # return HttpResponse('<img src=http://img.mp.itc.cn/q_70,c_zoom,w_640/upload/20161122/f49596398ade438585111da031b9a4db_th.jpg>')

    return redirect("/information") # 他会直接到urls.py文件中去找匹配的正则，不需要重新写 ./urls


# 设置和获取cookie
def mark(request):

    response = HttpResponse()

    response.set_cookie('name', 'python', max_age= 3600 * 24 * 14)

    value = request.COOKIES.get("name")
    print(value)

    return response    # 直接把返回对象返回即可


# 操作session
def mark1(request):

    request.session['name'] = "python"
    print(request.session.get("name"))
    # request.session.set_expiry(3600 * 24 * 14)

    # return HttpResponse(request.session)   # 直接把返回对象返回即可
    return HttpResponse("hao")



# 我们自定义的装饰器:
def my_decorator_1(func):
    def wrapper(request, *args, **kwargs):    # 不能自己添加self
        print('自定义装饰器被调用了')
        print('请求路径%s' % request.path)
        return func(request, *args, **kwargs) # 8. # 4. 这里的func是as_view 函数中内层函数 view函数的地址
    return wrapper                                 # 5. Mixin 扩展类 as_view 函数返回wrapper

# 11. 真正执行get函数的是 dispatch函数中 handler(request, *args, **kwargs),handler就是请求的类型（get）在类视图中地址
class FirstMixin(object):   # 但这句代码要等view()被调用才执行
    """ FirstMixin 扩展类 """
    @classmethod                               # 1. 调用as_view把类对象传入了，函数中的cls和self都是它
    def as_view(cls, *args, **kwargs):         # 10. dispatch函数中返回 return handler(request, *args, **kwargs),
        view = super().as_view(*args, **kwargs)# 2. view 返回的是父类 as_view 函数中内层函数 view函数的地址
        view = my_decorator_1(view)            # 9. view 函数中返回 return self.dispatch(request, *args, **kwargs)
        return view                            # 6. 返回的是wapper，装饰器内层函数的地址

class DemoView(FirstMixin, View):   # url(r'^DemoView$', views.DemoView.as_view()), 调用的是DemoView的as_view()方法
    def get(self, request):         # DemoView中没有这方法，但他的父类中有，所以先执行父类，遇到super。as_view()
        print('demoview get')       # 跳到 View 中 as_view()中执行
        return HttpResponse('demoview get')

    def post(self, request):
        print('demoview post')
        return HttpResponse('demoview post')


