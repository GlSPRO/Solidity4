from web3 import Web3
from web3.middleware import geth_poa_middleware
import tkinter as tk
from contract_info import address_contract, abi

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Проверка подключения
if not w3.is_connected():
    print("Failed to connect to Ethereum node")
    exit(1)

# Подключение к смарт-контракту
contract = w3.eth.contract(address=address_contract, abi=abi)

# Проверка подключения
if not w3.is_connected():
    print("Ошибка подключения к узлу Ethereum")
    exit(1)

def validate_password(password):
    if len(password) < 12:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r"[!@#\$%\^&\*]", password):
        return False
    return True

def register():
    address = input("Введите адрес: ")
    while True:
        password = input("Введите пароль: ")
        if validate_password(password):
            break
        else:
            print("Пароль не соответствует требованиям безопасности. Попробуйте снова.")
    try:
        w3.geth.personal.new_account(password)
        print("Успешная регистрация")
        return address
    except Exception as e:
        print(f"Ошибка регистрации: {e}")
        return None

def login():
    address = input("Введите адрес: ")
    password = input("Введите пароль: ")
    try:
        w3.geth.personal.unlock_account(address, password)
        print("Успешная авторизация")
        return address
    except Exception as e:
        print(f"Ошибка авторизации: {e}")
        return None

def create_estate():
    address = input("Введите адрес учетной записи: ")
    size = int(input("Введите размер недвижимости: "))
    estate_address = input("Введите адрес недвижимости: ")

    print("Выберите тип недвижимости:")
    print("0: House")
    print("1: Flat")
    print("2: Loft")
    estate_type_index = int(input("Введите индекс типа недвижимости: "))

    if estate_type_index not in [0, 1, 2]:
        print("Неверный индекс типа недвижимости.")
        return

    try:
        tx_hash = contract.functions.createEstate(size, estate_address, estate_type_index).transact({'from': address})
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print("Недвижимость успешно создана. Hash транзакции:", tx_hash.hex())
    except Exception as e:
        print(f"Ошибка создания недвижимости: {e}")

def create_ad():
    address = input("Введите адрес учетной записи: ")
    estate_id = int(input("Введите ID недвижимости: "))
    price = int(input("Введите цену недвижимости: "))

    try:
        tx_hash = contract.functions.createAd(estate_id, price).transact({'from': address})
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print("Объявление успешно создано. Hash транзакции:", tx_hash.hex())
    except Exception as e:
        print(f"Ошибка создания объявления: {e}")

def change_estate_status():
    address = input("Введите адрес учетной записи: ")
    estate_id = int(input("Введите ID недвижимости: "))
    status = input("Введите новый статус (true/false): ").lower() == 'true'

    try:
        tx_hash = contract.functions.changeEstateStatus(estate_id, status).transact({'from': address})
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print("Статус недвижимости успешно изменен. Hash транзакции:", tx_hash.hex())
    except Exception as e:
        print(f"Ошибка изменения статуса недвижимости: {e}")

def change_ad_status():
    address = input("Введите адрес учетной записи: ")
    ad_id = int(input("Введите ID объявления: "))
    status = input("Введите новый статус (Opened/Closed): ")

    status_mapping = {
        'opened': 0,
        'closed': 1
    }

    if status.lower() not in status_mapping:
        print("Неверный статус объявления.")
        return

    try:
        tx_hash = contract.functions.changeAdStatus(ad_id, status_mapping[status.lower()]).transact({'from': address})
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print("Статус объявления успешно изменен. Hash транзакции:", tx_hash.hex())
    except Exception as e:
        print(f"Ошибка изменения статуса объявления: {e}")

def buy_estate():
    address = input("Введите адрес учетной записи: ")
    ad_id = int(input("Введите ID объявления: "))
    price_in_wei = int(input("Введите цену в Wei: "))  # Вводим цену непосредственно в Wei

    try:
        tx_hash = contract.functions.buyEstate(ad_id).transact({'from': address, 'value': price_in_wei})
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print("Недвижимость успешно куплена. Hash транзакции:", tx_hash.hex())
    except Exception as e:
        print(f"Ошибка покупки недвижимости: {e}")





def withdraw_funds():
    address = input("Введите адрес учетной записи: ")
    amount = int(input("Введите сумму для вывода: "))

    try:
        tx_hash = contract.functions.withdraw(amount).transact({'from': address})
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print("Средства успешно выведены. Hash транзакции:", tx_hash.hex())
    except Exception as e:
        print(f"Ошибка вывода средств: {e}")

def view_estates():
    try:
        estates = contract.functions.getEstate().call()
        for estate in estates:
            print(estate)
    except Exception as e:
        print(f"Ошибка получения информации о недвижимости: {e}")

def view_ads():
    try:
        ads = contract.functions.getAds().call()
        for ad in ads:
            print(ad)
    except Exception as e:
        print(f"Ошибка получения информации об объявлениях: {e}")

def view_balance():
    address = input("Введите адрес учетной записи: ")
    try:
        balance = contract.functions.getBalance().call({'from': address})
        print(f"Баланс на смарт-контракте: {balance}")
    except Exception as e:
        print(f"Ошибка получения информации о балансе: {e}")

def main():
    while True:
        print("1. Регистрация")
        print("2. Авторизация")
        print("3. Создание недвижимости")
        print("4. Создание объявления")
        print("5. Изменение статуса недвижимости")
        print("6. Изменение статуса объявления")
        print("7. Покупка недвижимости")
        print("8. Вывод средств")
        print("9. Просмотр информации о недвижимости")
        print("10. Просмотр информации об объявлениях")
        print("11. Просмотр баланса")
        print("12. Выход")
        choice = input("Выберите действие: ")

        if choice == '1':
            register()
        elif choice == '2':
            login()
        elif choice == '3':
            create_estate()
        elif choice == '4':
            create_ad()
        elif choice == '5':
            change_estate_status()
        elif choice == '6':
            change_ad_status()
        elif choice == '7':
            buy_estate()
        elif choice == '8':
            withdraw_funds()
        elif choice == '9':
            view_estates()
        elif choice == '10':
            view_ads()
        elif choice == '11':
            view_balance()
        elif choice == '12':
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()