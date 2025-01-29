FROM node:16-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

ENV VITE_HOST=0.0.0.0

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]