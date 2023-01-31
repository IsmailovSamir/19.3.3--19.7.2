import requests
import json
from datetime import datetime, timezone
import random
import config

# Задаём базовый URL, как делали в Postman
base_url = 'https://petstore.swagger.io/v2'

# GET /user/login  Logs user into the system

username = config.username  # Задаём имя пользователя
password = config.password  # Задаём пароль

res = requests.get(f'{base_url}/user/login?login={username}&password={password}',
                   headers={'accept': 'application/json'})

print('GET /user/login  Logs user into the system')
print('  Статус запроса:', res.status_code)
print('  Ответ сервера body:', res.json())
print('  Ответ сервера header:', res.headers, '\n')

# POST /user  Create user

body = json.dumps(config.created_user)

res = requests.post(f'{base_url}/user', headers={'accept': 'application/json', 'Content-Type': 'application/json'},
                    data=body)

print('POST /user  Create user')
print('  Статус запроса:', res.status_code)
print('  Ответ сервера body:', res.json(), '\n')

# PUT /user/{username} Updated user

username = config.created_user['username']
body = json.dumps(config.updated_user)

res = requests.put(f'{base_url}/user/{username}',
                   headers={'accept': 'application/json', 'Content-Type': 'application/json'}, data=body)

print('PUT /user/{username} Updated user')
print('  Статус запроса:', res.status_code)
print('  Ответ сервера body:', res.json(), '\n')

# GET /user/{username} Get user by user name (before delete)

username = config.updated_user['username']

res = requests.get(f'{base_url}/user/{username}', headers={'accept': 'application/json'})

print('GET /user/{username} Get user by user name (before delete)')
print('  Статус запроса:', res.status_code)
print('  Ответ сервера body:', res.json(), '\n')

# DELETE /user/{username} Delete user

username = config.updated_user['username']

res = requests.delete(f'{base_url}/user/{username}', headers={'accept': 'application/json'})

print('DELETE /user/{username} Delete user')
print('  Статус запроса:', res.status_code)
print('  Ответ сервера body:', res.json(), '\n')

# GET /user/{username} Get user by user name (after delete)

username = config.updated_user['username']

res = requests.get(f'{base_url}/user/{username}', headers={'accept': 'application/json'})

print('GET /user/{username} Get user by user name (after delete) expected code 404')
print('  Статус запроса:', res.status_code)
print('  Ответ сервера body:', res.json(), '\n')

# POST /user/createWithList Creates list of users with given input array

body = json.dumps(config.list_of_users)

res = requests.post(f'{base_url}/user/createWithList', headers={'accept': 'application/json',
                                                                'Content-Type': 'application/json'}, data=body)

print('POST /user/createWithList Creates list of users with given input array')
print('  Статус запроса:', res.status_code)
print('  Ответ сервера body:', res.json(), '\n')

# POST /user/createWithArray Creates list of users with given input array
# Не могу понять чем этот запрос отличается от предыдущего, но раз он есть - надо проверить

body = json.dumps(config.list_of_users)

res = requests.post(f'{base_url}/user/createWithArray', headers={'accept': 'application/json',
                                                                 'Content-Type': 'application/json'}, data=body)

print('POST /user/createWithArray Creates list of users with given input array')
print('  Статус запроса:', res.status_code)
print('  Ответ сервера body:', res.json(), '\n')

# GET /user/logout  Logs out current logged in user session

res = requests.get(f'{base_url}/user/logout', headers={'accept': 'application/json'})

print('GET /user/logout  Logs out current logged in user session')
print('  Статус запроса:', res.status_code)
print('  Ответ сервера body:', res.json(), '\n')

# POST /store/order  Place an order for a pet

now = datetime.now(timezone.utc)  # Текущее время в UTC для заказа
body = config.order
body['shipDate'] = now.isoformat()  # Подставляем текущее время в заказ, так же можно изменить petId и quantity
body = json.dumps(body)

res = requests.post(f'{base_url}/store/order', headers={'accept': 'application/json',
                                                        'Content-Type': 'application/json'}, data=body)

orderid_for_delete = res.json()['id']  # Запоминаем id заказа, что бы удалить его в последующей проверке

print('POST /store/order  Place an order for a pet')
print('  Статус запроса:', res.status_code)
print('  Ответ сервера body:', res.json(), '\n')

# GET /store/order/{orderId}  Find purchase order by ID

orderId = random.randint(1, 10)  # Генерируем случайный номер заказа >= 1 и <= 10

res = requests.get(f'{base_url}/store/order/{orderId}', headers={'accept': 'application/json'})

