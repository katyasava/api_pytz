**Задание - Сервер API на базе pytz**

1. Сервер api работает на порту 8080
2. по запросу GET /<timezone name> отдает текущее время в запрошеной зоне в виде html, если <timezone name> пустое время отдает в GTM
3. по запросу POST /api/v1/convert перобразует время из одного часового пояса в другой
   пример для проверки: ```curl -X POST -d '{"date": "12.20.2021 22:21:05", "tz": "EST"}' http://$IP_SERVER:8080/api/v1/convert/GMT```
4. по запросу POST /api/v1/datediff отдает число секунд между датами из параметра json
   пример для проверки: ```curl -X POST -d '{"first_date": "12.06.2024 22:21:05", "first_tz": "EST", "second_date": "12:30pm 2024-02-01", "second_tz": "Europe/Moscow"}' http://$IP_SERVER:8080/api/v1/datediff```
