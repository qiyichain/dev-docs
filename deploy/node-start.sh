nohup geth --datadir /data/node0/data --ipcdisable --syncmode full --http --allow-insecure-unlock --http.addr "0.0.0.0" --unlock 0x4045d4ef78738b9750cc266bb972f66d950dc942 --password /data/node0/password.txt --ws --ws.addr "0.0.0.0"  --mine --bootnodes enode://2aa08cb22a14e1cb357a5638735f5c6c5591c5d3622b8a0c432c8c3f9633c0b9d4da44d0fa281ca0b1149bbd7809f8022b0305309902416db651e54ba0682be4@172.16.100.101:0?discport=30301 >> /data/geth.log 2>&1 &


nohup geth --datadir /data/node1/data --ipcdisable --syncmode full --http --allow-insecure-unlock --http.addr "0.0.0.0" --unlock 0x0d80b670b2d44017468ccc75787ea017678c6f72 --password /data/node1/password.txt --ws --ws.addr "0.0.0.0" --mine --bootnodes enode://2aa08cb22a14e1cb357a5638735f5c6c5591c5d3622b8a0c432c8c3f9633c0b9d4da44d0fa281ca0b1149bbd7809f8022b0305309902416db651e54ba0682be4@172.16.100.101:0?discport=30301 >> /data/geth.log 2>&1 &



nohup geth --datadir /data/node2/data --ipcdisable --syncmode full --http --allow-insecure-unlock --http.addr "0.0.0.0" --unlock 0xa26c57febec7700355a82e489cbe4649b7a66732 --password /data/node2/password.txt --ws --ws.addr "0.0.0.0" --mine --bootnodes enode://2aa08cb22a14e1cb357a5638735f5c6c5591c5d3622b8a0c432c8c3f9633c0b9d4da44d0fa281ca0b1149bbd7809f8022b0305309902416db651e54ba0682be4@172.16.100.101:0?discport=30301 >> /data/geth.log 2>&1 &


nohup geth  --gcmode=archive --datadir /data/node3/data --ipcdisable --syncmode full --http --allow-insecure-unlock --http.addr "0.0.0.0" --unlock 0xc20001631404c81d19e0b5b5aa4d30d45ed793d0 --password /data/node3/password.txt --ws --ws.addr "0.0.0.0" --http.api debug,net,eth,shh,web3,txpool --ws.api "eth,net,web3,network,debug,txpool" --mine --bootnodes enode://2aa08cb22a14e1cb357a5638735f5c6c5591c5d3622b8a0c432c8c3f9633c0b9d4da44d0fa281ca0b1149bbd7809f8022b0305309902416db651e54ba0682be4@172.16.100.101:0?discport=30301 >> /data/geth.log 2>&1 &

nohup geth --gcmode=archive --syncmode=full --datadir /data/node3/data --ipcdisable --http --allow-insecure-unlock --http.addr "0.0.0.0" --unlock 0xc20001631404c81d19e0b5b5aa4d30d45ed793d0 --password /data/node3/data/password.txt --ws --ws.addr "0.0.0.0" --http.api debug,net,eth,shh,web3,txpool --ws.api "eth,net,web3,network,debug,txpool" --mine --bootnodes enode://2aa08cb22a14e1cb357a5638735f5c6c5591c5d3622b8a0c432c8c3f9633c0b9d4da44d0fa281ca0b1149bbd7809f8022b0305309902416db651e54ba0682be4@172.16.100.101:0?discport=30301 >> /data/geth.log 2>&1 &



COIN=PEC ETHEREUM_JSONRPC_VARIANT=geth  ETHEREUM_JSONRPC_HTTP_URL=http://172.16.100.104:8545  ETHEREUM_JSONRPC_WS_URL=ws://172.16.100.104:8546 make start


