FROM nginx:alpine

LABEL org.opencontainers.image.title="codyssey-week1-nginx"
LABEL org.opencontainers.image.description="Week1 Mission1 custom nginx container"

ENV APP_ENV=development

COPY site/ /usr/share/nginx/html/

EXPOSE 80
