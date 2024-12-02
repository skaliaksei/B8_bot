from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Хранилище для расписания (пока в памяти)
schedule = {}

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот для управления расписанием вентиляционной системы.\n"
        "Доступные команды:\n"
        "/change - Изменить расписание\n"
        "/list - Показать текущее расписание"
    )

# Команда /list
async def list_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not schedule:
        await update.message.reply_text("Расписание пустое.")
    else:
        message = "Текущее расписание:\n"
        for day, times in schedule.items():
            message += f"{day.capitalize()}: Active: {times['active']} Inactive: {times['inactive']}\n"
        await update.message.reply_text(message)

# Команда /change
async def change_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Получение аргументов из команды
        args = context.args
        if len(args) != 3:
            await update.message.reply_text("Формат команды: /change <day> <active_time> <inactive_time>")
            return

        day, active_time, inactive_time = args[0].lower(), args[1], args[2]

        # Обновление расписания
        schedule[day] = {"active": active_time, "inactive": inactive_time}
        await update.message.reply_text(
            f"Расписание для {day.capitalize()} обновлено:\nActive: {active_time}\nInactive: {inactive_time}"
        )
    except Exception as e:
        await update.message.reply_text("Произошла ошибка. Проверьте формат команды.")

# Основная функция
def main():
    # Ваш токен от BotFather
    TOKEN = "7458392842:AAEg1PE5ll2UDybWyyUkNdrOPM8V3ZcHSho"
    # TOKEN = "TEST"

    # Создание приложения
    application = Application.builder().token(TOKEN).build()

    # Регистрация обработчиков команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("list", list_schedule))
    application.add_handler(CommandHandler("change", change_schedule))

    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    main()
