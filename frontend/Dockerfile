FROM node:20-alpine

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install

COPY app ./app
COPY components ./components
COPY lib ./lib
COPY public ./public
COPY tests ./tests
COPY jsconfig.json ./jsconfig.json
COPY next.config.mjs ./next.config.mjs
COPY vitest.config.mjs ./vitest.config.mjs

CMD ["npm", "run", "dev"]