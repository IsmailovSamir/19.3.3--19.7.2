import json
import os

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

from settings import wrong_email, wrong_password, valid_email, valid_password

from tests.test_pet_friends import pf


class PetFriends:
    """апи библиотека к веб приложению Pet Friends"""

    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"

    def get_api_key(self, email: str, password: str) -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате
        JSON с уникальным ключем пользователя, найденного по указанным email и паролем"""

        headers = {
            'email': email,
            'password': password,
        }
        res = requests.get(self.base_url+'api/key', headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key: json, filter: str = "") -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON
        со списком наденных питомцев, совпадающих с фильтром. На данный момент фильтр может иметь
        либо пустое значение - получить список всех питомцев, либо 'my_pets' - получить список
        собственных питомцев"""

        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_new_pet(self, auth_key: json, name: str, animal_type: str,
                    age: str, pet_photo: str) -> json:
        """Метод отправляет (постит) на сервер данные о добавляемом питомце и возвращает статус
        запроса на сервер и результат в формате JSON с данными добавленного питомца"""

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result

    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """Метод отправляет на сервер запрос на удаление питомца по указанному ID и возвращает
        статус запроса и результат в формате JSON с текстом уведомления о успешном удалении.
        На сегодняшний день тут есть баг - в result приходит пустая строка, но status при этом = 200"""

        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def update_pet_info(self, auth_key: json, pet_id: str, name: str,
                        animal_type: str, age: int) -> json:
        """Метод отправляет запрос на сервер о обновлении данных питомуа по указанному ID и
        возвращает статус запроса и result в формате JSON с обновлённыи данными питомца"""

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }

        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

        """задиние 19.7.2 , метод creat_pet_simple"""

    def creat_pet_simple(self,auth_key:json, name:str , animal_type:str , age: int) -> json:

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }

        res = requests.post(self.base_url + '/api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError :
            result = res.text
        print(result)
        return status , result

    def add_photo_of_a_pet(self, auth_key:json, pet_id:str, pet_photo:str ) ->json:
        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result

    def test_get_api_key_with_wrong_password(email=valid_email, password='5454545'):
        """ Проверяем что запрос api ключа возвращает статус 403 при неверно введенном пароле"""

        # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
        status, result = pf.get_api_key(email, password)

        # Сверяем полученные данные с нашими ожиданиями
        assert status == 403
        assert "key" not in result

    # # 2 негативный тест . Создание питомца без заполнения обязательных полей

def test_unssuccesfull_add_new_pet_without_photo(name='ted', animal_type='медведь',age='12', pet_photo=''):
    """Проверяем что можно добавить питомца без прикрепления фото"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом. Ожидаем, что питомца без фото добавить данным методом нельзя
    assert status == 400
def test_unssuccsesfull_add_new_pet_without_animal_type(name='dffhxf', animal_type='fghd',
                                     age='12', pet_photo='images/ted.jpg'):
    """Проверяем что можно добавить питомца c пустым полем Тип животного"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом. Ожидаем, что питомца без обязательного поля Тип животного
    assert status == 400

def test_unssuccsesfull_add_new_pet_without_uncorrect_age_type(name='asd', animal_type='rhsdf',
                                     age='fgjg', pet_photo='images/ted.jpg'):
    """Проверяем что можно добавить питомца с наполнением поля возраст буквенными значениями вместо цифровых"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом.
    # Ожидаем, что питомец с возрастом не числового значения не может быть создан
    assert status == 400

def test_unssuccsesfull_add_realy_old_pet(name='adfgsd', animal_type='rhsdfhdf',
                                     age='10000', pet_photo='images/ted.jpg'):
    """Проверяем что можно добавить питомца со значением более двух цифр в поле возраст"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    # Ожидаем, что возраст питомца будет принят только в том случае,
    # если он состаляет 2 и менее цифр. В противном случае выводим ошибку
    if len(age) <= 2:
       assert status == 200

    else:
        # если возраст животного больше двух символов
        raise Exception("Слишком большое число")


def test_unssuccsesfull_get_api_key_with_wrong_email(email='samir-01@mail.ru', password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 403 при неверно введенном email"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert "key" not in result

def test_unssuccsesfull_create_pet_without_photo_with_invalid_key (name='чак норис', animal_type='аля-улю',
                                                  age='3'):
    """Проверяем что нельзя добавить питомца с некорректным ключом"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.create_pet_simple({'key': 'sdgdghjk'}, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403

def test_unssuccsesfull_get_my_pets_with_invalid_key(filter="my_pets"):
    """ Проверяем, что запрос "моих питомцев" при запросе с неверно указанным ключом ничего не возвращает """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets({'key': '.eJwljjluQzEMRO-i2oW4SCJ9GUPckLTfdhXk7hbgbjAPM3h_7VFXPn_a_XW989Yev9HujSeCAgXBBsTaNos7q9LpgcxgrH4QW2A5j8PDbKOm9gBY6ilQc_reSSUJXFaTIwbWWUZ1LtyJaBXh7lxUc3jnLgIyUdoReT_z-tr4dKRYCdn38HWiZtSOIGWpLueIh6YPBVzTIIRUhLL9fwCe2D7i.Y2v6MA.h6yvEPd9jxhUIB0z_P8lK4fZGZU	'}, filter)
    assert status == 403