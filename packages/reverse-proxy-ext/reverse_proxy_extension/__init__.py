import json
from pathlib import Path

from .handlers import setup_handlers
from ._version import __version__

def _jupyter_server_extension_points():
    return [{"module": "reverse_proxy_extension"}]

def _jupyter_server_extension_paths():
    return [{"module": "reverse_proxy_extension"}]

def _load_jupyter_server_extension(server_app):
    """Registers the API handler to receive HTTP requests from the frontend extension.
    Parameters
    ----------
    server_app: jupyterlab.labapp.LabApp
        JupyterLab application instance
    """
    url_path = "jlab_api"
    setup_handlers(server_app.web_app, url_path)
    server_app.log.info(
        f"Registered jlab_reverse_proxy extension at URL path /{url_path}"
    )

# For backward compatibility with the classical notebook
load_jupyter_server_extension = _load_jupyter_server_extension
