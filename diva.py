from flask import Flask, render_template, request, redirect, Response
from verficationPipeline import anti_spoof_check, id_check
from camera import VideoCamera
from datetime import datetime as d
from web3 import Web3
from solcx import compile_source

# web3.py instance
url = "HTTP://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(url))

# set pre-funded account as sender
web3.eth.default_account = web3.eth.accounts[0]

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


def newBallot(listOfCandidates):
    # Submit the transaction that deploys the contract
    tx_hash = Ballot.constructor(["Johhny", "Michael"]).transact()

    # Wait for the transaction to be mined, and get the transaction receipt
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    address = tx_receipt['contractAddress']

    # address = "0x95A49A5e402A894D7f186781610b3e7f2fb1a33D"
    with open("addresses.csv", "a+") as file:
        file.write(address + ",")
    return address


with open("addresses.csv", 'r+') as file:
    adresses = [f for f in file.read().split(",")]

address = adresses[0]

address = web3.toChecksumAddress(address)
contract = web3.eth.contract(address=address, abi=abi)
print("DiVA>> Connecting to ETH")

elections = []


def update():
    options = contract.functions.getOptions().call()
    participants = contract.functions.getParticipants().call()
    print(options)

    elections = [
        {"options": [{"name": o[0], "votecount": o[2]} for o in options],
         "participants": [{"uid": p[0], "selection": p[1], "timestamp": p[2]} for p in participants]}
    ]
    print(elections)
    return elections


'''
name = "Johhny34"
tx_hash = contract.functions.createOption(name).transact()
web3.eth.waitForTransactionReceipt(tx_hash)
print('Added new candidate: ', name)
options = contract.functions.getOptions().call()
print("\nThe new options are",options)
'''


def vote(uid, option, contract=contract):
    # try:
    tx_hash = contract.functions.vote(int(uid), option, 0).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    #     return 1
    # except:
    #     print("Could not vote, possibly already voted.")
    #     return 0

# err_msg = vote(contract,504,"Michael")
# options = contract.functions.getOptions().call()
# print("\n\n The options are:",options)


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def main():
    elections = update()
    if request.method == "POST":
        req = request.form
        if ("vote-form" in request.method):
            uid = req["uid"]
            option = req["option"]
            vote(uid, option)
        elif ("" in request.method):
            uid = req["uid"]
            option = req["option"]
            vote(uid, option)
        return redirect(request.url)

    return render_template('index.html', verified=True, participants=elections[0]["participants"], options=elections[0]["options"])


@app.route('/anti_spoof_verification')
def anti_spoof_verification():
    return render_template('spoof_check.html')


@app.route('/anti_spoof_verification/video_feed')
def anti_spoof_verification_video_feed():
    return Response(anti_spoof_check(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/id_verification')
def id_verification():
    return render_template('id_check.html')


@app.route('/id_verification/video_feed')
def id_verification_video_feed():
    return Response(id_check(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
