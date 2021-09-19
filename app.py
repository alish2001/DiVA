import json
from web3 import Web3
from solcx import compile_source

# open the contract source
with open("contracts/ballot.sol",) as contract_file:
    contract = contract_file.read()

# Solidity source code
compiled_sol = compile_source(contract)

# retrieve the contract interface
contract_id, contract_interface = compiled_sol.popitem()

# get bytecode / bin
bytecode = contract_interface['bin']

# get abi
abi = contract_interface['abi']

# web3.py instance
url = "HTTP://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(url))

# set pre-funded account as sender
web3.eth.default_account = web3.eth.accounts[0]

Ballot = web3.eth.contract(abi=abi, bytecode=bytecode)

# Submit the transaction that deploys the contract
tx_hash = Ballot.constructor().transact()

# Wait for the transaction to be mined, and get the transaction receipt
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

web3.eth.defaultAccount = web3.eth.accounts[0]

#abi = json.loads(abi.read())

address = web3.toChecksumAddress("0xb8614e051e04e636cEcc5D243707F01cD70b4BdF")

contract = web3.eth.contract(address = address, abi = abi)


print("Connecting to ETH")
print(str(contract.functions.returnEntry().call()))
name = "Johhny"
name = input()
tx_hash = contract.functions.createCandidate(name).transact()

web3.eth.waitForTransactionReceipt(tx_hash)

print('Added new candidate: ', name)
# add list of candidates after update
