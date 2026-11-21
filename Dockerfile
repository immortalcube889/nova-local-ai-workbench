FROM python:3.12-slim

WORKDIR /app
COPY nova_workbench ./nova_workbench
COPY static ./static
EXPOSE 8080
ENV NOVA_HOST=0.0.0.0 NOVA_PORT=8080 NOVA_DATA_DIR=/data
RUN useradd --create-home --uid 10001 nova && mkdir -p /data && chown -R nova:nova /app /data
USER nova
CMD ["python", "-m", "nova_workbench.app"]
