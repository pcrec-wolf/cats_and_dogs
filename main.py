import image_api
import Ya_disk
import json
from config import YA_TOKEN, FOLDER_NAME


def save_info_to_json(info_data, filename="upload_info.json"):
    """Сохраняет информацию о загруженных файлах в JSON"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(info_data, f, ensure_ascii=False, indent=2)
        print(f"Информация сохранена в {filename}")
    except Exception as e:
        print(f"Ошибка сохранения JSON: {e}")


def show_dog_breeds(image_api):
    """Показать доступные породы собак"""
    print("\nПолучение списка пород...")
    breeds = image_api.get_all_dog_breeds()

    if not breeds:
        print("Не удалось получить список пород")
        return None

    print("\nДоступные породы:")
    breed_list = list(breeds.keys())
    for i, breed in enumerate(breed_list[:20], 1):  # Показываем первые 20 пород
        sub_breeds = breeds[breed]
        if sub_breeds:
            print(f"{i}. {breed} ({', '.join(sub_breeds)})")
        else:
            print(f"{i}. {breed}")

    print("21. Случайная порода")
    return breed_list


def choose_image_type(image_api):
    """Выбор типа картинки"""
    print("=" * 50)
    print("Выберите тип картинки:")
    print("1. Кошка с текстом")
    print("2. Собака")

    choice = input("Введите номер (1 или 2): ").strip()

    if choice == "1":
        text = input("Введите текст для картинки: ").strip()
        image_data = image_api.get_cat_with_text(text)
        file_name = f"cat_{text}.jpg" if text else "cat_random.jpg"
        return image_data, file_name

    elif choice == "2":
        breed_list = show_dog_breeds(image_api)
        if not breed_list:
            return None, None

        breed_choice = input("Введите номер породы (1-21): ").strip()

        try:
            breed_choice = int(breed_choice)
            if 1 <= breed_choice <= 20:
                breed = breed_list[breed_choice - 1]
                image_data = image_api.get_dog_image(breed)
                file_name = f"dog_{breed}.jpg"
            elif breed_choice == 21:
                image_data = image_api.get_dog_image("random")
                file_name = "dog_random.jpg"
            else:
                print("Неверный выбор")
                return None, None

            return image_data, file_name

        except (ValueError, IndexError):
            print("Неверный ввод")
            return None, None

    else:
        print("Неверный выбор")
        return None, None


def main():
    # Инициализация API
    api = image_api.ImageAPI()

    # Получаем токен
    token = YA_TOKEN or input('Введите токен Яндекс.Диска: ').strip()

    if not token or token == 'your_token_here':
        print("Ошибка: Не указан токен Яндекс.Диска")
        return

    # Выбираем тип картинки
    image_data, file_name = choose_image_type(api)

    if not image_data or not file_name:
        print("Не удалось получить картинку")
        return

    # Сохраняем локально для проверки
    local_path = f"temp_{file_name}"
    with open(local_path, "wb") as f:
        f.write(image_data)
    print(f"Картинка скачана и сохранена локально: {local_path}")

    # Работа с Яндекс.Диском
    yandex_disk = Ya_disk.YandexDisk(token)

    # Создаем папку
    if not yandex_disk.create_folder(FOLDER_NAME):
        print("Ошибка создания папки на Яндекс.Диске")
        return

    # Загружаем на Яндекс.Диск
    remote_path = f"{FOLDER_NAME}/{file_name}"

    print("Загрузка на Яндекс.Диск...")
    if yandex_disk.upload_file(remote_path, image_data):
        print(f"Картинка успешно загружена на Яндекс.Диск: {remote_path}")

        # Получаем информацию о файле
        file_info = yandex_disk.get_file_info(remote_path)

        # Сохраняем информацию в JSON
        if file_info:
            info_data = {
                "file_name": file_name,
                "remote_path": remote_path,
                "size": file_info.get("size", 0),
                "created": file_info.get("created", ""),
                "modified": file_info.get("modified", ""),
                "type": "cat" if "cat" in file_name else "dog"
            }

            save_info_to_json([info_data])
            print(f"Размер файла: {file_info.get('size', 0)} байт")
        else:
            print("Не удалось получить информацию о файле")
    else:
        print("Ошибка загрузки на Яндекс.Диск")


if __name__ == "__main__":
    main()
