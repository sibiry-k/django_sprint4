<h1 align="center">Блогикум</h1>
<p align="center">
<img src="https://img.shields.io/badge/-Python_-Python?style=plastic&logo=python&logoColor=%233776AB&color=%23F8DD4C">
<img src="https://img.shields.io/badge/-Django_-Django?style=plastic&logo=Django&logoColor=%23092E20&color=%235AC02C">
<img src="https://img.shields.io/badge/-SQLite_-SQLite?style=plastic&logo=sqlite&logoColor=%23003B57&color=6fa8dc">
</p>

___

## Блогикум - учебный проект, написанный с использованием фреймворка *Django*, целью которого является закрепление полученных навыков работы с *Django ORM*.
**Блогикум** представляет собой социальную сеть для публикации личных дневников, на котором пользователь может создать свою страницу и публиковать на ней посты. Для каждого поста указывается категория, а также, опционально - локация. 

Для реализации данного функционала:
 - описаны модели **Post**, **Category**, **Location**, **User**
 - настроена панель администратора **Django**
 - написаны view-функции, формы, пути
 - отредактированы HTML-шаблоны

## Запуск проекта
### Перед запуском проекта необходимо:
1. Клонировать репозитарий на локальную машину.
2. Создать виртуальное пространство:<br>
   ```python -m venv venv```
3. Активировать виртуальное пространство:<br>
3.1. Для Windows:<br>
   ```source venv/Scripts/activate``` <br>
3.2. Для Linux или MacOS:<br>
   ```source venv/bin/activate```
4. Обновить менеджер пакетов pip:<br>
   ```python -m pip install --upgrade pip```
5. Устаноить зависиомсти проекта:<br>
   ```pip install -r requirements.txt```


Проект готов к запуску!

### Запуск проекта:
Для запуска необходимо перейти в рабочую папку проекта (там где лежит файл *manage.py*) и выполнить команды:
1. Для создания и применения миграций:<br>
   ```python manage.py makemigrations```<br>
   ```python manage.py migrate```
2. Для запуска сервера разработки:<br>
   ```python manage.py runserver```
