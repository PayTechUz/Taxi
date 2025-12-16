# Taxi Backend

Foydalanuvchi balansiga to'lovlarni qabul qilish uchun mo'ljallangan backend loyiha. Payme va Click to'lov tizimlari orqali foydalanuvchilar o'z hamyonlarini to'ldirishlari mumkin.

## O'rnatish

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Sozlash

`.env.sample` faylini `.env` ga nusxalang va `PAYTECH_LICENSE_API_KEY` ni kiriting:

```bash
cp .env.sample .env
```

API kalitni olish uchun https://pay-tech.uz/console/ sahifasiga o'ting va litsenziya sotib oling.
