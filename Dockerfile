FROM python:3.8

RUN python -m pip install poetry
COPY poetry.lock /app/poetry.lock
COPY pyproject.toml /app/pyproject.toml

WORKDIR /app
RUN poetry config virtualenvs.create false &&\
    poetry install --no-dev &&\
    rm -rf ~/.cache

COPY . .
RUN ls
CMD streamlit run ./app.py --server.port ${PORT}

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
RUN mkdir -p /root/.streamlit
RUN bash -c 'echo -e "\
[general]\n\
email = \"\"\n\
" > /root/.streamlit/credentials.toml'
