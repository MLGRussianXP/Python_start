from PyQt5.QtWidgets import *
import os
import json

app = QApplication([])

'''Интерфейс приложения'''
notes_win = QWidget()
notes_win.setWindowTitle('Умные заметки')
notes_win.resize(900, 600)

list_notes = QListWidget()
list_notes_label = QLabel('Список заметок')

button_note_create = QPushButton('Создать заметку')
button_note_del = QPushButton('Удалить заметку')
button_note_save = QPushButton('Сохранить заметку')

field_tag = QLineEdit('')
field_tag.setPlaceholderText('Введите тег...')
field_text = QTextEdit()
button_tag_add = QPushButton('Добавить к заметке')
button_tag_del = QPushButton('Открепить от заметки')
button_tag_search = QPushButton('Искать заметки по тегу')
list_tags = QListWidget()
list_tags_label = QLabel('Список тегов')

layout_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_1.addWidget(field_text)

col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)
row_1 = QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)
row_2 = QHBoxLayout()
row_2.addWidget(button_note_save)
col_2.addLayout(row_1)
col_2.addLayout(row_2)

col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)
row_3 = QHBoxLayout()
row_3.addWidget(button_tag_add)
row_3.addWidget(button_tag_del)
row_4 = QHBoxLayout()
row_4.addWidget(button_tag_search)

col_2.addLayout(row_3)
col_2.addLayout(row_4)

layout_notes.addLayout(col_1, stretch=2)
layout_notes.addLayout(col_2, stretch=1)
notes_win.setLayout(layout_notes)

'''Функционал приложения'''


def show_note():
    # ничего не изменилось
    key = list_notes.selectedItems()[0].text()
    field_text.setText(notes[key]["текст"])
    list_tags.clear()
    list_tags.addItems(notes[key]["теги"])


def add_note():
    while True:
        note_name, ok = QInputDialog.getText(notes_win, "Добавить заметку", "Название заметки: ")
        ''' метод .strip() очищает строку от пробелов слева и справа от слов'''
        if ok and note_name.strip():
            if not os.path.exists(os.path.join('Notes', note_name.strip() + '.json')):
                notes[note_name.strip()] = {"текст": "", "теги": []}
                list_notes.addItem(note_name.strip())
                list_tags.addItems(notes[note_name.strip()]["теги"])
                break
            else:
                QMessageBox(icon=QMessageBox.Warning, text='Придумай другое имя!').exec_()
        else:
            QMessageBox(icon=QMessageBox.Warning, text='Ой всё!').exec_()
            break


def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]["текст"] = field_text.toPlainText().strip()
        print(os.path.join('Notes', key + '.json'))
        with open(os.path.join('Notes', key + '.json'), "w", encoding='utf-8') as file:
            json.dump(notes, file, ensure_ascii=False)
    else:
        QMessageBox(icon=QMessageBox.Warning, text='Заметка для сохранения не выбрана!').exec_()


def remove_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes)
        if os.path.exists(os.path.join('Notes', key + '.json')):
            os.remove(os.path.join('Notes', key + '.json'))
    else:
        QMessageBox(icon=QMessageBox.Warning, text='Заметка для удаления не выбрана!').exec_()


# теги
def add_tag():
    if list_notes.selectedItems():
        if field_tag.text().strip():
            key = list_notes.selectedItems()[0].text()
            tag = field_tag.text().strip()
            if tag not in notes[key]["теги"]:
                notes[key]["теги"].append(tag)
                list_tags.addItem(tag)
                field_tag.clear()
                with open(os.path.join('Notes', key + '.json'), "w", encoding='utf-8') as file:
                    json.dump(notes, file, ensure_ascii=False)
            else:
                QMessageBox(icon=QMessageBox.Warning,
                            text='Такой тег уже есть в списке тегов, придумай что-нибудь новенькое!').exec_()
        else:
            QMessageBox(icon=QMessageBox.Warning, text='Тег не может быть пустым! Пробелы не считаются!').exec_()
    else:
        QMessageBox(icon=QMessageBox.Warning, text='Заметка для добаления тега не выбрана!').exec_()


def del_tag():
    if list_tags.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]["теги"].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]["теги"])
        with open(os.path.join('Notes', key + '.json'), "w", encoding='utf-8') as file:
            json.dump(notes, file, ensure_ascii=False)
    else:
        QMessageBox(icon=QMessageBox.Warning, text='Тег для удаления не выбран!').exec_()


def search_tag():
    tag = field_tag.text().strip()
    if button_tag_search.text() == "Искать заметки по тегу":
        if tag:
            notes_filtered = {}
            for note in notes:
                if tag in notes[note]["теги"]:
                    notes_filtered[note] = notes[note]
            button_tag_search.setText("Сбросить поиск")
            list_notes.clear()
            list_tags.clear()
            list_notes.addItems(notes_filtered)
        else:
            QMessageBox(icon=QMessageBox.Warning, text='Прежде чем что-то искать, нужно что-то ввести!').exec_()
            field_tag.clear()
            field_tag.setFocus()
    elif button_tag_search.text() == "Сбросить поиск":
        field_tag.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        button_tag_search.setText("Искать заметки по тегу")


list_notes.itemClicked.connect(show_note)
button_note_create.clicked.connect(add_note)
button_note_save.clicked.connect(save_note)
button_note_del.clicked.connect(remove_note)
button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(del_tag)
button_tag_search.clicked.connect(search_tag)

notes_win.show()
notes = {}

if not os.path.exists('Notes'):
    os.makedirs('Notes')

''' Метод .endswith проверяет заканчивается ли строка на переданный параметр. На выходе True или False. 

    os.listdir(<Опциональный путь до папки>) возвращает список файлов и папок в указанной папке, если 
    не указать параметр, то вернется список файлов и папок из директорий откуда произошёл запуск программы.
    На всякий случай, метод .update() добавляет/обновляет в словарь пару ключ-значение.
'''

if len(os.listdir('Notes')) > 0:
    for item in os.listdir('Notes'):
        if item.endswith('json'):
            with open(os.path.join('Notes', item), "r", encoding='utf-8') as file:
                note = json.load(file)
                notes.update(note)
list_notes.addItems(notes)
app.exec_()
