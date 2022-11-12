FROM python:3.10

RUN mkdir -p /usr/src/pdfpad
WORKDIR /usr/src/pdfpad

COPY . /usr/src/pdfpad

RUN apt-get update -y && apt-get install poppler-utils -y
RUN python -m pip install --upgrade pip --no-cache-dir
RUN pip install -e . --no-cache-dir
RUN pip install -r web/web-requirements.txt --no-cache-dir

EXPOSE 7575

CMD ["uvicorn", "web:app", "--host", "0.0.0.0", "--port", "7575"]