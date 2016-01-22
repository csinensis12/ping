'''
just simple ping, compatibile with python 3
'''

import socket
import struct


# create ICMP echo frame: type, code, checksum, IF, sequence number, data
def createIcmp():
    TYPE = 8
    CODE = 0
    ID = 1  # identifier
    SN = 16  # sequence number
    #DATA = 'abcdefghijklmnopqrstuvwabcdefghi'
    DATA = 'hi:)'

    header = struct.pack('bbhhh', TYPE, CODE, 0, ID, SN)
    data = bytearray()
    data.extend(map(ord, DATA))
    cs = get_checksum(header + data)
    print(hex(cs))
    new_header = struct.pack('bbhhh', TYPE, CODE, cs, ID, SN)
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


def ping(address):
    icmp_frame = createIcmp()

    # send ICMP frame
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'), None)
    for i in range(4):
        my_socket.sendto(icmp_frame, (address, 1))
        print(i)
        received_icmp_frame = my_socket.recv(1024)
        print('Received', repr(received_icmp_frame))
    my_socket.close()

    # wait for response

    # parse response


if __name__ == '__main__':
    # Testing
    # ping('127.0.0.1')
    # ping('192.168.0.1')
    ping('8.8.8.8')

    createIcmp()
