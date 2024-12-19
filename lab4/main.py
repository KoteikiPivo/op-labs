import requests
import telebot
from bot_token import TOKEN

base_url = ("https://cdn.jsdelivr.net/npm/@fawazahmed0/"
            "currency-api@latest/v1/currencies/%s.json")

responses = {
    "start": "Use /help to see what this bot can do",
    "help": ("This bot can list exchange rates for a currency and convert a "
             "sum to another currency.\nCommands:\n"
             "/help - print this message\n"
             "/checkrate - check an exchange rate for a currency\n"
             "/checkall - check all exchange rates for a currency\n"
             "/convert - convert a value to another currency"),
    "checkall1": "Enter the currency to check all rates for:",
    "checkall2": "Currency rates for %s:\n%s",
    "checkrate1": "Enter the currency to check rate for:",
    "checkrate2": "Enter the second currency:",
    "checkrate3": "1 %s == %s %s",
    "convert1": "Enter the currency to convert from:",
    "convert2": "Enter the currency to convert to:",
    "convert3": "Enter value to convert:",
    "convert4": "%s %s == %s %s",
    "invalid": "Invalid response. Please try the command again"
}

bot = telebot.TeleBot(TOKEN)
bot.set_my_commands([
    telebot.types.BotCommand("/start", "Start the bot"),
    telebot.types.BotCommand("/help", "Type out help message"),
    telebot.types.BotCommand("/checkrate", "Check the rate of a currency"),
    telebot.types.BotCommand("/checkall", "Check all rates of a currency"),
    telebot.types.BotCommand("/convert", "Convert value to another currency"),
])

values = {"first": "",
          "second": "",
          "page": 0,
          "p_rates": "",
          "p_rates_list": [],
          "last_p_message": None}
inline_markup = telebot.util.quick_markup({
    '<<': {'callback_data': 'back'},
    '>>': {'callback_data': 'forward'}
}, row_width=2)


def write_page_rates():
    values["p_rates"] = ""
    for rate in values["p_rates_list"][(values["page"] * 20):
                                       (values["page"] + 1) * 20:]:
        values["p_rates"] = (values["p_rates"] + rate[0].upper() +
                             "  " + str(round(rate[1], 5)) + "\n")
    values["p_rates"] = values["p_rates"][:-1]


def get_all_rates(base_cur):
    req = requests.get(base_url % base_cur)
    if req.status_code != 404:
        return req.json()[base_cur]
    else:
        return None


def get_rate(base_cur, conv_cur):
    rates = get_all_rates(base_cur)
    try:
        return rates[conv_cur]
    except KeyError:
        return None


def convert_currency_value(base_cur, conv_cur, value):
    pass


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_message(message.chat.id, responses["start"])


@bot.message_handler(commands=["help"])
def send_help(message):
    bot.send_message(message.chat.id, responses["help"])


@bot.message_handler(commands=["checkrate"])
def check_currency(message):
    bot.send_message(message.chat.id, responses["checkrate1"])
    bot.register_next_step_handler(message, check_input_first)


def check_input_first(message):
    values["first"] = message.text
    if get_all_rates(values["first"]) is not None:
        bot.send_message(message.chat.id, responses["checkrate2"])
        bot.register_next_step_handler(message, check_input_second)
    else:
        bot.reply_to(message, responses["invalid"])


def check_input_second(message):
    values["second"] = message.text
    rate = get_rate(values["first"], values["second"])
    if rate is not None:
        bot.reply_to(message, responses["checkrate3"] %
                     (values["first"].upper(),
                      rate, values["second"].upper()))
    else:
        bot.reply_to(message, responses["invalid"])


@bot.message_handler(commands=["convert"])
def convert_currency(message):
    bot.send_message(message.chat.id, responses["convert1"])
    bot.register_next_step_handler(message, convert_input_first)


def convert_input_first(message):
    values["first"] = message.text
    if get_all_rates(values["first"]) is not None:
        bot.send_message(message.chat.id, responses["convert2"])
        bot.register_next_step_handler(message, convert_input_second)
    else:
        bot.reply_to(message, responses["invalid"])


def convert_input_second(message):
    values["second"] = message.text
    rate = get_rate(values["first"], values["second"])
    if rate is not None:
        values["p_rates"] = rate
        bot.send_message(message.chat.id, responses["convert3"])
        bot.register_next_step_handler(message, convert_input_third)
    else:
        bot.reply_to(message, responses["invalid"])


def convert_input_third(message):
    value = message.text
    try:
        converted = round(int(value) * values["p_rates"], 2)
        bot.send_message(message.chat.id,
                         responses["convert4"] %
                         (value, values["first"].upper(),
                          converted, values["second"].upper()))
    except ValueError:
        bot.reply_to(message, responses["invalid"])


@bot.callback_query_handler(func=lambda call: call.data == 'back')
def back_call(call):
    if values["page"] > 0:
        values["page"] -= 1
        write_page_rates()
        bot.edit_message_text(responses["checkall2"] %
                              (values["first"].upper(), values["p_rates"]),
                              call.message.chat.id,
                              call.message.message_id,
                              reply_markup=inline_markup)


@bot.callback_query_handler(func=lambda call: call.data == 'forward')
def forward_call(call):
    if values["page"] < 16:
        values["page"] += 1
        write_page_rates()
        bot.edit_message_text(responses["checkall2"] %
                              (values["first"].upper(), values["p_rates"]),
                              call.message.chat.id,
                              call.message.message_id,
                              reply_markup=inline_markup)
    else:
        bot.send_message(call.message.message_id, responses["invalid"])


@bot.message_handler(commands=["checkall"])
def check_all(message):
    if values["last_p_message"] is not None:
        bot.delete_message(*values["last_p_message"])
    bot.send_message(message.chat.id, responses["checkall1"])
    bot.register_next_step_handler(message, check_input_all)


def check_input_all(message):
    values["first"] = message.text
    values["page"] = 0
    values["p_rates_list"] = [(x, y) for x, y
                              in get_all_rates(values["first"]).items()]
    write_page_rates()
    if values["p_rates_list"] is not None:
        bot_message = bot.send_message(
            message.chat.id, responses["checkall2"] % (values["first"].upper(),
                                                       values["p_rates"]),
            reply_markup=inline_markup)
        values["last_p_message"] = (
            bot_message.chat.id, bot_message.message_id)
    else:
        bot.reply_to(message, responses["invalid"])


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()
