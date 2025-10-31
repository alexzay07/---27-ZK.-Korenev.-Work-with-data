import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Получение токена из переменных окружения
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not TOKEN:
    raise ValueError("Не найден TELEGRAM_BOT_TOKEN в переменных окружения!")

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправка приветственного сообщения при команде /start."""
    user = update.effective_user
    await update.message.reply_text(
        f'Привет, {user.first_name}! Я бот для работы с данными.\n'
        f'Используй /help для списка команд.'
    )

# Обработчик команды /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправка справки о доступных командах."""
    help_text = (
        "Доступные команды:\n"
        "/start - Начать работу с ботом\n"
        "/help - Показать эту справку\n"
        "/info - Получить информацию о боте\n"
    )
    await update.message.reply_text(help_text)

# Обработчик команды /info
async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправка информации о боте."""
    info_text = (
        "Бот для работы с данными\n"
        "Версия: 1.0\n"
        "Проект: Work with data - 27 ZK Korenev"
    )
    await update.message.reply_text(info_text)

# Обработчик текстовых сообщений
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Эхо-ответ на текстовые сообщения."""
    await update.message.reply_text(f'Вы написали: {update.message.text}')

# Обработчик ошибок
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Логирование ошибок."""
    logger.error('Exception while handling an update:', exc_info=context.error)

def main() -> None:
    """Запуск бота."""
    # Создание приложения
    application = Application.builder().token(TOKEN).build()

    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("info", info_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Регистрация обработчика ошибок
    application.add_error_handler(error_handler)

    # Запуск бота
    logger.info("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
