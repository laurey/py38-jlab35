# my_jupyterlab_proxy_plugin/setup.py
# from jupyter_server.extension.application import ExtensionApp
# from jupyter_server.base.handlers import JupyterHandler
# from tornado.web import URLSpec
# from .proxy_handler import ProxyHandler

# def setup_handlers(web_app, url_prefix):
#     """
#     将代理处理程序添加到 JupyterServer 的 URL 路由中
#     """
#     handlers = [
#         (r"/proxy/(.*)", ProxyHandler),  # 配置代理的路由路径
#     ]
#     web_app.settings['handlers'] = handlers


# class ProxyExtensionApp(ExtensionApp):
#     """
#     JupyterLab 扩展应用，注册代理服务
#      """
#    def initialize(self):
#        self.log.info("Initializing Proxy Extension")
#        setup_handlers(self.web_app, self.url_prefix)


# 在服务器启动时自动调用此类
#def load_jupyter_server_extension(nbapp):
#    nbapp.log.info("Loading Proxy Extension")
#    ProxyExtensionApp.instance().initialize()

import json
import os
from pathlib import Path
from setuptools import setup, find_packages
from jupyter_packaging import npm_builder, get_data_files, wrap_installers, create_cmdclass

HERE = Path(__file__).parent.resolve()

long_description = (HERE / "README.md").read_text()

# Get the package info from package.json
pkg_json = json.loads((HERE / "package.json").read_bytes())

def _get_data_files():
    """Get the data files for the package."""
    data_files = [
        ("etc/jupyter/jupyter_server_config.d", "jupyter-config/", "*.json"),
    ]

    def add_data_files(path):
        for (dirpath, dirnames, filenames) in os.walk(path):
            if filenames:
                paths = [(dirpath, dirpath, filename) for filename in filenames]
                data_files.extend(paths)

    # Add all static and templates folders.
    return data_files


name="reverse_proxy_extension"

data_files_spec=[
    ("etc/jupyter/jupyter_server_config.d", "jupyter-config/server-config", "*.json"),
    # For backward compatibility with notebook server
    ("etc/jupyter/jupyter_notebook_config.d", "jupyter-config/nb-config", "*.json"),
]

setup_args = dict(
    name=name,
    version=pkg_json["version"],
    description=pkg_json["description"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
    install_requires=[
        "jupyter_server>=2.0.0,<3",
        "tornado>=5.0.0"
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    package_data={
         "reverse_proxy_extension": ["*.py", "*.json"]
    },
    # data_files=data_files_spec,
    entry_points={
        "console_scripts": [],
	'jupyter_serverproxy_servers': [
            'reverse_proxy_extension = reverse_proxy_extension'
        ]
    },
    platforms="Linux, Mac OS X, Windows",
    keywords=["Jupyter", "JupyterLab", "JupyterLab3"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Framework :: Jupyter",
    ],
)


if __name__ == "__main__":
    setup(**setup_args)
