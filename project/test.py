from unittest.mock import MagicMock
import Bot_file

def test_text_function():
    message = MagicMock()
    Bot_file.bot = MagicMock()
    message.text = "Отели"
    Bot_file.text(message)
    assert Bot_file.bot.send_message.call_count == 1

def test_text_function_fail():
    message = MagicMock()
    Bot_file.bot = MagicMock()
    message.text = "двлждыплждвлап"
    Bot_file.text(message)
    assert Bot_file.bot.send_message.call_count == 0

def test_text_room_function():
    message = MagicMock()
    Bot_file.bot = MagicMock()
    message.text = "назад"
    Bot_file.room(message,'-_-')
    assert Bot_file.bot.send_message.call_count == 1
    assert Bot_file.bot.send_message.call_args_list[0][0][1] == "Выберите категорию"