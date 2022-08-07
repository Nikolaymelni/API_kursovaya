from VK import VkUser
from YA import YaUser
import configparser

if __name__ == '__main__':

    user_id = VkUser(input('Введите ID ВК: '))
    config_ya = configparser.ConfigParser()
    config_ya.read("tokens.ini")
    token_ya = config_ya["ya"]["token"]
    user_ya = YaUser(token_ya)
    #user_ya = YaUser(input('Введите Токен YA: '))

    user_ya.copying_photos_to_disk(user_id)
