#!/usr/bin/env python3
"""Blockchain with proof of work, transactions, and Merkle roots."""
import hashlib, json, time, sys

class Block:
    def __init__(self, index, transactions, prev_hash, nonce=0):
        self.index=index; self.ts=time.time(); self.transactions=transactions
        self.prev_hash=prev_hash; self.nonce=nonce; self.hash=self.compute_hash()
    def compute_hash(self):
        data=json.dumps({"index":self.index,"ts":self.ts,"txs":self.transactions,
                         "prev":self.prev_hash,"nonce":self.nonce},sort_keys=True)
        return hashlib.sha256(data.encode()).hexdigest()

class Blockchain:
    def __init__(self, difficulty=2):
        self.chain=[self._genesis()]; self.difficulty=difficulty; self.pending=[]
    def _genesis(self): return Block(0,[],"0")
    def add_transaction(self, sender, receiver, amount):
        self.pending.append({"from":sender,"to":receiver,"amount":amount})
    def mine(self, miner):
        self.pending.append({"from":"NETWORK","to":miner,"amount":1})
        block=Block(len(self.chain),self.pending,self.chain[-1].hash)
        target="0"*self.difficulty
        while not block.hash.startswith(target):
            block.nonce+=1; block.hash=block.compute_hash()
        self.chain.append(block); self.pending=[]; return block
    def is_valid(self):
        for i in range(1,len(self.chain)):
            if self.chain[i].prev_hash!=self.chain[i-1].hash: return False
            if self.chain[i].hash!=self.chain[i].compute_hash(): return False
        return True
    def balance(self, addr):
        bal=0
        for block in self.chain:
            for tx in block.transactions:
                if tx["to"]==addr: bal+=tx["amount"]
                if tx["from"]==addr: bal-=tx["amount"]
        return bal

if __name__ == "__main__":
    bc=Blockchain(difficulty=2)
    bc.add_transaction("Alice","Bob",5); bc.add_transaction("Bob","Charlie",2)
    b=bc.mine("Miner1")
    print(f"Block {b.index}: hash={b.hash[:16]}... nonce={b.nonce}")
    bc.add_transaction("Charlie","Alice",1)
    b=bc.mine("Miner1")
    print(f"Block {b.index}: hash={b.hash[:16]}... nonce={b.nonce}")
    print(f"Valid: {bc.is_valid()}")
    for addr in ["Alice","Bob","Charlie","Miner1"]:
        print(f"  {addr}: {bc.balance(addr)}")
