FROM nvcr.io/nvidia/pytorch:25.01-py3

WORKDIR /app

COPY call.py /app/call.py 
COPY pytorch_calculation.py /app/pytorch_calculation.py 

ENTRYPOINT ["python", "/app/pytorch_calculation.py"]
