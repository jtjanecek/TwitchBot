from TriviaPlugin import TriviaPlugin
from ExamplePlugin import ExamplePlugin

def initialize_plugins() -> list:
    # Plugins list. Append custom plugins here.
    plugins = []
    plugins.append(TriviaPlugin())
    plugins.append(ExamplePlugin())
    return plugins
