# praktikum_new_diplom
https://github.com/MuhammadMlv/foodgram-project-react/actions/workflows/main.yml/badge.svg

## Описание
Продуктовый помощник». Онлайн-сервис и API для него. На этом сервисе 
пользователи публикуют свои рецепты, подписываются на публикации других 
пользователей, добавляют понравившиеся рецепты в список «Избранное», а перед 
походом в магазин могут скачать сводный список продуктов, необходимых для 
приготовления одного или нескольких выбранных блюд

### Стэк технологий: 
- Python
- Django
- Django DRF
- Docker
- React
- Nginx
- PostgreSQL
- 
### Как запустить проект:

Для запуска приложение у вас должен быть установлен Docker.

Клонировать репозиторий и перейти в него в командной строке:

```
https://github.com/MuhammadMlv/MuhammadMlv/foodgram-project-react.git
```

Выполнить команду

```
docker-compose up --build -d
```

После запуска приложения в контейнере необходимо выполнить следующие команды

```
docker-compose exec backend python manage.py migrate — применить миграции
docker-compose exec backend python manage.py collectstatic --no-input — применить статику
docker-compose exec backend python manage.py load_ingredients - загрузка ингредиентов
```

### Доступ к сайту админке 
```
ip-адрес: http://51.250.68.56/recipes
login: admin
password: Linux_Password
```