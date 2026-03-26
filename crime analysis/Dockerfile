# FROM python:3.11-slim

# RUN pip install pandas numpy matplotlib seaborn scikit-learn scipy requests

# WORKDIR /app/pipeline/

# COPY . /app/pipeline/

# CMD [ "bash" ]
# FROM python:3.11-slim

# WORKDIR /app/pipeline/

# RUN apt-get update && apt-get install -y --no-install-recommends \
#     bash \
#     && rm -rf /var/lib/apt/lists/*

# RUN pip install --no-cache-dir \
#     pandas \
#     numpy \
#     matplotlib \
#     seaborn \
#     scikit-learn \
#     scipy \
#     requests

# COPY . /app/pipeline/

# CMD ["/bin/bash"]

# FROM python:3.11-slim

# WORKDIR /app/pipeline/

# RUN apt-get update && apt-get install -y --no-install-recommends \
#     bash \
#     && rm -rf /var/lib/apt/lists/*

# RUN python -m pip install --upgrade pip && \
#     python -m pip install --no-cache-dir pandas numpy matplotlib seaborn scikit-learn scipy requests

# COPY ingest.py preprocess.py analytics.py visualize.py cluster.py summary.sh README.md /app/pipeline/

# CMD ["/bin/bash"]
FROM python:3.11-slim

WORKDIR /app/pipeline/

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir \
    pandas \
    numpy \
    matplotlib \
    seaborn \
    scikit-learn \
    scipy \
    requests

COPY ingest.py preprocess.py analytics.py visualize.py cluster.py summary.sh /app/pipeline/
CMD ["/bin/bash"]