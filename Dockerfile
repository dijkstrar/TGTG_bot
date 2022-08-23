FROM python:3-alpine


WORKDIR tgtg
COPY requirements.txt ./
RUN apk add --no-cache gcc musl-dev curl bash && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN ["chmod", "+x", "bot/docker_entrypoint.sh"]

CMD  ["sh","bot/docker_entrypoint.sh"]