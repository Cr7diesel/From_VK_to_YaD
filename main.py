from Vk import VkUser
from Yandex import UploadToYaD


if __name__ == '__main__':
    vk_user_id = VkUser(input('Введите id пользователя: '))
    uploader = UploadToYaD(input('Введите токен ЯндексДиска: '))
    print('Скачиваем фотографии профиля и сохраняем на ЯндексДиск')
    uploader.from_vk_to_yad(vk_user_id)
