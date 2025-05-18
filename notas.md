autopep8 --in-place -aaa  # Nível 3 para aplicação do PEP8 no código.

# subindo containers:

🔁 1. Taguear as imagens
🚀 2. Subir para o Docker Hub

docker tag tc-app willmacedo1/tc-app:latest
docker tag tc-mlflow willmacedo1/tc-mlflow:latest

docker push willmacedo1/tc-app:latest
docker push willmacedo1/tc-mlflow:latest


# Logando e subindo containers:

docker container prune & docker compose -f docker-compose.yaml build --no-cache & docker compose -f docker-compose.yaml up
docker tag tc-app willmacedo1/tc-app:latest
docker tag tc-mlflow willmacedo1/tc-mlflow:latest

docker push willmacedo1/tc-app:latest
docker push willmacedo1/tc-mlflow:latest

# ------------------------------------------------------------------------- #


docker stop $(docker ps -aq)
docker rm -f $(docker ps -aq)
docker rmi -f $(docker images -q)
sudo docker run --restart=always -p 8000:8000 --name tc-app willmacedo1/tc-app
sudo docker run --restart=always -p 5000:5000 --name tc-mlflow willmacedo1/tc-mlflow
docker logs -f tc-app
# docker logs -f tc-mlflow
