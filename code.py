import telebot
from telebot import types
from bs4 import BeautifulSoup
import requests

bot = telebot.TeleBot(token="6695056328:AAFpkP8agmEZ9ypFkOaLQOQWGY1RCdCMn4o")


@bot.message_handler(commands=['start'])
def start_bot(message):
  first_mess = f"<b>{message.from_user.first_name}</b>, привет!\nХочешь найти стихотворение?"
  markup = types.InlineKeyboardMarkup()
  button_yes = types.InlineKeyboardButton(text = 'Да', callback_data='yes')
  markup.add(button_yes)
  bot.send_message(message.chat.id, first_mess, parse_mode='html', reply_markup=markup)

@bot.callback_query_handler(func=lambda call:True)
def response(function_call):
  if function_call.message:
     if function_call.data == "yes":
        second_mess = "Напиши название стихотворения, которое желаешь найти"
        bot.send_message(function_call.message.chat.id, second_mess)
        bot.answer_callback_query(function_call.id)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    url = "https://www.culture.ru/literature/poems?query=" + message.text

    headers = {
        "Accept" : "*/*",
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    request = requests.get(url, headers=headers)
    soup = BeautifulSoup(request.text, "html.parser")

    links = soup.find_all("div", class_ = "_1ERrb")

    if len(links) > 0:
        url = "https://www.culture.ru" + links[0].find("a")["href"]
        request = requests.get(url, headers=headers)
        soup = BeautifulSoup(request.text, "html.parser")

        name_links = soup.find("div", class_="ipubq")
        poem_name = soup.find("div", class_="xtEsw")
        text = soup.find("div", class_="xZmPc")
        array = []
        array.append(name_links.get("data-author-title"))
        array.append('\n')
        array.append('\n')
        array.append(poem_name.text)
        tag_texts = text.find_all('div')
        for tags in tag_texts:
            brs = tags.find_all('br')
            try:
                text_before = brs[0].previous_sibling.strip()
            except Exception:
                break
            array.append('\n')
            array.append('\n')
            array.append(text_before)
            for br in brs:
                array.append('\n')
                text_after = br.next_sibling.strip()
                array.append(text_after)
        bot_message = ''
        for elem in array:
            bot_message += elem
        bot.send_message(message.from_user.id, bot_message)
        bot.send_message(message.from_user.id, 'Напиши название следующего стихотворения!')
    else:
        bot.send_message(message.from_user.id, 'Попробуй ввести другое название!')

bot.infinity_polling()


