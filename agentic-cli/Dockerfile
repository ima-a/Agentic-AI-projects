FROM python:3.12-slim

RUN apt-get update && apt-get install -y gosu && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 3. Copy files
COPY requirements.txt .
# We copy the entrypoint script (which we will create next)
COPY entrypoint.sh .
COPY main.py .
COPY .env .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Sandbox setup
RUN mkdir sandbox

# 6. FIX: Make the entrypoint executable and fix Windows line endings
RUN sed -i 's/\r$//' entrypoint.sh && chmod +x entrypoint.sh

# 7. Start using the Entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["python", "main.py"]
