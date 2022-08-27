#coding:utf8
# author: yqq
# date: 2022-08-27
# descriptions: 生成启动脚本

import json
import os, stat
from typing import List

# 验证节点启动脚本模板
validator_start_template = """
if [ ! -d /data/{0}/data ];then
    echo "start.sh : /data/{0}/data does not exists"
    exit 1 
fi

if [ ! -d /data/{0}/logs ];then
   mkdir -p /data/{0}/logs
fi

nohup geth \\
--datadir /data/{0}/data \\
--logpath /data/{0}/logs \\
--networkid 2285 \\
--ipcdisable \\
--syncmode full \\
--unlock {1} \\
--password /data/{0}/data/password.txt \\
--mine \\
--bootnodes enode://{2}@{3}:0?discport=30301 \\
--metrics \\
--metrics.influxdb \\
--metrics.influxdb.endpoint="http://{4}:{5}" \\
--metrics.influxdb.database="{0}" \\
--metrics.influxdb.username={6} \\
--metrics.influxdb.password={7} \\
&
"""

# 普通同步节点（对外提供RPC服务）
sync_node_start_template = """

if [ ! -d /data/syncnode/data ];then
    echo  "start.sh : /data/syncnode/data does not exists"
    exit 1 
fi

if [ ! -d /data/syncnode/logs ];then
   mkdir -p /data/syncnode/logs
fi

nohup geth \\
--syncmode=full \\
--networkid 2285 \\
--datadir /data/syncnode/data \\
--logpath /data/syncnode/logs \\
--ipcdisable \\
--http \\
--http.addr "0.0.0.0" \\
--ws \\
--ws.addr "0.0.0.0" \\
--http.api debug,net,eth,web3,txpool \\
--ws.api "eth,net,web3,debug,txpool" \\
--bootnodes enode://{0}@{1}:0?discport=30301 \\
--metrics \\
--metrics.influxdb \\
--metrics.influxdb.endpoint="http://{2}:{3}" \\
--metrics.influxdb.database="syncnode" \\
--metrics.influxdb.username={4} \\
--metrics.influxdb.password={5} \\
&
"""

# 归档节点启动脚本模板（供区块浏览器使用）
archive_node_start_template = """

if [ ! -d /data/archivenode/data ];then
    echo " start.sh : directory:/data/archivenode/data does not exists"
    exit 1 
fi

if [ ! -d /data/archivenode/logs ];then
   mkdir -p /data/archivenode/logs
fi

nohup geth \\
--gcmode=archive \\
--syncmode=full \\
--networkid 2285 \\
--datadir /data/archivenode/data \\
--logpath /data/archivenode/logs \\
--ipcdisable \\
--http \\
--http.addr "0.0.0.0" \\
--ws \\
--ws.addr "0.0.0.0" \\
--http.api debug,net,eth,web3,txpool \\
--ws.api "eth,net,web3,debug,txpool" \\
--bootnodes enode://{0}@{1}:0?discport=30301  \\
--metrics \\
--metrics.influxdb \\
--metrics.influxdb.endpoint="http://{2}:{3}" \\
--metrics.influxdb.database="archivenode" \\
--metrics.influxdb.username={4} \\
--metrics.influxdb.password={5} \\
&
"""


def gen_validator_start_script(
    node_name,
    node_account,
    bootnode_pubkey, 
    bootnode_ip, 
    influxdb_ip, 
    influxdb_port, 
    influxdb_username,
    influxdb_password
    ):

    # 使用模板生成
    script = validator_start_template.format(
        node_name,
        node_account,
        bootnode_pubkey,
        bootnode_ip,
        influxdb_ip,
        influxdb_port,
        influxdb_username,
        influxdb_password,
    )

    return script


def gen_sync_node_start_script(
    bootnode_pubkey,
    bootnode_ip,
    influxdb_ip,
    influxdb_port,
    influxdb_username,
    influxdb_password
):
    script = sync_node_start_template.format(
        bootnode_pubkey,
        bootnode_ip,
        influxdb_ip,
        influxdb_port,
        influxdb_username,
        influxdb_password,
    )
    return script


