FROM python:3.14-slim

# install system packages needed for pip git+https://... dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
 && rm -rf /var/lib/apt/lists/*

# create non-root user app
RUN useradd -m -d /app -s /bin/bash app

# app directory
WORKDIR /app

# copy dependency manifests first for better layer caching
COPY requirements.txt /app/requirements.txt
COPY whl /app/whl

# make app directory writable by the app user
RUN chown -R app:app /app

# switch to non-root user before pip --user installs
USER app

# install Python dependencies
RUN pip install --user --no-cache-dir -r requirements.txt

# install local wheel packages
RUN ls whl/*.whl 2>/dev/null && pip install --user --no-cache-dir whl/*.whl || echo "No wheels to install found."

# create convenience reload and install scripts
WORKDIR /app/.local/bin
RUN printf '#!/bin/bash\nuvicorn main:app --reload &\n' > reload; \
    chmod u+x reload; \
    printf '#!/bin/bash\npip install --user --no-cache-dir "$@"\n' > pippin; \
    chmod u+x pippin

# add .local/bin to PATH
ENV PATH="/app/.local/bin:$PATH"

# return to app dir
WORKDIR /app

# now copy the rest of the application code
COPY --chown=app:app main.py /app/main.py
COPY --chown=app:app routers /app/routers
COPY --chown=app:app notebooks /app/notebooks
COPY --chown=app:app templates /app/templates

# serve on port 9000
EXPOSE 9000

# start uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]