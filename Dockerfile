FROM node:18-alpine AS build

WORKDIR /app

RUN npm install -g pnpm
COPY package.json .
COPY pnpm-lock.yaml .
RUN pnpm install --frozen-lockfile
COPY tsconfig.json .
COPY public public
COPY src src
RUN pnpm build

FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN rm requirements.txt

RUN addgroup --system --gid 1001 container
RUN adduser --system --uid 1001 user
USER user

COPY --chown=user:container --from=build /app/build ./build
COPY --chown=user:container main.py .
COPY --chown=user:container api api
COPY --chown=user:container model.pkl .

RUN prisma generate

ENV HOST=0.0.0.0
ENV PORT=8000
ENV EXTRA_ARGS=

CMD prisma db push && uvicorn main:app --host $HOST --port $PORT $EXTRA_ARGS
