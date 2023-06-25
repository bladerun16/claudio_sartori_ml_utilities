""" produced by ChatGPT with the prompt 
 'how can I import into python a script from a github repository, if the package 
  is not published, without cloning the repository?'
"""
import importlib.util
import requests
import sys

def remote_import(script_url, module_name, to_import = True):
    """
    remote_import - Import a .py script into the current session
                    It can be used to import a file stored on a public
                    GitHub project
    parameters:
    - script_url  : complete url of the script. 
                    For GitHub
                    'https://raw.githubusercontent.com/<githubusername>/<projectname>/main/<pathname>'
    - module_name : name of the module
    - to_import   : if True it imports the module, otherwise the module will be available for import, 
                    default True
    """

    # Fetch the contents of the script file
    response = requests.get(script_url)
    script_code = response.text

    # Create a module specification
    spec = importlib.util.spec_from_loader(module_name, loader=None, origin=script_url)

    # Create a module from the specification
    module = importlib.util.module_from_spec(spec)

    # Set the script code as the module's source code
    exec(script_code, module.__dict__)

    # Register the module in sys.modules
    sys.modules[module_name] = module
    if to_import:
        import importlib
        module = importlib.import_module(module_name, package=None)
        return "Module '{}' imported\n".format(module_name)
    return "Module {} available for import\n".format(module_name)
