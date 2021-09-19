import json
import time
from web3 import Web3
from solcx import compile_source


# web3.py instance
url = "HTTP://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(url))

# set pre-funded account as sender
web3.eth.default_account = web3.eth.accounts[0]

def newContract(listOfCandidates):

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

    Ballot = web3.eth.contract(abi=abi, bytecode=bytecode)
    '''
    # Submit the transaction that deploys the contract
    tx_hash = Ballot.constructor(["Johhny","Michael"]).transact()

    # Wait for the transaction to be mined, and get the transaction receipt
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    address = tx_receipt['contractAddress']
    '''
    address = "0x95A49A5e402A894D7f186781610b3e7f2fb1a33D"
    return address,abi,bytecode

'''
    address_file = open("addresses",'w')
    address_file.write(address)
    address_file.close()

    abi_file = open("abi",'w')
    abi_file.write(abi)
    abi_file.close()

    bytecode_file = open("addresses",'w')
    bytecode_file.write(address)
    bytecode_file.close()
'''

address,abi,byecode = newContract(["Michael","Ali","Faraz","Marko"])

#web3.eth.defaultAccount = web3.eth.accounts[0]

'''
with open("addresses",) as _file:
    address = _file.read()
with open("abi",) as _file:
    abi = _file.read()
with open("bytecode",) as _file:
    bytecode = _file.read()
'''

address = web3.toChecksumAddress(address)
contract = web3.eth.contract(address = address, abi = abi)
print("Connecting to ETH")

options = contract.functions.getOptions().call()
print("\n\n The options are:",options)

'''
name = "Johhny34"
tx_hash = contract.functions.createOption(name).transact()
web3.eth.waitForTransactionReceipt(tx_hash)
print('Added new candidate: ', name)
options = contract.functions.getOptions().call()
print("\nThe new options are",options)
'''
def vote(contract,uid,option):

    try:
        tx_hash = contract.functions.vote(uid,option,0).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)
        return 1
    except:
        print("Could not vote, possibly already voted.")
        return 0

err_msg = vote(contract,504,"Michael")
options = contract.functions.getOptions().call()
print("\n\n The options are:",options)

