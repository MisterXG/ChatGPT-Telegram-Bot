import openai
import telebot

openai.api_key = ''  # Your openai secret key
token = ''  # Your telegram bot token

bot = telebot.TeleBot(token)

role = [{'role': 'system', 'content': ''}]  # Here you should write whose role ChatGPT will play
conversations = {}


@bot.message_handler(commands=['start'])
def start(message):
    global role
    conversations.update({message.from_user.id: role})
    msg = bot.send_message(message.chat.id, 'Hello, my name is ChatGPT and I can answer almost every questsion! Ask '
                                            'me anything')


@bot.callback_query_handler(func=lambda data: True)
def reset(data):
    global role
    d = data.data.split('[]')
    conversations[int(d[0])] = role
    bot.send_message(int(d[1]), 'Dialogue reset successfully!')


@bot.message_handler(content_types=['text'])
def chatgpt(message):
    completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=conversations[message.from_user.id],
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7, )
    keyboard = telebot.types.InlineKeyboardMarkup()
    reset_button = telebot.types.InlineKeyboardButton(text='reset dialogue',
                                                      callback_data=f'{message.from_user.id}[]{message.chat.id}')
    keyboard.add(reset_button)
    response = completion.choices[0].message.content
    conversations[message.from_user.id].append({'role': 'user', 'content': message.text})
    conversations[message.from_user.id].append({'role': 'assistant', 'content': response})
    bot.send_message(message.chat.id, response, reply_markup=keyboard)


bot.polling(non_stop=True)
