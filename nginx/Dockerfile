FROM nginx:1.20.0-alpine

LABEL maintainer="YOUR_COMPANY <info@YOUR_DOMAIN>"
LABEL fileVersion="1"

COPY ./static /opt/app/static
COPY ./nginx.conf /etc/nginx/

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["nginx"]
