from web3 import Web3
from web3.middleware import geth_poa_middleware
from contract_info import address_contract, abi

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
contract = w3.eth.contract(address=address_contract, abi=abi)
# print(contract.address)
# print(w3.eth.get_balance('0xef96AD0cea45ab622140E4b93C77c22c6Db267a0'))

accounts = w3.eth.accounts

for i in range(len(accounts)):
    print(f"Адрес аккаунта {i+1}: {w3.eth.get_balance(accounts[i])}")