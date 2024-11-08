import sqlite3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class ProductSearchApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.label = Label(text="Введите штрихкод:")
        self.layout.add_widget(self.label)

        self.text_input = TextInput(hint_text="Штрихкод", size_hint_y=None, height=40)
        self.layout.add_widget(self.text_input)

        self.search_button = Button(text="Поиск", size_hint_y=None, height=40)
        self.search_button.bind(on_press=self.search_product)
        self.layout.add_widget(self.search_button)

        self.result_label = Label(text="", size_hint_y=None, height=40)
        self.layout.add_widget(self.result_label)

        return self.layout

    def search_product(self, instance):
        barcode = self.text_input.text
        if barcode:
            product = self.get_product_by_barcode(barcode)
            if product:
                self.result_label.text = f"Продукт: {product[1]}, Цена: {product[2]}"
            else:
                self.result_label.text = "Продукт не найден"
        else:
            self.result_label.text = "Введите штрихкод"

    def get_product_by_barcode(self, barcode):
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE barcode=?", (barcode,))
        product = cursor.fetchone()
        conn.close()
        return product

if __name__ == '__main__':
    ProductSearchApp().run()
