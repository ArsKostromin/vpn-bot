
# 🤖 VPN-Бот для Telegram

✅ Бот для продажи VPN-подписок с пополнением через крипту, Robokassa и Telegram Stars  
✅ Удобная админка на Django: задаём тарифы, управляем подписками, серверами и VLESS-конфигами  
✅ Автоматическая генерация VLESS после оплаты  

---

## 📋 Основные функции бота

1. **Пополнение баланса**
   - Через **криптовалюту** (через Cryptomus)
   - Через **Robokassa**
   - Через **звёзды Telegram** (ссылка-оплата)

2. **Покупка VPN**
   - Пользователь выбирает: тип VPN → страну → длительность
   - Бот списывает средства, создаёт подписку и выдаёт VLESS-ссылку

3. **Просмотр профиля**
   - Баланс
   - Реферальная ссылка

4. **Реферальная система**
   - Получение бонусов за приглашённых друзей

5. **Просмотр активных VPN**
   - Список купленных подписок
   - Ссылки на конфиги (в т.ч. в формате VLESS)

---

## ⚙️ Настройка и запуск

### 1. Клонирование

```bash
git clone https://github.com/ArsKostromin/vpn-bot.git
cd vpn-bot
````

### 2. Установка зависимостей

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Настройка `.env`

Создайте `.env` на основе `.env.example` и укажите:

```dotenv
BOT_TOKEN=...
DJANGO_SECRET_KEY=...
DATABASE_URL=postgres://...
ROBOKASSA_LOGIN=...
ROBOKASSA_PASSWORD1=...
ROBOKASSA_PASSWORD2=...
CRYPTO_WALLETS=btc:...,eth:...
STARS_PAYMENT_URL=https://...
REFERRAL_BONUS=50
```

### 4. Миграции и суперпользователь

```bash
./manage.py migrate
./manage.py createsuperuser
```

### 5. Запуск

```bash
./manage.py runserver 0.0.0.0:8000
python bot.py
```

---

## 🛠 Админка

Для управления пользователями, тарифами и серверами используется отдельная админка:
🔗 [https://github.com/ArsKostromin/vpnbot](https://github.com/ArsKostromin/vpnbot)

---

## 🔄 Как работает покупка VPN

1. Пользователь нажимает "Купить VPN"
2. Бот предлагает тарифы из Django
3. После выбора и оплаты вызывается FastAPI на сервере
4. Создаётся VLESS-конфиг и сохраняется в `Subscription`
5. Ссылка отправляется пользователю

---

## ✅ Проверка работы

* `/profile` — профиль, баланс, реферальная ссылка
* `/subscriptions` — активные подписки
* Пополнение через любую из систем
* Проверка генерации конфигов после оплаты

---

## ✨ Итоги

* Полноценный VPN-магазин в Telegram
* Поддержка Robokassa, криптовалют и Telegram Stars
* Удобное управление через Django-админку
* Подписки с VLESS-генерацией и реферальной системой
* промокоды и скидки

```
