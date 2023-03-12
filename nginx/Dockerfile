FROM nginx:1.19.6-alpine
RUN rm /etc/nginx/conf.d/default.conf  # копи настройки из локальной папки в настройки nginx в контейнере
COPY nginx.conf /etc/nginx/conf.d
