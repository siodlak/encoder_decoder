FROM python:3.7

ADD encoder_decoder.py /

CMD ["-t", "String testowy", "-v"]

ENTRYPOINT ["python3", "/encoder_decoder.py"]
