import os

from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Bot
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater
from telegram.utils.request import Request

from client.models import CustomClient, Product


def log_errors(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'Произошла ошибка: {e}'
            print(error_message)
            raise e

    return inner


@log_errors
def do_echo(update: Update, context: CallbackContext):
    static_directory = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))) + "\\static\\"
    chat_id = update.message.chat_id
    username = update.message.chat.username
    print(f"username {username}  type {type(username)}")
    if username is None:
        username = update.message.chat.first_name
    print(f"chat_id {chat_id}")
    print(f"context {context}")
    print(f"update.message {update.message}")
    print(f"update.message.chat {update.message.chat.username}")
    text = update.message.text
    reply_text = f'Ваш ID = {chat_id}\n Username {username} \n'
    update.message.reply_text(
        text=reply_text,
    )
    try:
        if "инвентарь" in text.lower():
            user = CustomClient.objects.get(telegram_username=username)
            print(f"user {user} user.pk  {user.pk}")
            print(f"dir user {dir(user)}")
            products = Product.objects.filter(user_pk=user.pk)
            print(f"products {products} products len {len(products)}")
            for pr in products:
                reply_text = f"Имя продукта {pr.title} \n"
                reply_text += f"Цена {pr.price} \n"
                reply_text += f"Описание {pr.description} \n"
                print(f"img {static_directory}{pr.product_img}")
                context.bot.send_photo(chat_id, photo=open(f"{static_directory}{pr.product_img}", 'rb'))
                update.message.reply_text(
                    text=reply_text,
                )
        elif "персонаж" in text.lower():
            user = CustomClient.objects.get(telegram_username=username)
            reply_text = f"Имя персонажа {user.game_username} \n"
            reply_text += f"Раса {user.race} \n"
            reply_text += f"Класс {user.class_name} \n"
            reply_text += f"История {user.history} \n"
            reply_text += f"Деньги {user.money} \n"
            context.bot.send_photo(chat_id, photo=open(f"{static_directory}{user.profile_avatar}", 'rb'))
            update.message.reply_text(
                text=reply_text,
            )
        else:
            reply_text = "Напиши инвентарь или персонаж"
            update.message.reply_text(
                text=reply_text,
            )


    except Exception as exc:
        reply_text = f'Ваш ID = {chat_id}\n Username {username} \n ты точно зареган? {exc}'
        update.message.reply_text(
            text=reply_text,
        )

    directory = os.path.dirname(os.path.realpath(__file__))
    file = f"{directory}//test.jpg"
    context.bot.send_photo(chat_id, photo=open(file, 'rb'))


@log_errors
def get_products(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id

    # p, _ = Profile.objects.get_or_create(
    #     external_id=chat_id,
    #     defaults={
    #         'name': update.message.from_user.username,
    #     }
    # )
    # count = Message.objects.filter(profile=p).count()
    user_pk = CustomClient.objects.get(chat_id=chat_id)
    products = Product.objects.filter(user_pk)
    count = 0
    update.message.reply_text(
        text=f'Ваши предметы {products}',
    )


class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **options):
        # 1 -- правильное подключение
        request = Request(
            connect_timeout=0.5,
            read_timeout=1.0,
        )
        bot = Bot(
            request=request,
            token=settings.TOKEN,
            base_url=getattr(settings, 'PROXY_URL', None),
        )
        print(bot.get_me())

        # 2 -- обработчики
        updater = Updater(
            bot=bot,
            use_context=True,
        )

        message_handler = MessageHandler(Filters.text, do_echo)
        updater.dispatcher.add_handler(message_handler)
        updater.dispatcher.add_handler(CommandHandler('count', get_products))

        # 3 -- запустить бесконечную обработку входящих сообщений
        updater.start_polling()
        updater.idle()
