from flask import Flask, jsonify
from modules.mod_bchain import models
app = Flask(__name__)

blockchain = models.Blockchain()


@app.route("/mine_block")
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block["proof"]
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {"message": "Congratulations, you just mined a block!",
                "index": block["index"],
                "timestamp": block['timestamp'],
                "proof": block["proof"],
                "previous_hash": block["previous_hash"]}

    return jsonify(response), 200


@app.route("/get_chain")
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response)




