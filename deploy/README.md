# 测试链搭建步骤

## 部署环境

- 系统：Linux/MacOS
- 工具：`yum install make automake  -y` 或 `sudo apt install make automake -y`
- Python3: `yum install python3` 或 `sudo apt install python3 -y`
- 下载peculiar最新的发布的版本可执行文件，解压，将`geth`加到`/usr/bin/geth`：https://github.com/qiyichain/peculiar/releases
- 检查geth是否能执行：`geth --help`

## 关键参数

- chainId: `12285`
- 初始测试账户（同时作为系统合约的admin）：`0xf513e4e5Ded9B510780D016c482fC158209DE9AA`
- 节点数量：4


## 步骤

所有的步骤都使用Makefile进行操作

### 0.清空历史数据

- `make clean`

### 1.通过`genesis.json`初始化节点数据目录

> 需要系统已经安装`python3`

- `make init`

### 2.启动引导节点（仅第一次启动需要，链正常出块之后，就不需要了）

- `make start-bootnode`

### 3.启动节点（单机部署）

> 32668, 8545, 8546, 30301 这几个端口不能被别的端口占用

- 终端1前台启动`node0`：`make start-node0`
- 终端2前台启动`node1`：`make start-node1`
- 终端2前台启动`node2`：`make start-node2`
- 终端3前台启动`node3`：`make start-node3`

> 如需后台启动，自行使用`nohup xxxx >> ./nodexxxx/geth.log 2>&1 &`启动即可

至此，本地启动4个验证节点结束


(结束)
----

### 4:启动节点(多机部署)

假设在node0服务器上进行了初始化操作，将已初始化的节点目录、下载好的可执行文件geth拷贝到其他机器上。

- 拷贝脚本:
    ```shell
    cp -f /root/peculiar/build/bin/geth /usr/bin/geth
    cp -R dev-docs/deploy/nodes/node0 /data
    sshpass -p $PASSWORD scp -r dev-docs/deploy/nodes/node1 root@172.16.100.102:/data
    sshpass -p $PASSWORD scp /root/peculiar/build/bin/geth root@172.16.100.102:/usr/bin/geth
    sshpass -p $PASSWORD scp -r dev-docs/deploy/nodes/node2 root@172.16.100.103:/data
    sshpass -p $PASSWORD scp /root/peculiar/build/bin/geth root@172.16.100.103:/usr/bin/geth
    sshpass -p $PASSWORD scp -r dev-docs/deploy/nodes/node3 root@172.16.100.104:/data
    sshpass -p $PASSWORD scp /root/peculiar/build/bin/geth root@172.16.100.104:/usr/bin/geth
    ```

> 注意：如果不需要节点状态监控可以去掉`--metrics`所有的配置，如需要则需要配置influxDB


- node0启动脚本: 
    ```shell
    nohup geth \
    --datadir /data/node0/data \
    --networkid 12285 \
    --ipcdisable \
    --syncmode full \
    --http \
    --allow-insecure-unlock \
    --http.addr "0.0.0.0" \
    --unlock 0x4045d4ef78738b9750cc266bb972f66d950dc942 \
    --password /data/node0/data/password.txt \
    --ws \
    --ws.addr "0.0.0.0"  \
    --mine \
    --bootnodes enode://2aa08cb22a14e1cb357a5638735f5c6c5591c5d3622b8a0c432c8c3f9633c0b9d4da44d0fa281ca0b1149bbd7809f8022b0305309902416db651e54ba0682be4@172.16.100.101:0?discport=30301 \
    --metrics \
    --metrics.influxdb \
    --metrics.influxdb.endpoint="http://172.16.100.105:8086" \
    --metrics.influxdb.database="node0" \
    --metrics.influxdb.username=influxdb \
    --metrics.influxdb.password=password \
    >> /data/geth.log 2>&1 &
    ```


- node1启动:

    ```shell
    nohup geth \
    --datadir /data/node1/data \
    --networkid 12285 --ipcdisable \
    --syncmode full \
    --http \
    --allow-insecure-unlock \
    --http.addr "0.0.0.0" \
    --unlock 0x0d80b670b2d44017468ccc75787ea017678c6f72 \
    --password /data/node1/data/password.txt \
    --ws \
    --ws.addr "0.0.0.0" \
    --mine \
    --bootnodes enode://2aa08cb22a14e1cb357a5638735f5c6c5591c5d3622b8a0c432c8c3f9633c0b9d4da44d0fa281ca0b1149bbd7809f8022b0305309902416db651e54ba0682be4@172.16.100.101:0?discport=30301  \
    --metrics \
    --metrics.influxdb \
    --metrics.influxdb.endpoint="http://172.16.100.105:8086" \
    --metrics.influxdb.database="node1" \
    --metrics.influxdb.username=influxdb \
    --metrics.influxdb.password=password \
    >> /data/geth.log 2>&1 &

    ```

- node2启动


    ```shell
    nohup geth \
    --datadir /data/node2/data \
    --networkid 12285 \
    --ipcdisable \
    --syncmode full \
    --http \
    --allow-insecure-unlock \
    --http.addr "0.0.0.0" \
    --unlock 0xa26c57febec7700355a82e489cbe4649b7a66732 \
    --password /data/node2/data/password.txt \
    --ws \
    --ws.addr "0.0.0.0" \
    --metrics \
    --metrics.influxdb \
    --metrics.influxdb.endpoint="http://172.16.100.105:8086" \
    --metrics.influxdb.database="node2" \
    --metrics.influxdb.username=influxdb \
    --metrics.influxdb.password=password \
    --mine \
    --bootnodes enode://2aa08cb22a14e1cb357a5638735f5c6c5591c5d3622b8a0c432c8c3f9633c0b9d4da44d0fa281ca0b1149bbd7809f8022b0305309902416db651e54ba0682be4@172.16.100.101:0?discport=30301 \
    >> /data/geth.log 2>&1 &
    ```


- node3


    ```shell
    nohup geth \
    --gcmode=archive \
    --syncmode=full \
    --networkid 12285 \
    --datadir /data/node3/data \
    --ipcdisable \
    --http \
    --allow-insecure-unlock \
    --http.addr "0.0.0.0" \
    --unlock 0xc20001631404c81d19e0b5b5aa4d30d45ed793d0 \
    --password /data/node3/data/password.txt \
    --ws \
    --ws.addr "0.0.0.0" \
    --http.api debug,net,eth,shh,web3,txpool \
    --ws.api "eth,net,web3,network,debug,txpool" \
    --mine \
    --bootnodes enode://2aa08cb22a14e1cb357a5638735f5c6c5591c5d3622b8a0c432c8c3f9633c0b9d4da44d0fa281ca0b1149bbd7809f8022b0305309902416db651e54ba0682be4@172.16.100.101:0?discport=30301  \
    --metrics \
    --metrics.influxdb \
    --metrics.influxdb.endpoint="http://172.16.100.105:8086" \
    --metrics.influxdb.database="node3" \
    --metrics.influxdb.username=influxdb \
    --metrics.influxdb.password=password \
    >> /data/geth.log 2>&1 &

    ```