# 1️⃣ Use a lightweight Python image as the base
FROM python:3.9

# 2️⃣ Set the working directory inside the container
WORKDIR /app

# 3️⃣ Copy all files from your project directory into the container
COPY . .

# 4️⃣ Install required dependencies
RUN pip install -r requirements.txt

# 5️⃣ Expose port 7860 (Hugging Face Spaces uses this port)
EXPOSE 7860

# 6️⃣ Run FastAPI backend when the container starts
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
