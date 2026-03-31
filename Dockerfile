# Combined Dockerfile for GenMentor (Frontend + Backend)
FROM python:3.10-slim

# Set environment variables for faster download in China
ENV HF_ENDPOINT=https://hf-mirror.com
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install dependencies
COPY backend/requirements.txt ./backend/requirements.txt
COPY frontend/requirements.txt ./frontend/requirements.txt

RUN pip install --no-cache-dir -r backend/requirements.txt
RUN pip install --no-cache-dir -r frontend/requirements.txt
# Ensure sentence-transformers and huggingface-hub are correctly versioned for langchain-huggingface
RUN pip install --no-cache-dir huggingface-hub==0.33.4 transformers -U sentence-transformers -U hf_transfer

# Copy the rest of the code
COPY . .

# Create a startup script
RUN echo '#!/bin/bash\n\
python backend/main.py & \n\
streamlit run frontend/main.py --server.port 8501 --server.address 0.0.0.0\n\
' > /app/start.sh && chmod +x /app/start.sh

# Expose the ports (Backend: 5000, Frontend: 8501)
EXPOSE 5000 8501

# Run the startup script
CMD ["/app/start.sh"]
