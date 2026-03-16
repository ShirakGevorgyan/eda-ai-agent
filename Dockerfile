FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
EXPOSE 8501

RUN echo "#!/bin/bash\nuvicorn app.main:app --host 0.0.0.0 --port 8000 & \nstreamlit run frontend/ui.py --server.port 8501 --server.address 0.0.0.0" > /app/run.sh
RUN chmod +x /app/run.sh

CMD ["/app/run.sh"]