FROM python:3.13-slim

# change dir
WORKDIR /app

# copy files and folders
COPY main.py /app/main.py
COPY requirements.txt /app/requirements.txt
COPY whl /app/whl
COPY routers /app/routers
COPY notebooks /app/notebooks
COPY templates /app/templates

# create non-root user app
RUN useradd -m -d /app -s /bin/bash app; \
    chown -R app:app /app
USER app

# install packages listed in requirements.xt
RUN pip install --user --no-cache-dir -r requirements.txt

# install wheels packages placed in directory /app/whl
RUN ls whl/*.whl 2>/dev/null && pip install --user --no-cache-dir whl/*.whl || echo "No wheels to install found."

# create convenience reload and install scripts
WORKDIR .local/bin
RUN printf "#!/bin/bash\nuvicorn main:app --reload &" > reload; \
    chmod u+x reload; \ 
    printf '#!/bin/bash\npip install --user --no-cache-dir "$@"' > pippin; \
    chmod u+x pippin; 

# add .local/bin to PATH
ENV PATH="/app/.local/bin:$PATH"

# cd back to /app
WORKDIR ../.. 

# serve on port 9000
EXPOSE 9000

# Start uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]
