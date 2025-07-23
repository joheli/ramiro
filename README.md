[![Build and Publish Docker Image](https://github.com/joheli/ramiro/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/joheli/ramiro/actions/workflows/docker-publish.yml)
# Ramiro

`ramiro` is a dockerized server for [marimo](https://marimo.io/) notebooks based on [FastAPI](https://fastapi.tiangolo.com/).
The images are available under [packages](https://github.com/joheli/ramiro/pkgs/container/ramiro). Pull the latest image via 
docker command `docker pull ghcr.io/joheli/ramiro:latest`.

## Start rollin'

Spin up a docker container using the image provided with a volume (folder) containing your marimo notebooks and you should be good to go. 
Please note that the volume should be mapped to `/app/notebooks` in the container.

E.g.

```
docker run --name ramiro -v /your/path/to/marimo_notebooks:/app/notebooks -p 9000:9000 ghcr.io/joheli/ramiro:latest
```

If you have entered this on your own computer, you should now be able to access the landing page under `http://localhost:9000`.

## Install python packages

You can either rebuild the image with a fresh `requirements.txt` file or add packages after build into the container.

To add packages into the container proceed as follows:

```
# Enter the container with user "app"
docker exec -it --user app ramiro bash

# once inside the container, add package XXX by typing
pip install --user --no-cache-dir XXX

# alternatively, use convenience script "pippin"
pippin XXX
```

> [!TIP]
> If you don't wish to reinstall all python packages every time you restart the container, how about persisting `/app/.local` to a volume? How, you ask? Simple: just add `-v ramiro_local:/app/.local` to above "docker run" command! Now all changes in `/app/.local` are persisted to named volume `ramiro_local`. (You can obviously change the name of the named volume or mount an existing folder as well.)

## Add route(r)s to FastAPI

You can add route(r)s to the FastAPI container. A bit of disambiguation: a _route_ is an API endpoint, a _router_ specifies different _routes_ and is of type `fastapi.APIRouter`. 
To add additional endpoint "hello", create a file called `hello.py` with the following contents:

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/hello")
async def say_hello():
    return {"message": "Hello!"}
```

Now put file `hello.py` into a folder that you bind as a volume to the container by adding `-v /your/router/folder:/app/routers` to above "docker run" command.

> [!IMPORTANT]
> Please only specify routes that have not been used yet! Just as a reminder: `/` and `/apps` are already taken, see [main.py](main.py), so add different endpoints!

> [!CAUTION]
> Please only connect folders containing trusted routes and python code!

## Reload the server

The files are served with [uvicorn](https://www.uvicorn.org/). To reload uvicorn in the container, enter the container as above. Then, type

```
# long command
uvicorn main:app --reload

# alternatively, use convenience script "reload"
reload
```

Have fun!