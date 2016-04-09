from TriviaPlugin import TriviaPlugin
from ExamplePlugin import ExamplePlugin
import os
import sys

def initialize_plugins() -> list:
    # Plugins list. Append custom plugins here.
    plugin_names = next(os.walk(str(os.path.dirname(__file__))))[1]
    try:
        plugin_names.remove("__pycache__")
    except:
        pass

    plugins = []
    for plugin in plugin_names:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__),plugin))
        exec(("from " + plugin + " import " + plugin))
        plugins.append(eval(plugin + "." + plugin + "()"))

    return plugins
