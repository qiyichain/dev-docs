
# 重新创建验证节点账户
# accounts:
# 	mkdir -p ./nodes/node0 && mkdir -p ./nodes/node1 && mkdir -p ./nodes/node2 && mkdir -p ./nodes/node3
# 	geth --datadir ./nodes/node0/data account new
# 	geth --datadir ./nodes/node1/data account new
# 	geth --datadir ./nodes/node2/data account new
# 	geth --datadir ./nodes/node3/data account new

.PHONY:genesis
genesis:
	python3 auto-fill-genesis.py 

init: genesis
	geth --datadir=./nodes/node0/data init ./genesis.json
	geth --datadir=./nodes/node1/data init ./genesis.json
	geth --datadir=./nodes/node2/data init ./genesis.json
	geth --datadir=./nodes/node3/data init ./genesis.json

clean:
	rm -rf ./nodes/node0/data
	rm -rf ./nodes/node1/data
	rm -rf ./nodes/node2/data
	rm -rf ./nodes/node3/data

start-node0:
	geth --datadir ./nodes/node0/data --ipcdisable --syncmode full --http --allow-insecure-unlock --http.addr "0.0.0.0" --unlock 0x4045d4ef78738b9750cc266bb972f66d950dc942 --password ./password.txt --mine --bootnodes  enode://2aa08cb22a14e1cb357a5638735f5c6c5591c5d3622b8a0c432c8c3f9633c0b9d4da44d0fa281ca0b1149bbd7809f8022b0305309902416db651e54ba0682be4@127.0.0.1:0?discport=30301

start-node1:
	geth --datadir ./nodes/node1/data --ipcdisable --syncmode full --http --allow-insecure-unlock --http.addr "0.0.0.0" --unlock 0x0d80b670b2d44017468ccc75787ea017678c6f72 --password ./password.txt --mine --port 30304 --http.port 8546 --bootnodes  enode://2aa08cb22a14e1cb357a5638735f5c6c5591c5d3622b8a0c432c8c3f9633c0b9d4da44d0fa281ca0b1149bbd7809f8022b0305309902416db651e54ba0682be4@127.0.0.1:0?discport=30301

start-node2:
	geth --datadir ./nodes/node2/data --ipcdisable --syncmode full --http --allow-insecure-unlock --http.addr "0.0.0.0" --unlock 0xa26c57febec7700355a82e489cbe4649b7a66732 --password ./password.txt --mine --port 30306 --http.port 8548 --bootnodes  enode://2aa08cb22a14e1cb357a5638735f5c6c5591c5d3622b8a0c432c8c3f9633c0b9d4da44d0fa281ca0b1149bbd7809f8022b0305309902416db651e54ba0682be4@127.0.0.1:0?discport=30301

start-node3:
	geth --datadir ./nodes/node3/data --ipcdisable --syncmode full --http --allow-insecure-unlock --http.addr "0.0.0.0" --unlock 0xc20001631404c81d19e0b5b5aa4d30d45ed793d0 --password ./password.txt --mine --port 30308 --http.port 8549 --bootnodes  enode://2aa08cb22a14e1cb357a5638735f5c6c5591c5d3622b8a0c432c8c3f9633c0b9d4da44d0fa281ca0b1149bbd7809f8022b0305309902416db651e54ba0682be4@127.0.0.1:0?discport=30301

gen-bootnode:
	mkdir -p bnode
	bootnode -genkey bnode/boot.key

start-bootnode:
	bootnode -nodekey bnode/boot.key
