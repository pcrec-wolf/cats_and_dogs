import requests
import json
from logger import logger


class YandexDisk:
    def __init__(self, token):
        self.token = token
        self.base_url = "https://cloud-api.yandex.net/v1/disk"
        self.headers = {"Authorization": f"OAuth {token}"}

    def create_folder(self, folder_name):
        """Создает папку на Яндекс.Диске"""
        try:
            response = requests.put(
                f"{self.base_url}/resources",
                headers=self.headers,
                params={"path": folder_name}
            )
            return response.status_code in [201, 409]
        except Exception as e:
            logger.error(f"Ошибка создания папки: {e}")
            return False

    def upload_file(self, file_path, file_content):
        """Загружает файл на Яндекс.Диск"""
        try:
            # Получаем ссылку для загрузки
            response = requests.get(
                f"{self.base_url}/resources/upload",
                headers=self.headers,
                params={"path": file_path, "overwrite": "true"}
            )

            if response.status_code == 200:
                upload_url = response.json()["href"]

                # Загружаем файл
                upload_response = requests.put(upload_url, files={"file": file_content})
                return upload_response.status_code == 201
            return False

        except Exception as e:
            logger.error(f"Ошибка загрузки файла: {e}")
            return False

    def get_file_info(self, file_path):
        """Получает информацию о файле"""
        try:
            response = requests.get(
                f"{self.base_url}/resources",
                headers=self.headers,
                params={"path": file_path}
            )
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            logger.error(f"Ошибка получения информации: {e}")
            return None