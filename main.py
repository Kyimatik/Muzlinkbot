import telebot
from telebot import types
import os
import yt_dlp
from concurrent.futures import ThreadPoolExecutor
import json


TOKEN = '?'
GROUP_ID = -?

bot = telebot.TeleBot(TOKEN)
AWAITING_VIDEO_LINK = 2

waiting_feedback = {}
user_states = {}




BASE_PATH = '/home/amantur/bot'

executor = ThreadPoolExecutor()


STATS_FILE_PATH = '?'



def load_stats():
    try:
        with open(STATS_FILE_PATH, 'r') as stats_file:
            stats_data = json.load(stats_file)
            if 'unique_users_count' not in stats_data:
                stats_data['unique_users_count'] = 0
            stats_data['unique_users'] = set(stats_data['unique_users'])
            return stats_data
    except FileNotFoundError:
        print("Stats file not found.")
        return {'unique_users': set(), 'unique_users_count': 0, 'videos_sent': 0}
    except json.JSONDecodeError as e:
        print(f"Error loading stats: {e}")
        return {'unique_users': set(), 'unique_users_count': 0, 'videos_sent': 0}

def save_stats(stats):
    with open(STATS_FILE_PATH, 'w') as stats_file:
        json.dump(stats, stats_file, default=list)



def process_message(message):
    user_id = message.from_user.id

    # Проверяем, что сообщение пришло из личного чата (private chat)
    if message.chat.type == 'private':
        if message.text == '/start':
            handle_start(message)
        elif message.text == '/help':
            handle_help(message)
        elif 'https' in message.text and 'youtu' in message.text:
            handle_media_link(message)
        elif message.text == '/founder':
            handle_founder(message)
        elif message.text == '/feedback':
            handle_feedback_command(message)
        elif message.text == '/stats':
            send_stats_to_group(message)
        else:
            bot.delete_message(message.chat.id, message.message_id)
    else:
        # Если сообщение пришло из группового чата
        if message.text.startswith('/'):
            # Если сообщение является командой, игнорируем его
            return


def handle_start(message):
    user_name = message.from_user.first_name
    photo_file_path1 = '/home/amantur/bot/audios/gifs/Принцип работы бота.png'
    with open(photo_file_path1, 'rb') as photo_file:
        bot.send_photo(message.from_user.id, photo_file)
    bot.send_message(message.from_user.id, f"""Hello👋, {user_name} ! Чтобы начать работать, вставьте ссылку на музыку 💿 или плейлист📜!


<b>❗❗️ Файл отправляется в формате WEBM, а не mp3 ❗️❗️</b>
""",parse_mode="HTML",reply_markup=types.ReplyKeyboardRemove())



def handle_founder(message):
    if message.chat.type == 'private':
        #gif_file_path = '/home/amantur/bot/audios/gifs/ichigo.gif'
        bot.send_message(message.chat.id, """Все соцальные сети создателей⬛️:
Instagram - https://www.instagram.com/emirlanchikk
Telegram - @bumizxc
Tik Tok - https://www.tiktok.com/@emirlan4ik_?_t=8jpJgkrC8qg&_r=

Instagram - https://www.instagram.com/akbarrych
Telegram - @Akbarrych
Tik Tok - https://www.tiktok.com/@kchkvkbr?_t=8jpJXhQqtmh&_r=1
Просим вас подписаться на наши  Соц-сети , так вы поддерживаете нас тем самым улучшая наш проект.❤️
        """,reply_markup=types.ReplyKeyboardRemove())


def handle_feedback_command(message):
    if message.chat.type == 'private':
        user_id = message.from_user.id
        waiting_feedback[user_id] = True
        bot.send_message(message.chat.id,
                          "Здесь вы можете оставить свои комментарии и предложения по улучшению бота.⚡\n"
                          "Чтобы оставить комментарий, просто напишите свои пожелания, и это, конечно же, дойдет до основателя!\n"
                          "Напишите свой отзыв:",reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, handle_feedback_message)
    else:
        pass


