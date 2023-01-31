import os
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

from api import PetFriends
from settings import valid_email, valid_password


class PetFriends_negative:
    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"


pf = PetFriends_negative()



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
def test_unssuccsesfull_add_new_pet_without_animal_type(name='asaasas', animal_type='',
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

def test_unssuccsesfull_add_new_pet_without_uncorrect_age_type(name='dffhxf', animal_type='fghd',
                                     age='gvhjbhbbblj', pet_photo='images/ted.jpg'):
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

def test_unssuccsesfull_add_realy_old_pet(name='asd', animal_type='rhsdf',
                                     age='10000', pet_photo='images/cat1.jpg'):
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