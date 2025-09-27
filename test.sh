docker stop $(docker ps -q)
docker container prune #-f
docker image prune -a
docker build -t sugoi-v4:1.0 .
docker run -p 7860:7860 sugoi-v4:1.0
