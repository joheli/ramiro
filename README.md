# Ramiro

`ramiro` is a dockerized server for [marimo](https://marimo.io/) notebooks based on [fastapi](https://fastapi.tiangolo.com/).
The images are available under [packages](https://github.com/joheli/ramiro/pkgs/container/ramiro). Pull the latest image via 
docker command `docker pull ghcr.io/joheli/ramiro:latest`.

## Start rollin'

Spin up a docker container using the image provided with a volume (folder) containing your marimo notebooks and you should be good to go. 
Please note that the volume should be mapped to `/app/notebooks` in the container.

E.g.

```
docker run --name ramiro -v /your/path/to/marimo_notebooks:/app/notebooks -p 9000:9000 ghcr.io/joheli/ramiro:latest
```

If you have started this on your own computer, you can now access the landing page under `http://localhost:9000`.

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

## Reload the server

The files are served with [uvicorn](https://www.uvicorn.org/). To reload uvicorn in the container, enter the container as above. Then, type

```
# long command
uvicorn main:app --reload

# alternatively, use convenience script "reload"
reload
```

Have fun!