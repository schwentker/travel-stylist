FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN --mount=type=secret,id=pip_ca if [ -f /run/secrets/pip_ca ]; then export PIP_CERT=/run/secrets/pip_ca; fi && pip install --no-cache-dir -r requirements.txt
COPY --chown=65532:65532 *.py commerce/
COPY --chown=65532:65532 contracts commerce/contracts
COPY --chown=65532:65532 fixtures commerce/fixtures
COPY --chown=65532:65532 web commerce/web
USER 65532:65532
CMD ["python", "-m", "uvicorn", "commerce.app:app", "--host", "0.0.0.0", "--port", "8000"]
