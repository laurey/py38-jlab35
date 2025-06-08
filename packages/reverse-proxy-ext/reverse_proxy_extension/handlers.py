# my_jupyterlab_proxy_plugin/proxy_handler.py
from jupyter_server.utils import url_path_join
from jupyter_server.base.handlers import JupyterHandler, APIHandler
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.web import RequestHandler
import tornado
import json

class RouteHandler(APIHandler):
    # The following decorator should be present on all verb methods (head, get, post,
    # patch, put, delete, options) to ensure only authorized user can request the
    # Jupyter server
    @tornado.web.authenticated
    def get(self):
        self.finish(json.dumps({"data": "This is /jlab-ext-example/hello endpoint!"}))

    @tornado.web.authenticated
    def post(self):
        # input_data is a dictionary with a key "name"
        input_data = self.get_json_body()
        data = {"greetings": "Hello {}, enjoy JupyterLab!".format(input_data["name"])}
        self.finish(json.dumps(data))


class ProxyHandler(JupyterHandler):
    @tornado.web.authenticated
    async def get(self, path):
        """
        处理 GET 请求并将其代理到目标服务
        """
        target_url = f"https://jsonplaceholder.typicode.com/{path}"  # 目标 API URL
        http_client = AsyncHTTPClient()

        try:
            request = HTTPRequest(target_url, method="GET")
            response = await http_client.fetch(request)

            # 设置响应状态和头
            self.set_status(response.code)
            self.set_header("Content-Type", "application/json")

            # 返回代理的数据
            self.finish(response.body)

        except Exception as e:
            self.set_status(500)
            self.finish({"error": f"Failed to proxy request: {str(e)}"})

    @tornado.web.authenticated
    async def post(self, path):
        """
        处理 POST 请求并将其代理到目标服务
        """
        target_url = f"https://jsonplaceholder.typicode.com/{path}"  # 目标 API URL
        http_client = AsyncHTTPClient()

        try:
            body = self.request.body
            request = HTTPRequest(target_url, method="POST", body=body)
            response = await http_client.fetch(request)

            # 设置响应状态和头
            self.set_status(response.code)
            self.set_header("Content-Type", "application/json")

            # 返回代理的数据
            self.finish(response.body)

        except Exception as e:
            self.set_status(500)
            self.finish({"error": f"Failed to proxy request: {str(e)}"})


def setup_handlers(web_app, url_prefix):
     """
     将代理处理程序添加到 JupyterServer 的 URL 路由中
     """
     # handlers = [
     #     (r"/proxy/(.*)", ProxyHandler),  # 配置代理的路由路径
     # ]
     #web_app.settings['handlers'] = handlers

     host_pattern = ".*$"
    
     base_url = web_app.settings["base_url"]
     route_pattern = url_path_join(base_url, url_prefix, "hello")
     handlers = [
         (r"/proxy/(.*)", ProxyHandler),  # 配置代理的路由路径
         (route_pattern, RouteHandler)
     ]
     print("========base-url========", base_url)
     print("========r-url========", route_pattern)
     web_app.add_handlers(host_pattern, handlers) 
