FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN rm requirements.txt

RUN addgroup --system --gid 1001 container
RUN adduser --system --uid 1001 user
USER user

COPY --chown=user:container main.py .

ENV HOST=0.0.0.0
ENV PORT=8000
ENV EXTRA_ARGS=

CMD uvicorn main:app --host $HOST --port $PORT $EXTRA_ARGS
