import requests
import json
import time
from logger import logger
from progress_bar import ProgressBar


class YandexDisk:
    def __init__(self, token):
        self.token = token
        self.base_url = "https://cloud-api.yandex.net/v1/disk"
        self.headers = {"Authorization": f"OAuth {token}"}

    def create_folder(self, folder_name):
        """Создает папку на Яндекс.Диске"""
        print("Создание папки...")
        bar = ProgressBar(total=100, prefix='Создание папки', suffix='Complete', length=30)

        try:
            bar.update(30)
            response = requests.put(
                f"{self.base_url}/resources",
                headers=self.headers,
                params={"path": folder_name}
            )
            bar.update(80)
            result = response.status_code in [201, 409]
            bar.finish()
            return result
        except Exception as e:
            bar.update(100)
            logger.error(f"Ошибка создания папки: {e}")
            return False

    def upload_file(self, file_path, file_content):
        """Загружает файл на Яндекс.Диск"""
        print("Загрузка файла...")
        bar = ProgressBar(total=100, prefix='Загрузка', suffix='Complete', length=30)

        try:
            bar.update(10)
            # Получаем ссылку для загрузки
            response = requests.get(
                f"{self.base_url}/resources/upload",
                headers=self.headers,
                params={"path": file_path, "overwrite": "true"}
            )
            bar.update(30)

            if response.status_code == 200:
                upload_url = response.json()["href"]
                bar.update(50)

                # Загружаем файл
                upload_response = requests.put(upload_url, files={"file": file_content})
                bar.update(80)

                # Имитация прогресса проверки
                time.sleep(0.5)
                bar.finish()
                return upload_response.status_code == 201

            bar.update(100)
            return False

        except Exception as e:
            bar.update(100)
            logger.error(f"Ошибка загрузки файла: {e}")
            return False

    def get_file_info(self, file_path):
        """Получает информацию о файле"""
        print("Получение информации о файле...")
        bar = ProgressBar(total=100, prefix='Получение информации', suffix='Complete', length=30)

        try:
            bar.update(40)
            response = requests.get(
                f"{self.base_url}/resources",
                headers=self.headers,
                params={"path": file_path}
            )
            bar.update(80)

            if response.status_code == 200:
                bar.finish()
                return response.json()

            bar.update(100)
            return None
        except Exception as e:
            bar.update(100)
            logger.error(f"Ошибка получения информации: {e}")
            return None