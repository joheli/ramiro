import marimo
import os
import glob
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import importlib

# Directory where marimo notebooks are stored
NOTEBOOKS_DIR = "notebooks"

# Directory where additional routers can be places
ROUTERS_DIR = "routers"

# create a api that serves marimo notebooks
server = marimo.create_asgi_app()

# variable holding routes to notebooks
notebook_routes = []

# purely cosmetic: path to jinja2 template specifying html returned under route ('/'), 
# see landing page below
templates = Jinja2Templates(directory="templates")

# Assume that NOTEBOOKS_DIR either does not correspond to a directory or that it 
# does not contain marimo apps (i.e. *.py files)
app_directory = False

# First check whether NOTEBOOKS_DIR exists and whether python files are in it at all
if (
    os.path.isdir(NOTEBOOKS_DIR)
    and len(glob.glob(os.path.join(NOTEBOOKS_DIR, "*.py"))) > 0
):
    # if satisfactory, i.e. condition met, change app_directory to True
    app_directory = True
    # Dynamically discover all .py notebooks in the notebooks directory
    for filename in os.listdir(NOTEBOOKS_DIR):
        # only consider python files 
        # (assuming here that those are in fact are marimo apps, which presently is not checked, maybe a later todo)
        if filename.endswith(".py"):
            # cosmetic: separate the name part without the ending
            filename_noending = os.path.splitext(filename)[0]
            # create a route by prepending a forward slash '/'
            # note that the actual route has an additional '/apps' prepended, see below
            route = "/" + filename_noending
            # determine the path referring to the marimo notebook
            notebook_path = os.path.join(NOTEBOOKS_DIR, filename)
            # add this path to the server under the specified route
            server = server.with_app(path=route, root=notebook_path)
            # save the route and filename (without ending) in a list of tuples
            notebook_routes.append((route, filename_noending))

# create a fastapi app
app = FastAPI()

# add additional routes, if present in folder ROUTERS_DIR
for filename in os.listdir(ROUTERS_DIR):
    if filename.endswith(".py") and filename != "__init__.py":
        modulename = filename[:-3]
        module_path = f"{ROUTERS_DIR}.{modulename}"
        try:
            # Import the module dynamically
            module = importlib.import_module(module_path)
            # Expect the router to be named "router" in each module
            app.include_router(getattr(module, "router"))
        except (ImportError, AttributeError) as e:
            print(f"Skipping {modulename}: {e}")

# as stated above, marimo apps are served under base route '/apps' even though
# routes start with '/'
app.mount("/apps", server.build())


# landing page under route '/'
# The template accomodates for unsatisfactory NOTEBOOKS_DIR checks, see above, by providing a help message (if app_directory == False)
@app.get("/", response_class=HTMLResponse)
async def list_apps(request: Request):
    # provide context for the jinja2 template
    context = {
        "request": request,
        "app_directory": app_directory,
        "notebook_routes": notebook_routes,
        "help": "No apps found.",
    }
    # return html served as landing page
    return templates.TemplateResponse("template.html", context=context)
