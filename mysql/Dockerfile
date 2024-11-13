# syntax=docker/dockerfile:1

# Use the base image mysql:8.0
FROM mysql:8.0

# Set environment variables
ENV MYSQL_DATABASE ecg
ENV MYSQL_ROOT_PASSWORD 123

EXPOSE 3306

# Copy custom scripts or configuration files from your host to the container
COPY ./db/ /docker-entrypoint-initdb.d/