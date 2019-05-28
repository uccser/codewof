FROM uccser/nginx-with-gulp:1.15.8

ADD codewof/package.json /app/
RUN npm install
ADD ./codewof/ /app/
RUN chmod 755 /app/
ADD infrastructure/nginx/nginx.conf /etc/nginx/nginx.conf
