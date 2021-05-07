## Развертывание приложения
Предварительно должен быть установлен Docker. 

### 1. Сборка образов
```shell
cd db && docker build -t inford_db . && cd ..
cd services/client_service && docker build -t client_service . && ../..
```

### 2. Создание Docker Network
```shell
docker network create inford_network
```

### 3. Запуск БД
```shell
docker run -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres --name postgres --network inford_network inford_db
```

### 4. Запуск сервисов
```shell
docker run --network inford_network -p 80:80 client_service
```
