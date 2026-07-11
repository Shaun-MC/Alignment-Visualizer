# Build from the repo root, not api/, since core/ (an editable dependency of api/)
# has to be in the build context too:
#   docker build -f api/Dockerfile -t alignment-visualizer-api .

FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Dependencies first, in their own layer - only invalidated by changes to core/ or
# api/requirements.txt, not by application code changes below.
COPY pyproject.toml ./
COPY core/ ./core/
COPY api/requirements.txt ./api/requirements.txt
RUN cd api && pip install --no-cache-dir -r requirements.txt

# Application code
COPY api/ ./api/

RUN useradd --create-home appuser
USER appuser

WORKDIR /app/api
EXPOSE 8000

CMD ["python", "main.py"]
