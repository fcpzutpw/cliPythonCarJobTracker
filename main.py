import json
import os


class JobTracker:
    def __init__(self, filename='jobs_data.json'):
        self.entries = []
        self.filename = filename
        self.exchange_rates = {
            'USD': 1.0,
            'RUB': 95.0,
            'KZT': 430.0
        }
        self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                self.entries = json.load(file)
        else:
            self.entries = []

    def save_data(self):
        with open(self.filename, 'w') as file:
            json.dump(self.entries, file)

    def add_entry(self, category, description, price, currency):
        if currency not in self.exchange_rates:
            print("Ошибка: неверная валюта.")
            return
        entry = {
            'category': category,
            'description': description,
            'price': price,
            'currency': currency
        }
        self.entries.append(entry)
        self.save_data()

    def convert_to_currency(self, amount, currency_from, currency_to):
        # Конвертация суммы из одной валюты в другую через базовую (USD)
        amount_in_usd = amount / self.exchange_rates[currency_from]
        return amount_in_usd * self.exchange_rates[currency_to]

    def get_summary(self, currency):
        if currency not in self.exchange_rates:
            print("Ошибка: неверная валюта.")
            return

        work_total = 0
        parts_total = 0
        expenses_total = 0

        for entry in self.entries:
            if 'category' not in entry or 'price' not in entry or 'currency' not in entry:
                continue

            converted_price = self.convert_to_currency(entry['price'], entry['currency'], currency)
            if entry['category'] == 'work':
                work_total += converted_price
            elif entry['category'] == 'parts':
                parts_total += converted_price
            elif entry['category'] == 'expenses':
                expenses_total += converted_price

        print(f"\nСводная таблица в {currency}:")
        print(f"Общая стоимость работ: {work_total:.2f} {currency}")
        print(f"Общая стоимость деталей: {parts_total:.2f} {currency}")
        print(f"Общие прочие расходы: {expenses_total:.2f} {currency}")


def main():
    job_tracker = JobTracker()

    while True:
        print("\n1. Добавить выполненную работу")
        print("2. Добавить покупку детали")
        print("3. Добавить прочие расходы")
        print("4. Показать сводную таблицу")
        print("5. Выйти")
        choice = input("Выберите действие: ")

        if choice == '1':
            description = input("Описание работы: ")
            price = float(input("Цена за работу: "))
            currency = input("Валюта (USD, RUB, KZT): ")
            job_tracker.add_entry('work', description, price, currency)

        elif choice == '2':
            description = input("Описание детали: ")
            price = float(input("Цена за деталь: "))
            currency = input("Валюта (USD, RUB, KZT): ")
            job_tracker.add_entry('parts', description, price, currency)

        elif choice == '3':
            description = input("Описание расхода: ")
            price = float(input("Сумма расхода: "))
            currency = input("Валюта (USD, RUB, KZT): ")
            job_tracker.add_entry('expenses', description, price, currency)

        elif choice == '4':
            currency = input("Валюта для сводной таблицы (USD, RUB, KZT): ")
            job_tracker.get_summary(currency)

        elif choice == '5':
            break

        else:
            print("Неверный выбор, попробуйте снова.")


if __name__ == "__main__":
    main()
