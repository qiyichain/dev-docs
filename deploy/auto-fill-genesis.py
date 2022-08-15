# coding: utf-8


#author: yqq
#date: 2022-08-15
#descriptions: 自动读取nodes下面的数据,填充./genesis.json中的extraData字段

from typing import List
import os

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


def gen_genesis_extra_data(miner_addrs: List[str]):
    """
    生成genesis.json中的extraData
    """
    # // TODO(yqq) 2022-08-11 , The algorithm of generating extraData
	# 	genesis.ExtraData = make([]byte, 32+len(signers)*common.AddressLength+65)
	# 	for i, signer := range signers {
	# 		copy(genesis.ExtraData[32+i*common.AddressLength:], signer[:])
	# 	}
    prefix_32bytes = '00'*32
    addrs_str = ''.join(miner_addrs)
    suffix_65bytes = '00'*65
    extra_data = '0x' + prefix_32bytes + addrs_str + suffix_65bytes
    return extra_data



def update_genesis_extra_data(extra_data: str):
    """
    更新genesis.json中的extraData字段,其他字段保持不变(位置)
    """
    lines = []
    with open('./example-genesis.json', 'r') as infile:
        lines = infile.readlines()
        print('len={}'.format(len(lines)))
        for i in range(len(lines)):
            line = lines[i]
            if '"extraData"' in line:
                new_line = '  "extraData":"{}",\n'.format(extra_data)    
                lines[i] = new_line
                break
        pass

    with open('genesis.json', 'w') as outfile:
        outfile.writelines(lines)

    pass


def main():
    addrs = read_node_address_from_nodes()
    print(addrs)
    extra_data = gen_genesis_extra_data(addrs)
    print(extra_data)
    update_genesis_extra_data(extra_data)
    pass


if __name__ == '__main__':
    main()


