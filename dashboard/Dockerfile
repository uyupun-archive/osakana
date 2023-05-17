# ビルドステージ
FROM node:18.15.0 AS build

WORKDIR /app

COPY . .
RUN npm ci
RUN npm run build


# ランタイムステージ
FROM nginx:stable as runtime

COPY --from=build /app/dist /usr/share/nginx/html

ARG PORT=3000
ENV PORT=$PORT
COPY default.conf.template /etc/nginx/conf.d/default.conf.template
RUN envsubst "${PORT}" < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf
EXPOSE $PORT

CMD ["nginx", "-g", "daemon off;"]
