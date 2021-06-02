## Развертывание приложения
Предварительно должен быть установлен Docker. 

### 1. Сборка образов
```shell
cd db && docker build -t inford_db . && cd ..
cd services/client_service && docker build -t client_service . && ../..
cd services/analysis_service && docker build -t analysis_service . && ../..
```

### 2. Создание Docker Network
```shell
docker network create inford_network
```

### 3. Запуск БД
```shell
docker run --rm -it -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres --name postgres --network inford_network inford_db
```

### 4. Запуск сервисов
```shell
docker run --rm -it --network inford_network --name analysis_service analysis_service
docker run --rm -it --network inford_network -p 80:80 --name client_service client_service
```

Или через docker-compose (тогда должен быть предустановлен docker-compose)
```shell
docker-compose up -d
```

## Или через скрипт
```shell
./deploy.sh
```

