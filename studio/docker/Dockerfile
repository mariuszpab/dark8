FROM nginx:stable-alpine
# Copy web assets from build context (pass project root as context)
# When building: docker build -t dark8-studio:local -f studio/docker/Dockerfile .
COPY web /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
