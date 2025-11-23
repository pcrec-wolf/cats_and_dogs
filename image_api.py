import requests


class ImageAPI:
    def __init__(self):
        pass

    def get_cat_with_text(self, text):
        """Получить картинку кошки с текстом"""
        if text:
            url = f"https://cataas.com/cat/says/{text}"
        else:
            url = "https://cataas.com/cat"

        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при получении изображения кошки: {e}")
            return None

    def get_dog_image(self, breed="random", sub_breed=None):
        """Получить случайное изображение собаки"""
        try:
            if breed == "random":
                url = "https://dog.ceo/api/breeds/image/random"
            elif sub_breed:
                url = f"https://dog.ceo/api/breed/{breed}/{sub_breed}/images/random"
            else:
                url = f"https://dog.ceo/api/breed/{breed}/images/random"

            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                image_url = data['message']

                # Скачиваем само изображение
                img_response = requests.get(image_url)
                if img_response.status_code == 200:
                    return img_response.content
            return None

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при получении изображения собаки: {e}")
            return None

    def get_all_dog_breeds(self):
        """Получить список всех пород собак"""
        try:
            response = requests.get("https://dog.ceo/api/breeds/list/all")
            if response.status_code == 200:
                return response.json()['message']
            return {}
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при получении списка пород: {e}")
            return {}