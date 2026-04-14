import lichtfeld as lf
from .panels.main_panel import PluginManagerPanel

_classes = [PluginManagerPanel]

def on_load():
    for cls in _classes:
        lf.register_class(cls)
    lf.log.info("plugin_manager loaded")

def on_unload():
    for cls in reversed(_classes):
        lf.unregister_class(cls)
    lf.log.info("plugin_manager unloaded")