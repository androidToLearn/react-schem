# -----------------
# שלב 1: Build React (Vite)
# -----------------
FROM node:18 AS builder

WORKDIR /app
COPY package*.json .
RUN npm install
RUN npm install -g serve
COPY . .

ENV REACT_APP_MODE=production

RUN npm run build
# -----------------
# שלב 2: Flask
# -----------------
FROM python:3.11-slim
WORKDIR /app


# התקנת Flask והרחבות
COPY requirements.txt .
RUN python -m pip install -r requirements.txt


COPY  . . 

# העתקת קבצי backend

# העתקת ה־React build (Vite יוצרת dist/)

EXPOSE 5000
CMD ["python", "app.py"]
