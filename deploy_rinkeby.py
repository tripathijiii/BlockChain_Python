from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    print(simple_storage_file)

# installing solc
install_solc("0.6.0")


# Compile our solidity
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)


# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]


# for connecting to gnache
w3 = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/9a92b2fc54f440bbb5c194d678bb1614")
)
chain_id = 4
my_address = "0x4fCC5058b5B64f7218444F41ba26fFbE08eE3088"
# export privatekey to os or use a dotenv
private_key = os.getenv(("Private_Key2"))

# Create the contract in Python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)

# build a transaction
# Sign a transaction
# Send a transaction
transaction = SimpleStorage.constructor().build_transaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)
# Signing a transaction
print("working...")
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# Send the signed Transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
# waiting for confirmation
print("working...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)


# working with the Contract
# we need :-
# 1. Contract address
# 2. Contract ABI

simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# Call -> simulate making the call and getting a return value
# Transact -> Actually makes a state change
print(simple_storage.functions.retrieve().call())
print("working...")
store_transaction = simple_storage.functions.store(15).build_transaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce + 1,
    }
)
signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
transaction_hash = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash=transaction_hash)
print(simple_storage.functions.retrieve().call())
