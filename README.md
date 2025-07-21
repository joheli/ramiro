# Ramiro

`ramiro` is a dockerized server for [marimo](https://marimo.io/) notebooks based on [fastapi](https://fastapi.tiangolo.com/).

## Start rollin'

Spin up a docker container using the image provided with a volume (folder) containing your marimo notebooks and you should be good to go.

E.g.

```
docker run --name ramiro --volume /your/path/to/marimo_notebooks:/notebooks ramiro:XX
```

## Install python packages

You can either rebuild the image with a fresh `requirements.txt` file or add packages after build into the container.

E.g. 

```
# Enter the container with user "app"
docker exec -it --user app ramiro bash

# once inside the container, add package XXX by typing
pip install --user --no-cache-dir XXX

# alternatively, use convenience script "pippin"
pippin XXX
```

## Reload the server

The files are served with [uvicorn](https://www.uvicorn.org/). To reload, enter the container as above. Then, type

```
# long command
uvicorn main:app --reload

# alternatively, use convenience script "reload"
reload
```

Have fun!