from flask import Flask, jsonify, request
from modules.mod_bchain import models
from uuid import uuid4

app = Flask(__name__)

# Creating Blockchain
blockchain = models.Blockchain()

# Creating an address for the node on Port 5000
node_address = str(uuid4()).replace('-', '')


@app.route("/mine_block")
def mine_block():
    # Get information from the blockchain stored into variables
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block["proof"]
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    # Add Transaction
    blockchain.add_transaction(sender=node_address, receiver="Nemanja", amount=16)
    # Create block
    block = blockchain.create_block(proof, previous_hash)

    response = {"message": "Congratulations, you just mined a block!",
                "index": block["index"],
                "timestamp": block['timestamp'],
                "proof": block["proof"],
                "previous_hash": block["previous_hash"],
                "transactions": block["transactions"]
                }

    return jsonify(response), 200


@app.route("/get_chain")
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response)


@app.route("/is_valid")
def is_valid():
    is_chain_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_chain_valid:
        response = {"message": "The Blockchain is valid."}
    else:
        response = {"message": "The Blockchain is NOT valid!"}
    return jsonify(response), 200


# Add new transaction to the Blockchain
@app.route("/add_transaction", methods=["POST"])
def add_transaction():
    json_file = request.get_json()
    transaction_keys = ["sender", "receiver", "amount"]

    if not all(key in json_file for key in transaction_keys):
        return "Transaction missing some of the required elements!", 400

    index = blockchain.add_transaction(sender=json_file.sender, receiver=json_file.receiver, amount=json_file.amount)
    response = {"message": f"This transaction will be added to Block {index}."}
    return response, 201


# Connecting new nodes
@app.route("/connect_node", methods=["POST"])
def connect_node():
    json_file = request.get_json()
    nodes = json_file.get('nodes')
    if nodes is None:
        return "No node", 400

    for node in nodes:
        blockchain.add_node(node)
    response = {"message": "All the nodes are now connected. The Examcoin Blockchain now contains the following nodes:",
                "total_nodes": list(blockchain.nodes)}
    return jsonify(response), 201


# Replacing the chain by the longest chain if needed
@app.route("/replace_chain")
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {"message": "The nodes had different chains so the chain was replaced by the longest one.",
                    "new_chain": blockchain.chain}
    else:
        response = {"message": "OK. The chain is the largest one.",
                    "actual_chain": blockchain.chain}

    return jsonify(response), 200


app.run("0.0.0.0", port=5000)
