FROM python:3.11-slim
WORKDIR /app
COPY app.py .
RUN mkdir -p /data
ENV PORT=8080
ENV DB_PATH=/data/negative-space.db
EXPOSE 8080
CMD ["python3", "app.py"]
