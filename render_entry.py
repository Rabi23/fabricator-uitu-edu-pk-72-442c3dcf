import importlib.util
import os

from bootstrap_render import ensure_connected_export_ready


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ensure_connected_export_ready()
backend_path = os.path.join(BASE_DIR, "admin_system", "backend", "app.py")
spec = importlib.util.spec_from_file_location("fabricator_render_backend", backend_path)
module = importlib.util.module_from_spec(spec)
if spec.loader is None:
    raise RuntimeError("Unable to load exported backend app for deployment.")
spec.loader.exec_module(module)
app = module.app
