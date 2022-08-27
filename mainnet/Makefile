
# 创建验证节点账户, 归档节点和同步节点不需要创建账户
accounts: clean
	@mkdir -p ./nodes/node0/data && mkdir -p ./nodes/node1/data && mkdir -p ./nodes/node2/data && mkdir -p ./nodes/node3/data
	@mkdir -p ./nodes/node0/logs && mkdir -p ./nodes/node1/logs && mkdir -p ./nodes/node2/logs && mkdir -p ./nodes/node3/logs
	@mkdir -p ./nodes/archivenode/data && mkdir -p ./nodes/archivenode/logs
	@mkdir -p ./nodes/syncnode/data && mkdir -p ./nodes/syncnode/logs
	@echo -n $(shell tr -cd 'a-zA-Z0-9' </dev/urandom |head -c14)> ./nodes/node0/data/password.txt
	@echo -n $(shell tr -cd 'a-zA-Z0-9' </dev/urandom |head -c14)> ./nodes/node1/data/password.txt
	@echo -n $(shell tr -cd 'a-zA-Z0-9' </dev/urandom |head -c14)> ./nodes/node2/data/password.txt
	@echo -n $(shell tr -cd 'a-zA-Z0-9' </dev/urandom |head -c14)> ./nodes/node3/data/password.txt
	@geth --datadir ./nodes/node0/data account new --password ./nodes/node0/data/password.txt
	@geth --datadir ./nodes/node1/data account new --password ./nodes/node1/data/password.txt
	@geth --datadir ./nodes/node2/data account new --password ./nodes/node2/data/password.txt
	@geth --datadir ./nodes/node3/data account new --password ./nodes/node3/data/password.txt

.PHONY:genesisstart-bootnode
genesis:
	python3 auto-fill-genesis.py 

init: accounts genesis gen-bootnode
	geth --datadir=./nodes/node0/data init ./genesis.json
	geth --datadir=./nodes/node1/data init ./genesis.json
	geth --datadir=./nodes/node2/data init ./genesis.json
	geth --datadir=./nodes/node3/data init ./genesis.json
	geth --datadir=./nodes/archivenode/data init ./genesis.json
	geth --datadir=./nodes/syncnode/data init ./genesis.json

.PHONY:clean
clean:
	@rm -rf ./nodes
	@rm -rf ./bnode

.PHONY:gen
gen: 
	echo -n $(shell bootnode -nodekey bnode/boot.key -writeaddress)> bnode/boot.pubkey
	python3 gen-start-script.py

gen-bootnode:
	mkdir -p bnode
	bootnode -genkey bnode/boot.key

start-bootnode:
	bootnode -nodekey bnode/boot.key  -addr $(shell cat gen-script-config.json | jq .node0_ip | sed  's\"\\g'):30301


.PHONY:copy
copy:
ifeq ($(NODEPASS),)
	@echo "NODEPASS does exists! Please set NODEPASS to ~/.bashrc and source ~/.bashrc"
else
	cp -r ./nodes/node0 /data
	@echo "node0 copy finished"
	@sshpass -p $(NODEPASS) scp -r ./nodes/node1 root@$(shell cat gen-script-config.json | jq .node1_ip | sed  's\"\\g'):/data
	@sshpass -p $(NODEPASS) scp $(shell which geth) root@$(shell cat gen-script-config.json | jq .node1_ip | sed  's\"\\g'):/usr/bin/geth
	@echo "node1 copy finished"
	@sshpass -p $(NODEPASS) scp -r dev-docs/deploy/nodes/node2 root@$(shell cat gen-script-config.json | jq .node2_ip | sed  's\"\\g'):/data
	@sshpass -p $(NODEPASS) scp $(shell which geth) root@$(shell cat gen-script-config.json | jq .node2_ip | sed  's\"\\g'):/usr/bin/geth
	@echo "node2 copy finished"
	@sshpass -p $(NODEPASS) scp -r dev-docs/deploy/nodes/node3 root@$(shell cat gen-script-config.json | jq .node3_ip | sed  's\"\\g'):/data
	@sshpass -p $(NODEPASS) scp $(shell which geth) root@$(shell cat gen-script-config.json | jq .node3_ip | sed  's\"\\g'):/usr/bin/geth
	@echo "node3 copy finished"
	@sshpass -p $(NODEPASS) scp -r dev-docs/deploy/nodes/archivenode root@$(shell cat gen-script-config.json | jq .archivenode_ip | sed  's\"\\g'):/data
	@sshpass -p $(NODEPASS) scp $(shell which geth) root@$(shell cat gen-script-config.json | jq .archivenode_ip | sed  's\"\\g'):/usr/bin/geth
	@echo "archivenode copy finished"
	@sshpass -p $(NODEPASS) scp -r dev-docs/deploy/nodes/syncnode root@$(shell cat gen-script-config.json | jq .syncnode_ip | sed  's\"\\g'):/data
	@sshpass -p $(NODEPASS) scp $(shell which geth) root@$(shell cat gen-script-config.json | jq .nsyncnode_ip | sed  's\"\\g'):/usr/bin/geth
	@echo "syncnode copy finished"
	@echo "all ok"
endif
