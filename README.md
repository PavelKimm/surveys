# surveys

## Инструкция по использованию
* ### Для начала работы необходимо установить Docker и Docker-compose

* ### Склонируйте репозиторий в нужную папку
<code> git clone https://github.com/PavelKimm/surveys.git . </code>

* ### Запустите docker-compose
<code> sudo docker-compose up --build </code>

* ### Для создания суперпользователя можно воспользоваться следующими командами в консоли
<code> sudo docker exec -it surveys bash </code>
<code> python manage.py createsuperuser </code>
