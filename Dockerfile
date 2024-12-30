FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


# Set working directory
WORKDIR /Flasheeta

# Install dependencies
RUN pip install --upgrade pip setuptools wheel

RUN apt-get update && apt-get install -y \
    python3-dev gcc libmariadb-dev libmariadb3 pkg-config

RUN pip install greenlet
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose the port Flask runs on
EXPOSE 5000

# Command to run the application
CMD ["flask", "run"]