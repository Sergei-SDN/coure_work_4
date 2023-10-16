import json
import os
from abc import ABC, abstractmethod

class JSONSaver(ABC):

    @abstractmethod
    def __init__(self, path):
        pass

    @abstractmethod
    def save_file(self, data):
        pass

    @abstractmethod
    def open_and_find_info(self, info):
        pass

    @abstractmethod
    def check_file(self):
        pass

class JSONSaver_Areas(JSONSaver):
    """
    Этот класс для сохранения информации об областях в JSON-файле.
    """
    def __init__(self, path):
        self.path = path

    def save_file(self, data: dict):
        """
        Сохранение данных в JSON-файле
        """
        with open(self.path, "w", encoding='utf-8') as file:
            json.dump(data, file)


    def open_and_find_info(self, info: str):
        """
        Поиск информации в файле.
        """
        with open(self.path, "r", encoding='utf-8') as file:
            data = json.load(file)
            if info in data:
                result = data[info]
            else:
                result = False
        return result

    def check_file(self):
        """
        Проверка доступности файла.
        """
        return os.path.isfile(self.path)