FROM node:20-alpine

WORKDIR /app

COPY package.json package-lock.json* ./

# If you don't have package-lock.json, npm install will still work
RUN npm install

COPY . .

CMD ["npm", "run", "dev"]
