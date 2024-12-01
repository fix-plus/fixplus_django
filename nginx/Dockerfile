FROM nginx:latest
RUN rm /etc/nginx/conf.d/default.conf
ADD default.conf /etc/nginx/conf.d/default.conf

RUN mkdir -p /app/backend/staticfiles && \
    mkdir -p /app/backend/mediafiles && \
    mkdir -p /app/frontend/build && \
    chmod 755 /app/backend/staticfiles && \
    chmod 755 /app/backend/mediafiles  && \
    chmod 755 /app/frontend/build

VOLUME /app/backend/staticfiles
VOLUME /app/backend/mediafiles
VOLUME /app/frontend/build