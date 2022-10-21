# dating_service
docker stop $(docker ps -aq) - остановить запущенные контейнеры
docker rm $(docker ps -aqf status=exited) - убить все контейнеры, которые остановлены