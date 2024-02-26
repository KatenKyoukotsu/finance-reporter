from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
import sqlite3
import matplotlib as pit
import io

class MainApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        button = Button(text='Show Graph', on_press=self.show_graph)
        self.image = Image()
        layout.add_widget(button)
        layout.add_widget(self.image)
        return layout

    def show_graph(self, instance):
        # Получение данных из базы данных
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM my_table")
        data = c.fetchall()
        conn.close()

        # Преобразование данных в формат, который можно использовать для построения диаграммы
        labels = [row[1] for row in data]
        sizes = [row[2] for row in data]

        # Создание диаграммы
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Сохранение диаграммы в буфер
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)

        # Загрузка диаграммы в виджет Kivy
        texture = Texture.create(size=(512, 512))
        texture.blit_buffer(buf.read(), colorfmt='rgba', bufferfmt='ubyte')
        self.image.texture = texture

if __name__ == '__main__':
    MainApp().run()