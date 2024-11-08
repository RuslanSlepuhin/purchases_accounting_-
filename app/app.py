import sqlite3
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

class ProductSearchApp(App):
    def build(self):
        self.layout = GridLayout(cols=1, padding=10, spacing=10, size_hint_y=1)
        self.layout.bind(minimum_height=self.layout.setter('height'))

        self.label = Label(text="Введите штрихкод:", size_hint_y=None, height=30)
        self.layout.add_widget(self.label)

        self.text_input = TextInput(hint_text="Штрихкод", size_hint_y=None, height=40)
        self.layout.add_widget(self.text_input)

        self.search_button = Button(text="Поиск", size_hint_y=None, height=40)
        self.search_button.bind(on_press=self.search_product)
        self.layout.add_widget(self.search_button)

        self.result_layout = GridLayout(cols=1, size_hint_y=None)
        self.result_layout.bind(minimum_height=self.result_layout.setter('height'))
        self.layout.add_widget(self.result_layout)

        return self.layout

    def search_product(self, instance):
        barcode = self.text_input.text
        if barcode:
            products = self.get_products_by_barcode(barcode)
            self.result_layout.clear_widgets()
            if products:
                for product in products:
                    product_label = Label(text=f"Продукт: {product[1]}, Цена: {product[2]}", size_hint_y=None, height=40)
                    self.result_layout.add_widget(product_label)

                    unit_input = TextInput(hint_text="Единица товара", size_hint_y=None, height=40)
                    self.result_layout.add_widget(unit_input)

                    quantity_input = TextInput(hint_text="Количество", size_hint_y=None, height=40)
                    self.result_layout.add_widget(quantity_input)

                    add_button = Button(text="Добавить", size_hint_y=None, height=40)
                    add_button.bind(on_press=lambda instance, p=product, u=unit_input, q=quantity_input: self.add_product(p, u, q))
                    self.result_layout.add_widget(add_button)
            else:
                self.result_layout.add_widget(Label(text="Продукт не найден", size_hint_y=None, height=40))
        else:
            self.result_layout.clear_widgets()
            self.result_layout.add_widget(Label(text="Введите штрихкод", size_hint_y=None, height=40))

    def add_product(self, product, unit_input, quantity_input):
        unit = unit_input.text
        quantity = quantity_input.text
        if unit and quantity:
            try:
                quantity = float(quantity)
                self.insert_product(barcode=product[1], name=product[2], price=product[3], unit=unit, quantity=quantity)
                self.result_layout.clear_widgets()
                self.result_layout.add_widget(Label(text=f"Продукт '{product[1]}' добавлен", size_hint_y=None, height=40))
            except ValueError:
                self.result_layout.clear_widgets()
                self.result_layout.add_widget(Label(text="Неверный формат количества", size_hint_y=None, height=40))
        else:
            self.result_layout.clear_widgets()
            self.result_layout.add_widget(Label(text="Заполните все поля", size_hint_y=None, height=40))

    def get_products_by_barcode(self, barcode):
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE barcode=?", (barcode,))
        products = cursor.fetchall()
        conn.close()
        return products

    def insert_product(self, barcode, name, price, unit, quantity):
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (barcode, name, price, unit, quantity) VALUES (?, ?, ?, ?, ?)", (barcode, name, price, unit, quantity))
        conn.commit()
        conn.close()

if __name__ == '__main__':
    ProductSearchApp().run()
