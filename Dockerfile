FROM python:2
ADD server.py /
WORKDIR /data
EXPOSE 8080
CMD [ "python", "../server.py" ]