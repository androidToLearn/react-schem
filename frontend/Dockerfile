FROM node:18

WORKDIR /app
COPY package*.json .
RUN npm install
RUN npm install -g serve
COPY . .

ENV REACT_APP_MODE=production

RUN npm run build

CMD ["serve", "/app/dist"]
