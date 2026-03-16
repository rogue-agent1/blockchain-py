import hashlib, time, json
class Block:
    def __init__(s, index, transactions, prev_hash, nonce=0):
        s.index=index;s.timestamp=time.time();s.transactions=transactions
        s.prev_hash=prev_hash;s.nonce=nonce;s.hash=s.compute_hash()
    def compute_hash(s):
        data = json.dumps({"index":s.index,"timestamp":s.timestamp,"transactions":s.transactions,
                          "prev_hash":s.prev_hash,"nonce":s.nonce}, sort_keys=True)
        return hashlib.sha256(data.encode()).hexdigest()
class Blockchain:
    def __init__(s, difficulty=2):
        s.chain=[]; s.pending=[];s.difficulty=difficulty;s.chain.append(s._genesis())
    def _genesis(s): return Block(0, [], "0")
    def mine(s):
        if not s.pending: return None
        block = Block(len(s.chain), s.pending, s.chain[-1].hash)
        target = "0" * s.difficulty
        while not block.hash.startswith(target): block.nonce += 1; block.hash = block.compute_hash()
        s.chain.append(block); s.pending = []; return block
    def add_transaction(s, sender, receiver, amount):
        s.pending.append({"sender":sender,"receiver":receiver,"amount":amount})
    def is_valid(s):
        for i in range(1, len(s.chain)):
            if s.chain[i].prev_hash != s.chain[i-1].hash: return False
            if s.chain[i].hash != s.chain[i].compute_hash(): return False
        return True
def demo():
    bc = Blockchain(difficulty=2)
    bc.add_transaction("Alice", "Bob", 10)
    bc.add_transaction("Bob", "Charlie", 5)
    block = bc.mine()
    print(f"Block #{block.index}: hash={block.hash[:16]}... nonce={block.nonce}")
    bc.add_transaction("Charlie", "Alice", 3)
    block = bc.mine()
    print(f"Block #{block.index}: hash={block.hash[:16]}... nonce={block.nonce}")
    print(f"Chain length: {len(bc.chain)}, Valid: {bc.is_valid()}")
if __name__ == "__main__": demo()
