FROM nginx:stable-alpine

COPY nginx/default.conf /etc/nginx/conf.d/default.conf
COPY frontend/html/ /usr/share/nginx/html/
COPY frontend/css/ /usr/share/nginx/html/css/
COPY frontend/js/ /usr/share/nginx/html/js/

EXPOSE 80
