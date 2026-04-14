import os
import tomllib
import lichtfeld as lf

THIS_PLUGIN = "plugin_manager"

def _discover_plugins():
    plugins_dir = os.path.expandvars(r"%USERPROFILE%\.lichtfeld\plugins")
    results = []
    if not os.path.isdir(plugins_dir):
        return results
    for entry in os.scandir(plugins_dir):
        if not entry.is_dir():
            continue
        toml_path = os.path.join(entry.path, "pyproject.toml")
        if not os.path.exists(toml_path):
            continue
        try:
            with open(toml_path, "rb") as f:
                data = tomllib.load(f)
            name = data.get("project", {}).get("name", "")
            if name and name != THIS_PLUGIN:
                results.append(name)
        except Exception:
            pass
    return sorted(results)

def _is_loaded(name):
    """Use list_loaded() to check if a plugin is active."""
    try:
        loaded = lf.plugins.list_loaded()  # returns a list of plugin name strings
        return name in loaded
    except Exception as e:
        lf.log.error(f"list_loaded() failed: {e}")
        return False

def _get_state_str(name):
    """Get a readable state string for diagnostics."""
    try:
        state = lf.plugins.get_state(name)
        return str(state)
    except Exception as e:
        return f"unknown ({e})"


class PluginManagerPanel(lf.ui.Panel):
    id = "plugin_manager.main"
    label = "P-on/off"
    space = lf.ui.PanelSpace.MAIN_PANEL_TAB
    order = 0

    def draw(self, ui):
        plugins = _discover_plugins()

        if not plugins:
            ui.label("No plugins found.")
            return

        ui.label("Installed Plugins")
        ui.separator()

        for name in plugins:
            loaded = _is_loaded(name)
            status = "● ON " if loaded else "○ OFF"

            if ui.button(f"{status}  {name}"):
                lf.log.info(f"Button pressed: {name}, currently loaded={loaded}, state={_get_state_str(name)}")
                try:
                    if loaded:
                        lf.plugins.unload(name)
                        lf.log.info(f"Unloaded: {name}")
                    else:
                        lf.plugins.load(name)
                        lf.log.info(f"Loaded: {name}")
                except Exception as e:
                    lf.log.error(f"Toggle failed for {name}: {e}")