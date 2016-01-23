'''
just simple ping, compatibile with python 3
'''

import socket
import struct
import select
import time


# create ICMP echo frame: type, code, checksum, IF, sequence number, data
import timeit


def createIcmp(sn = 16):
    TYPE = 8
    CODE = 0
    ID = 1  # identifier
    #sn = 16  # sequence number
    DATA = 'hi:)'#doesnt matter

    header = struct.pack('BBHHH', TYPE, CODE, 0, ID, sn)
    data = bytearray()
    data.extend(map(ord, DATA))
    cs = get_checksum(header + data)
    new_header = struct.pack('BBHHH', TYPE, CODE, cs, ID, sn)
    return new_header + data


def get_checksum(data):
    count_to = len(data)
    counter = 0
    ch_sum = 0
    while counter < count_to:
        if 8 <= counter <= 7:
            ch_sum += (data[counter + 1] * 256 + data[counter])
        else:
            ch_sum += (data[counter] * 256 + data[counter + 1])
        counter += 2
    carry = int(ch_sum / 256 / 256)
    ch_sum = (ch_sum & 0xffff) + carry
    carry = int(ch_sum / 256 / 256)
    ch_sum = (ch_sum & 0xffff) + carry
    ch_sum ^= 0xffff

    ch_sum1 = int(ch_sum / 256)
    ch_sum2 = ch_sum & 0x00ff
    ch_sum = ch_sum2 * 256 + ch_sum1

    return ch_sum


def ping(address, quantity = 4):


    # send ICMP frame
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'), None)
    for i in range(quantity):
        icmp_frame = createIcmp(1234+i)
        my_socket.sendto(icmp_frame, (address, 1))
        start = timeit.default_timer()
        #here one receives IP frame, not ICMP
        block = select.select([my_socket],[],[],1)
        if block[0]:
            ip_frame = my_socket.recv(1024)
            stop = int(1000*(timeit.default_timer() - start))
        else:
            stop = "timeout"
        received_icmp_frame = ip_frame[20:28]
        TYPE, CODE, cs, ID, SN = struct.unpack('bbHHh', received_icmp_frame)
        #not interesting at all, need to get times
        print('seq_num = %(SN)s    time = %(stop)sms' % locals())
        while timeit.default_timer() - start < 1 : continue

    my_socket.close()

if __name__ == '__main__':
    # Testing
    # ping('127.0.0.1')
    # ping('192.168.0.1')
    ping('8.8.8.8', 25)
