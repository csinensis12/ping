'''
just simple ping, compatibile with python 3
'''
#asd
import socket
import struct
import select
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
    #fixme: im sure it could be done better (faster)
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
    #fixme: if response will come after 3s, waird things may happen, fix needed. comparing the seq_numbers would be ok

    my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'), None)
    for i in range(quantity):
        sequence_number = 1234+i
        icmp_frame = createIcmp(sequence_number)
        my_socket.sendto(icmp_frame, (address, 1))
        start = timeit.default_timer()
        block = select.select([my_socket],[],[],3) # waiting for message in socket, timeout 3s
        if block[0]:
            ip_frame = my_socket.recv(1024) # ip frame !!!
            stop = int(1000*(timeit.default_timer() - start))
            received_icmp_frame = ip_frame[20:28] # isolating ICMP frame (without data) from IP frame
            TYPE, CODE, cs, ID, SN = struct.unpack('bbHHh', received_icmp_frame)
            while timeit.default_timer() - start < 1 : continue # interval 1s between pings
        else:
            stop = "timeout"
        print('IP address = %(address)s   seq_num = %(sequence_number)s    time = %(stop)sms' % locals())



    my_socket.close()

if __name__ == '__main__':
    #TODO: getting address as argument of program
    #Testing
    #ping('google.pl')
    #ping('192.168.1.1')
    #ping('8.8.8.8')
    ping('americanexpress.com',50)
