from openai import OpenAI
import telebot

api_key = ''  # Your openai secret key
token = ''  # Your telegram bot token

bot = telebot.TeleBot(token)
client = OpenAI(api_key=api_key)

role = ''  # Here you should write whose role ChatGPT will play
conversations = {}


@bot.message_handler(commands=['start'])
def start(message):
    global role
    conversations.update({message.from_user.id: [{'role': 'system', 'content': role}]})
    bot.send_message(message.chat.id, 'Hello, my name is ChatGPT and I can answer almost every questsion! Ask me anything')


@bot.callback_query_handler(func=lambda data: True)
def reset(data):
    global role
    conversations[data.from_user.id] = [{'role': 'system', 'content': role}]
    bot.send_message(data.message.chat.id), 'Dialogue reset successfully!')


@bot.message_handler(content_types=['text'])
def chatgpt(message):
    conversations[message.from_user.id].append({'role': 'user', 'content': message.text})
    completion = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=conversations[message.from_user.id]
    )
    keyboard = telebot.types.InlineKeyboardMarkup()
    reset_button = telebot.types.InlineKeyboardButton(text='reset dialogue')
    keyboard.add(reset_button)
    response = completion.choices[0].message.content
    conversations[message.from_user.id].append({'role': 'assistant', 'content': response})
    bot.send_message(message.chat.id, response, reply_markup=keyboard)


bot.polling(non_stop=True)
