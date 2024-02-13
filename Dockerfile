FROM python:3.12 as builder

COPY requirements.txt /
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt

FROM python:3.12

ENV HOME=/home/app
ENV APP_HOME=/home/app/web

RUN mkdir -p /home/app && \
    groupadd app && useradd -g app app && \
    mkdir $APP_HOME

WORKDIR $APP_HOME

COPY --from=builder /wheels /wheels
COPY --from=builder requirements.txt .
RUN pip install --no-cache /wheels/*

COPY . $APP_HOME

RUN chown -R app:app $APP_HOME
USER app

ENV SERVER__PORT=$SERVER__PORT

EXPOSE $SERVER__PORT
ENTRYPOINT ["python", "-m", "agibot"]

CMD ["run"]
