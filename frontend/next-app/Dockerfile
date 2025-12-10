# frontend/next-app/Dockerfile
FROM node:18-alpine

WORKDIR /app
COPY frontend/next-app/package.json frontend/next-app/package-lock.json ./
RUN npm ci

COPY frontend/next-app ./

ENV NEXT_TELEMETRY_DISABLED=1

RUN npm run build

EXPOSE 3000
CMD ["npm", "start"]
