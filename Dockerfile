FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN pip install --no-cache-dir -e .

ENV KEDRO_DISABLE_TELEMETRY=1

# 8888 is only used when overriding CMD to launch `kedro jupyter lab` (see run_notebook.sh).
# 4141 is only used when overriding CMD to launch `kedro viz run` (see run_viz.sh).
EXPOSE 8888 4141

CMD ["kedro", "run"]