def gen_archive_node_start_script(
    bootnode_pubkey,
    bootnode_ip,
    influxdb_ip,
    influxdb_port,
    influxdb_username,
    influxdb_password
):
    script  = archive_node_start_template.format(
        bootnode_pubkey,
        bootnode_ip,
        influxdb_ip,
        influxdb_port,
        influxdb_username,
        influxdb_password,
    )
    return script

def read_config_file(path):
    cfg = json.load(open(path))
    return cfg

def read_node_address_from_nodes() -> List[str]:
    dirs = [
        './nodes/node0/data/keystore',
        './nodes/node1/data/keystore',
        './nodes/node2/data/keystore',
        './nodes/node3/data/keystore',
    ]
    ret_addrs = []
    for dir in dirs: 
        filenames = os.listdir(dir)
        for name in filenames:
            addr =  name[name.rfind('--') + 2 : ]
            ret_addrs.append(addr)
    return ret_addrs

def get_bootnode_pubkey():
    with open('./bnode/boot.pubkey') as infile:
        return infile.read(1024)


def main():

    # 读取配置
    cfg = read_config_file('gen-script-config.json')

    # 读取验证节点的账户地址
    nodes = read_node_address_from_nodes()

    assert len(nodes) == 4 , "nodes must be 4 nodes"

    # 从 ./bnode/boot.pubkey 获取引导节点pubkey
    bootnode_pubkey = get_bootnode_pubkey()

    for x in range(0, 4):
        node_name  = 'node{}'.format(x)
        s = gen_validator_start_script(
            node_name= node_name,
            node_account= '0x' + nodes[x],
            bootnode_ip = cfg['node0_ip'],  # 默认在node0上启动引导节点
            bootnode_pubkey= bootnode_pubkey,
            influxdb_ip= cfg['influxdb_ip'],
            influxdb_port = cfg['influxdb_port'],
            influxdb_username  = cfg['influxdb_username'],
            influxdb_password = cfg['influxdb_password'],
        )

        output_file_path = './nodes/{0}/start.sh'.format(node_name)
        ofile = open(output_file_path, 'w')
        ofile.write(s)
        ofile.flush()
        ofile.close()
        
        # 增加可执行权限 chmod 777 xxx/start.sh
        os.chmod(output_file_path, stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO)
        pass

    
    
    # 同步节点启动脚本
    if True:
        s = gen_sync_node_start_script(
            bootnode_ip = cfg['node0_ip'],  # 默认在node0上启动引导节点
            bootnode_pubkey= bootnode_pubkey,
            influxdb_ip= cfg['influxdb_ip'],
            influxdb_port = cfg['influxdb_port'],
            influxdb_username  = cfg['influxdb_username'],
            influxdb_password = cfg['influxdb_password'],
        )
        output_file_path = './nodes/syncnode/start.sh'.format(node_name)
        ofile = open(output_file_path, 'w')
        ofile.write(s)
        ofile.flush()
        ofile.close()
        # 增加可执行权限 chmod 777 xxx/start.sh
        os.chmod(output_file_path, stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO)

    # 归档节点启动脚本
    if True:
        s = gen_archive_node_start_script(
            bootnode_ip = cfg['node0_ip'],  # 默认在node0上启动引导节点
            bootnode_pubkey= bootnode_pubkey,
            influxdb_ip= cfg['influxdb_ip'],
            influxdb_port = cfg['influxdb_port'],
            influxdb_username  = cfg['influxdb_username'],
            influxdb_password = cfg['influxdb_password'],
        )
        output_file_path = './nodes/archivenode/start.sh'.format(node_name)
        ofile = open(output_file_path, 'w')
        ofile.write(s)
        ofile.flush()
        ofile.close()
        # 增加可执行权限 chmod 777 xxx/start.sh
        os.chmod(output_file_path, stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO)
        
    pass


if __name__ == '__main__':
    main()
    
