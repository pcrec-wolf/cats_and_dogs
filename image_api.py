import requests
from progress_bar import ProgressBar


class ImageAPI:
    def __init__(self):
        pass

    def get_cat_with_text(self, text):
        """Получить картинку кошки с текстом"""
        print("Получение картинки кошки...")
        bar = ProgressBar(total=100, prefix='Скачивание', suffix='Complete', length=30)

        if text:
            url = f"https://cataas.com/cat/says/{text}"
        else:
            url = "https://cataas.com/cat"

        try:
            bar.update(20)
            response = requests.get(url)
            bar.update(60)
            response.raise_for_status()
            bar.update(80)
            image_data = response.content
            bar.finish()
            return image_data
        except requests.exceptions.RequestException as e:
            bar.update(100)
            print(f"\nОшибка при получении изображения кошки: {e}")
            return None

    def get_dog_image(self, breed="random", sub_breed=None):
        """Получить случайное изображение собаки"""
        print("Получение картинки собаки...")
        bar = ProgressBar(total=100, prefix='Скачивание', suffix='Complete', length=30)

        try:
            bar.update(10)
            if breed == "random":
                url = "https://dog.ceo/api/breeds/image/random"
            elif sub_breed:
                url = f"https://dog.ceo/api/breed/{breed}/{sub_breed}/images/random"
            else:
                url = f"https://dog.ceo/api/breed/{breed}/images/random"

            bar.update(30)
            response = requests.get(url)
            bar.update(50)

            if response.status_code == 200:
                data = response.json()
                image_url = data['message']

                bar.update(60)
                # Скачиваем само изображение
                img_response = requests.get(image_url)
                bar.update(80)

                if img_response.status_code == 200:
                    bar.finish()
                    return img_response.content
            bar.update(100)
            return None

        except requests.exceptions.RequestException as e:
            bar.update(100)
            print(f"\nОшибка при получении изображения собаки: {e}")
            return None

    def get_all_dog_breeds(self):
        """Получить список всех пород собак"""
        print("Загрузка списка пород...")
        bar = ProgressBar(total=100, prefix='Получение пород', suffix='Complete', length=30)

        try:
            bar.update(30)
            response = requests.get("https://dog.ceo/api/breeds/list/all")
            bar.update(70)

            if response.status_code == 200:
                bar.finish()
                return response.json()['message']
            bar.update(100)
            return {}
        except requests.exceptions.RequestException as e:
            bar.update(100)
            print(f"\nОшибка при получении списка пород: {e}")
            return {}