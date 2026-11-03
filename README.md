# Channel Manager Bot

Telegram kanallarini boshqarish uchun bot: postlarni rejalashtirish,
majburiy obuna, statistika.

## Imkoniyatlar
- Rejalashtirilgan postlar va avtopost (APScheduler, UTC/zona bilan)
- Majburiy obuna tekshiruvi (middleware)
- FSM orqali post yaratish (matn + rasm)
- Ko'p tillilik: uz / ru / en (JSON tarjimalar)
- Statistika: SQL agregatsiyalar
- Faqat admin uchun buyruqlar

## Texnologiyalar
Python 3.12+, aiogram 3, SQLAlchemy 2 (async), asyncpg,
PostgreSQL, Alembic, APScheduler, pydantic-settings, uv

## Ishga tushirish
1. Repozitoriyani yuklab oling va bog'liqliklarni o'rnating:
   git clone https://github.com/mrFaxriddin1/channel-bot.git
   cd channel-bot
   uv sync
2. PostgreSQL'da baza va foydalanuvchi yarating.
3. `.env.example` dan `.env` nusxa oling va to'ldiring.
4. Migratsiyalarni qo'llang: `uv run alembic upgrade head`
5. Botni ishga tushiring: `uv run main.py`

## Buyruqlar
/start, /language, /help
Admin: /addchannel, /newpost, /stats

## Arxitektura
handlers → repositories → database, middlewares (db, i18n, obuna),
services (scheduler, obuna tekshiruvi)

## Keyingi yaxshilanishlar
- FSM holatini Redis'da saqlash
- Docker
- Testlar (pytest)
- Postlarni tahrirlash va o'chirish