FROM python:3.14

WORKDIR /app

RUN pip install uv

COPY . .

RUN uv sync --frozen

CMD ["uv", "run", "python", "src/cli.py"]