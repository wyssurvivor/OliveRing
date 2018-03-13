# -*- coding: utf-8 -*-
from hashlib import md5
from struct import unpack_from,unpack
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class Node:
    def __init__(self, address, host):
        self.address=address
        self.host=host

class OliveRing:
    def __init__(self, virtual_count, ring_length):
        self.virtual_count=virtual_count
        self.key_node_map={}
        self.key_list=[]
        self.length=ring_length

    def position(self, key):
        k=self.hash_func(key)

    def get_node(self, key):
        hash_key=self.hash_function(key)
        print hash_key
        low=0
        high=len(self.key_list)-1
        target_index=-1
        while low<=high:
            mid=(low+high)/2
            if self.key_list[mid]<hash_key:
                low=mid+1
            elif self.key_list[mid]>hash_key:
                high=mid-1
            else:
                target_index=mid
                break
        print target_index
        if target_index == -1:
            if low>len(self.key_list)-1:
                return self.key_list[0]
            else:
                return None

        return self.key_list[target_index]

    def add_node(self, key):
        pass

    def hash_function(self, key):
        unpacked=unpack("c"*16, md5(key).digest())
        sum = 0
        for j in range(0,4):
            sum+=(ord(unpacked[j*4+3])&0xff)<<24\
                      |(ord(unpacked[j*4+2])&0xff)<<16\
                      |(ord(unpacked[j*4+1])&0xff)<<8\
                      |(ord(unpacked[j*4])&0xff)
        return sum%self.length

    # ketama hashing function
    def allocate(self, key, node):
        for i in range(1, self.virtual_count/4):
            unpacked=unpack("c"*16, md5(self.get_key(key, i)).digest())
            for j in range(0, 4):
                index=(ord(unpacked[j*4+3])&0xff)<<24\
                      |(ord(unpacked[j*4+2])&0xff)<<16\
                      |(ord(unpacked[j*4+1])&0xff)<<8\
                      |(ord(unpacked[j*4])&0xff)
                index=index%self.length
                if not self.key_node_map.has_key(index):
                    self.key_list.append(index)
                    self.key_node_map[index]=node


        self.key_list.sort()
        print self.key_list

    def get_key(self, key, index):
        return key+"_"+str(index)

if __name__=='__main__':
    # print md5("wys").hexdigest()
    # print ord(unpack("c"*16, md5("wys").digest())[1])<<2|1
    ring = OliveRing(100, 1000000)
    ring.allocate("0.0.0.0:11211", Node("0.0.0.0", 11211))
    ring.get_node('wys')