FROM python:3.11-slim

RUN pip install pandas numpy matplotlib seaborn scikit-learn scipy requests

WORKDIR /app/pipeline/

COPY . /app/pipeline/

CMD [ "bash" ]