print('GET /store/order/{orderId}  Find purchase order by ID')
print('  Статус запроса:', res.status_code)
print('  Ответ сервера body:', res.json(), '\n')

# DELETE /store/order/{orderId}  Delete purchase order by ID

orderId = orderid_for_delete  # id заказа созданного выше

res = requests.delete(f'{base_url}/store/order/{orderId}', headers={'accept': 'application/json'})

print('DELETE /store/order/{orderId}  Delete purchase order by ID')
print('  Статус запроса:', res.status_code)
print('  Ответ сервера body:', res.json(), '\n')

# GET /store/inventory  Returns pet inventories by status

res = requests.get(f'{base_url}/store/inventory', headers={'accept': 'application/json'})

print('GET /store/inventory  Returns pet inventories by status')
print('  Статус запроса:', res.status_code)
print('  Ответ сервера body:', res.json(), '\n')

# POST /pet  Add a new pet to the store

body = config.new_pet
body['name'] = 'Petya'  # Имя добавляемого питомца
body['category']['name'] = 'python'  # Категория добавляемого питомца (не знаю что это пусть будет вид)
body['tags'][0]['name'] = 'carnivorous'  # Метка добавляемого питомца
body['tags'].append({"id": 0, "name": "long snake"})  # Ещё одна метка добавляемого питомца
body['status'] = 'test_status'  # Статус для тестирования, используется дальше
body = json.dumps(body)

res = requests.post(f'{base_url}/pet', headers={'accept': 'application/json',
                                                'Content-Type': 'application/json'}, data=body)

petid = res.json()['id']  # Запоминаем id добавленного питомца, потом пригодится

print('POST /pet  Add a new pet to the store')
print('  Статус запроса:', res.status_code)
print('  Ответ сервера body:', res.json(), '\n')

# GET /pet/findByStatus  Finds Pets by status

status = 'test_status'

res = requests.get(f'{base_url}/pet/findByStatus?status={status}', headers={'accept': 'application/json'})

print('GET /pet/findByStatus  Finds Pets by status')
print('  Статус запроса:', res.status_code)
print('  Ответ сервера body:', res.json(), '\n')

# PUT /pet  Update an existing pet

body = config.new_pet
body['id'] = petid  # Указываем id питомца которого надо обновить
body['name'] = 'Petya2'  # Новое имя питомца
body['category']['name'] = 'python'  # Категорию не трогаем
body['tags'][0]['name'] = 'carnivorous'  # Первую метку тоже не трогаем
body['tags'].append({"id": 1, "name": "very long snake"})  # За время пути питомец успел подрасти
body['status'] = 'test_status'  # Статус не трогаем
body = json.dumps(body)

res = requests.put(f'{base_url}/pet', headers={'accept': 'application/json',
                                               'Content-Type': 'application/json'}, data=body)

print('PUT /pet  Update an existing pet')
print('  Статус запроса:', res.status_code)
print('  Ответ сервера body:', res.json(), '\n')

# POST /pet/{petId}/uploadImage  Uploads an image

petId = petid
image = 'python.jpg'
files = {'file': (image, open(image, 'rb'), 'image/jpeg')}

res = requests.post(f'{base_url}/pet/{petId}/uploadImage', headers={'accept': 'application/json'}, files=files)

print('POST /pet/{petId}/uploadImage  Uploads an image')
print('  Статус запроса:', res.status_code)
print('  Ответ сервера body:', res.json(), '\n')


# GET /pet/{petId}  Find pet by ID

petId = petid

res = requests.get(f'{base_url}/pet/{petId}', headers={'accept': 'application/json'})

print('GET /pet/{petId}  Find pet by ID')
print('  Статус запроса:', res.status_code)
print('  Ответ сервера body:', res.json(), '\n')


# POST /pet/{petId}  Updates a pet in the store with form data

petId = petid
name = 'Petya3'
status = 'new_test_status'
body = f'name={name}&status={status}'

res = requests.post(f'{base_url}/pet/{petId}', headers={'accept': 'application/json',
                                                        'Content-Type': 'application/x-www-form-urlencoded'}, data=body)

print('POST /pet/{petId}  Updates a pet in the store with form data')
print('  Статус запроса:', res.status_code)
print('  Ответ сервера body:', res.json(), '\n')


# DELETE /pet/{petId}  Deletes a pet

petId = petid

res = requests.delete(f'{base_url}/pet/{petId}', headers={'accept': 'application/json'})

print('DELETE /pet/{petId}  Deletes a pet')
print('  Статус запроса:', res.status_code)
print('  Ответ сервера body:', res.json(), '\n')