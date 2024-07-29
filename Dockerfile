# syntax=docker/dockerfile:1

FROM ubuntu:22.04
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]

EXPOSE 5001

CMD [ "app.py"]