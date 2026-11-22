import base64
import struct
from wiki_handler import WikiHandler
import bz2
import sys

#Script used to gennerate packets in binary form to then be sent over mesh

HEADER = struct.Struct(">BBHH") #6 byte total B = 1 byte H = 2 bytes

PAGE_REQ = 1
PAGE_RES = 2
PAGE_ERR = 3

INDEX_REQ = 4
INDEX_RES = 5


class PacketHandler:
    CHUNK_SIZE = 144

    def __init__(self):
        self.wiki_handler = WikiHandler()


    #uses wiki script to get page based on title
    def fetch_page(self, title: str): 
        wiki_page, short_des = self.wiki_handler.handle(title)
        return wiki_page


    #encodes packet accoring to HEADER struct
    def encode_packet(self, msg_type: int, crc8: int, seq_no: int, req_no: int):
        packet = HEADER.pack(msg_type, crc8, seq_no, req_no)
        return packet


    #Decodes packet according to HEADER struct
    def decode_packets(self, packet_list: list): #Hmmm unliekly that this will be a nice list of packets instead of a stream of all sorts?!!
        page_res_payloads= []

        for i in range(0, len(packet_list)):
            working_packet = packet_list[i]
            header = working_packet[:6]
            decoded_header = HEADER.unpack_from(header)

            msg_type = decoded_header[0]
            crc8 = decoded_header[1]
            seq_no = decoded_header[2]
            req_no = decoded_header[3]

            #crc check

            if msg_type == PAGE_RES:
                page_res_payloads.append(working_packet[6:])

        joined_payloads = b''.join(page_res_payloads)
        decoded_payload = bz2.decompress(joined_payloads) #This bit should only apply to decoding page response
        print(decoded_payload)


    #Wiki Page request handler returns list of packets
    def page_res_handler(self, msg_type, request):
        packet_list = []
        seq_no = 0

        wiki_page = self.fetch_page(title=request)
        wiki_comp = bz2.compress(wiki_page.encode("utf-8"))
        data_size = sys.getsizeof(wiki_comp)

        for i in range(0, len(wiki_comp), self.CHUNK_SIZE):

            packet = self.encode_packet(msg_type, 1, seq_no, 1) + (wiki_comp[i:i + 144])
            packet_list.append(packet)
            seq_no += 1

        packet = self.encode_packet(msg_type, 1, 1, 1)

        return packet_list


    #index page request handler
    def index_res_handler(self, msg_type, user):

        #some other script that gets indexes? maybe index req sent with every message if not in cache?
        packet = self.encode_packet(msg_type, 1, 1, 1)

        return packet