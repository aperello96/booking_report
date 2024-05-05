#FROM python:3.9-alpine
FROM ubuntu:20.04
#FROM arm64v8/ubuntu:20.04

# Instala el instalador de paquetes pip y cron
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y python3 python3-pip

# Instala las librerias python necesarias
RUN pip3 install --no-cache-dir python-dotenv schedule requests pandas

# Copia los ficheros necesarios
COPY ./main.py /main.py

# Damos permisos a los ficheros y aplicamos mycron a crontab
RUN chmod 7777 main.py

# Start program
CMD ["python3", "/main.py"]