def handle_feedback_message(message):
    user_id = message.from_user.id
    user_name = message.from_user.username
    user_feedback = message.text

    # Отправляем пожелания в группу
    group_text = f"Пользователь @{user_name} (ID: {user_id}) отправил пожелания: {user_feedback}"
    bot.send_message(GROUP_ID, group_text)

    # Отправляем благодарность пользователю
    bot.send_message(message.chat.id, "Спасибо за ваш отзыв! Он отправлен для обработки.")
    waiting_feedback[user_id] = False











def handle_help(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # Создаем кнопки
    start_button = types.KeyboardButton("/start")
    founder_button = types.KeyboardButton("/founder")
    feedback_button = types.KeyboardButton("/feedback")

    # Добавляем кнопки к разметке
    markup.add(start_button)
    markup.add(founder_button, feedback_button)

    # Отправляем сообщение с разметкой и текстом
    bot.send_message(
        message.from_user.id,
        """Список команд Бота 🤖:
/help - [Информация о всех существующих командах]✅
/start - [Команда старт, начало работы]🚀
/feedback - [Обратная связь с нами. Советы, как можно улучшить бота и т.д]🔛
/founder - [Про основателя]👨🏼‍�
*⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇-Как скачать музыку*
*Чтобы скачать музыку🎼*
Просто вставьте ссылку🔗 на видео или плейлист из YouTube в любое место в боте и он скачает вам.
Приятного использования дорогие подписчики,🙌❤""",
        reply_markup=markup
    )



#@bot.message_handler(commands=['reklama'])
#def reklama(message):
#    inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
#
#    # Создаем инлайн-кнопку с ссылкой
#    inline_button = types.InlineKeyboardButton(text='Бесплатная музыка🎶', url='t.me/muzlinkbot')
#
#    # Добавляем кнопку на клавиатуру
#    inline_keyboard.add(inline_button)
#
#    bot.send_message(message.from_user.id,'Скачай свою любимую <a href="http://t.me/muzlinkbot">музыку</a> бесплатно без подписок на каналы😘',reply_markup=inline_keyboard,parse_mode="HTML")


#handle media link  *func*

def handle_media_link(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    user_name = message.from_user.first_name
    bot.send_message(chat_id, f"Уважаемый(ая) {user_name}! Просим поднабраться терпения. Ваше аудио скачивается🔜🎵 С Уважением команда STE🖤")

    try:
        media_link = message.text
        audio_paths = download_media_audio(media_link, chat_id)
        for audio_path in audio_paths:
            send_audio(chat_id, audio_path)
            stats = load_stats()

            if message.from_user.id not in stats['unique_users']:
                user_info = f"{message.from_user.id}-@{message.from_user.username}"
                stats['unique_users'].add(user_info)
                stats['unique_users_count'] = len(stats['unique_users'])



                # Сохраняем обновленную статистику
                save_stats(stats)

    except yt_dlp.utils.DownloadError as e:
        if 'is not a valid URL' in str(e):
            bot.send_message(chat_id, f"{user_name} Неправильная ссылка. Пожалуйста, убедитесь, что вы правильно ее скопировали.")
        elif 'entity too large' in str(e):
            bot.send_message(chat_id, "Извините, видео слишком большое. Пожалуйста, попробуйте другую ссылку.")
        else:
            if 'The playlist does not exist' in str(e):
                bot.send_message(chat_id, f"""Уважаемый(ая) {user_name}, ваш плейлист не удалось найти.
Это может означать, что у вас ограниченный доступ к вашему плейлисту.
Чтобы это исправить, вам нужно изменить параметры доступа вашего плейлиста.""")
                photo_file_path1 = '/home/amantur/bot/audios/gifs/ИНСТ 1.jpg'
                with open(photo_file_path1, 'rb') as photo_file:
                    bot.send_photo(chat_id, photo_file)
                photo_file_path2 = '/home/amantur/bot/audios/gifs/ИНСТ 2.jpg'
                with open(photo_file_path2, 'rb') as photo_file:
                    bot.send_photo(chat_id, photo_file)
                return []
            else:
                error_message = f"Произошла ошибка при скачивании аудио из плейлиста: {e}"
                bot.send_message(chat_id, error_message)
                return []
    except Exception as e:
        bot.send_message(chat_id, f"Произошла непредвиденная ошибка: {e}")
    finally:
        # В этом варианте не требуется удаление маркеров или файлов
        pass

def download_media_audio(url, chat_id):
    if "/playlist" in url:
        return download_playlist_audio(url, chat_id)
    else:
        return [download_audio(url, chat_id)]


def download_audio(url, chat_id):
    download_folder = BASE_PATH
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(download_folder, '%(title)s'),
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        # Проверяем размер файла (в байтах)
        max_file_size_bytes = 50 * 1024 * 1024  # 50 МБ

        if 'filesize' in info and info['filesize'] > max_file_size_bytes:
            error_message = "Файл слишком большой. Пожалуйста, выберите видео у которого аудио меньше 50мб."
            bot.send_message(chat_id, error_message)
            return None

        ydl.download([url])

    return os.path.join(download_folder, ydl.prepare_filename(info))


def check_file_size(d):
    max_file_size_bytes = 50 * 1024 * 1024  # 50 МБ
    if 'filesize' in d and d['filesize'] > max_file_size_bytes:
        return {'download': False,
                'message': f"Файл '{d['title']}' слишком большой и не будет скачан. Пожалуйста, выберите видео менее 50 МБ."}
    return {'download': True}


def download_playlist_audio(url, chat_id):
    download_folder = BASE_PATH
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(download_folder, '%(title)s'),
        'progress_hooks': [check_file_size],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        ydl.download([url])

    valid_entries = [entry for entry in info['entries'] if
                     os.path.exists(os.path.join(download_folder, ydl.prepare_filename(entry)))]

    if not valid_entries:
        error_message = "Все файлы в плейлисте слишком большие и не будут скачаны. Пожалуйста, выберите видео менее 50 МБ."
        bot.send_message(chat_id, error_message)
        return []

    return [os.path.join(download_folder, ydl.prepare_filename(entry)) for entry in valid_entries]


def send_audio(chat_id, audio_path):
    text_message = "[🔍Скачать любимую музыку⚡️](t.me/muzlinkbot)"
    try:
        if audio_path is None:
            raise ValueError("Ваше видео не было скачано, поэтому попробуйте еще раз!) 🙏 ")

        with open(audio_path, 'rb') as audio_file:
            bot.send_audio(chat_id, audio_file, caption=text_message, parse_mode="MarkdownV2")
            stats = load_stats()

            # Обновляем количество отправленных видео
            stats['audios_sent'] += 1

            # Сохраняем обновленную статистику
            save_stats(stats)
        #bot.send_message(chat_id,"‼️Файл отправлен в формате <b>webm</b> а не <i>mp3</i>‼️",parse_mode="HTML")
    except Exception as e:
        error_message = f"Произошла ошибка при отправке аудио: {e}"
        if 'Entity Too Large' in error_message:
            bot.send_message(chat_id,
                             f"Файл {os.path.basename(audio_path)} не отправился из-за слишком большого веса. Просим вас, попробуйте еще раз!♻")
        else:
            bot.send_message(chat_id, error_message)
    finally:

            # Вне зависимости от того, произошла ошибка или нет, удаляем файл
        os.remove(audio_path)


def send_stats_to_group(message):
    try:
        # Загружаем текущую статистику
        stats = load_stats()

        # Отладочный вывод
        print(f"Before sending to group - Unique Users: {len(stats['unique_users'])}, Videos Sent: {stats['audios_sent']}")

        # Сохраняем обновленную статистику
        save_stats(stats)

        # Отправляем статистику в группу
        stats_message = f"Уникальных пользователей: {len(stats['unique_users'])}\nВсего отправлено аудио: {stats['audios_sent']}"
        bot.send_message(GROUP_ID, stats_message)

    except Exception as e:
        print(f"Error sending stats to group: {e}")
        bot.send_message(message.chat.id, "Произошла ошибка при отправке статистики в группу.")




# Обработчик всех сообщений
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_id = message.from_user.id

    # Проверяем, что сообщение пришло из личного чата (private chat)
    if message.chat.type == 'private':
        if user_id not in user_states:
            user_states[user_id] = {'state': 'start'}
        executor.submit(process_message, message)
    else:
        # Если сообщение пришло из группового чата
        if message.text.startswith('/'):
            # Если сообщение является командой, игнорируем его
            return
        else:
            # Если сообщение из группового чата не является командой, обрабатываем его
            executor.submit(process_message, message)


if __name__ == '__main__':
    bot.polling(none_stop=True)
