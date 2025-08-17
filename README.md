# Сервис создания кошельков, пополнения и вывода средств.

## [Документация ](http://localhost:8000/docs)

1. `make start` - Формирование Docker - образа + запуск.
2. `make stop` - Остановка.
3. `make venv` - Создание виртуального окружения
4. `source venv/bin/activate` - Активация виртуального окружения
5. `make install` - Установка зависимостей проекта.
6. `make test` - Тестирование проекта.

Для запуска тестов необходимо создать виртуальное окружение \
активировать его и установить зависимости, **_ТОЛЬКО_** после этого \
выполнять команду `make test`.

# Начало работы.

1. Cоздайте свой **SECRET_KEY** для файла **.env.prod**

**Windows:**

```
from secrets import token_bytes
from base64 import b64encode
print(b64encode(token_bytes(32)).decode())
```

**Linux/MacOs:**

```
openssl rand -base64 32
```

2. Зарегистрируйте пользователя:
```
curl -X 'POST' \
  'http://localhost:8000/api/v1/auth/register/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "SuperUserName",
  "password": "SuperSecretPassword"
}'
```

2. Войдите в систему:

```
curl -X 'POST' \
  'http://localhost:8000/api/v1/auth/login/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "SuperUserName",
  "password": "SuperSecretPassword"
}'
```

3. Создайте кошелек(_**Только авторизованный пользователь**_ \
может создать кошелек в системе.)

```
curl -X 'POST' \
  'http://localhost:8000/api/v1/wallets/create' \
  -H 'accept: application/json' \
  -d ''
```

4. Чтобы узнать свой wallet ID, если вдруг вы его забыли, \
то посмотреть его можно по адресу. \
(**_Только авторизованный пользователь_** \
может смотреть свой кошелек)
```
curl -X 'GET' \
  'http://localhost:8000/api/v1/wallets/my/' \
  -H 'accept: application/json'
```
5. [ПО ТЗ] Узнать баланс кошелька. \
Получить баланс кошелька может **_только \ 
авторизованный пользователь_**, который еще же \
_**является его владельцем**_.
```
curl -X 'GET' \
  'http://localhost:8000/api/v1/wallets/fdf607d9-ddec-4e37-8a81-ec8a8053bb41' \
  -H 'accept: application/json'
```

6. [ПО ТЗ] Совершение операций с кошельком. \
Доступные виды operation (`"DEPOSIT"`, `"WITHDRAW"`)

Пополнить(`DEPOSIT`) баланс кошелька, может любой пользователь \
неважно, авторизован он, или является ли он владельцем кошелька.
```
curl -X 'POST' \
  'http://localhost:8000/api/v1/wallets/fdf607d9-ddec-4e37-8a81-ec8a8053bb41/operation/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "operation": "DEPOSIT",
  "amount": 100
}'
```
Вывод(`WITHDRAW`) средств с баланса кошелька, может совершить **_только \
авторизованный пользователь_**, который является **_владельцем кошелька_**.
```
curl -X 'POST' \
  'http://localhost:8000/api/v1/wallets/fdf607d9-ddec-4e37-8a81-ec8a8053bb41/operation/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "operation": "WITHDRAW",
  "amount": 90
}'
```

7. Получить выписку по операциям совершенных с балансом кошелька:
Выписку может получить только авторизованный пользователь, являющийся \ 
владельцем кошелька.
```
curl -X 'GET' \
  'http://localhost:8000/api/v1/wallets/fdf607d9-ddec-4e37-8a81-ec8a8053bb41/details' \
  -H 'accept: application/json'
```

Технологический стэк:
1. Python 3.12
2. FastAPI
3. PostgreSQL
4. Pydantic
5. SQLAlchemy
6. Docker
7. Docker-compose
8. Grafana + Prometheus
9. Flake-8

**Надеюсь Вам понравится моя работа и Вы получите удовольствие от ее использования, как я, когда ее писал :)**