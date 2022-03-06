FROM python:3.7-alpine

WORKDIR .

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev make musl-dev g++ libstdc++
RUN python -m pip install --upgrade pip

COPY . .
RUN pip install -r requirements.txt

EXPOSE 5005

COPY . .
CMD ["python", "main.py"]

