# Python3 RESTful API with Flask + Flask-SQLAlchemy + PostgreSQL + JWT

Contoh master project Restful API menggunakan python3. Ini hanya project belajar, silahkan jika ada yang ingin mengembangkan project ini.

## Instalation

Saya menggunakan python virtual environment `pipenv`,

```bash
pip3 install pipenv
```

Kemudian jalankan virtual environmentnya,

```bash
pipenv shell
```

Setelah berjalan, kemudian install semua _packages_,

```bash
pip3 install -r requirements.txt
```

## Running

```bash
python3 server.py
```

## Testing

Gunakan [insomnia](https://insomnia.rest/), [postman](https://www.postman.com/), [RapidAPI](https://rapidapi.com/products/api-testing/) atau API Tester lainnya untuk melakukan testing pada project ini. Saat testing, wajib memberikan attribut header berupa Authorization (token hasil generate saat login) dan X-API-KEY (API Key sesuai dengan yang di set pada file .env).

## License
[MIT](https://choosealicense.com/licenses/mit/)
