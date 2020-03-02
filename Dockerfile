FROM python:3.7

ADD encoder_decoder.py /

CMD ["-v", "-t", "Example string"]

ENTRYPOINT ["python3", "/encoder_decoder.py"]
