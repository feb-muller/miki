from packet_gen import PacketHandler
import asyncio

PAGE_REQ = 1
PAGE_RES = 2
PAGE_ERR = 3

INDEX_REQ = 4
INDEX_RES = 5


class Send_Page_Req:
    def __init__(self):
        self.packet_gen = PacketHandler()

    def req_packet(self):
        title = input("What Page are you looking for: ")
        packet = self.packet_gen.page_req_handler(PAGE_REQ, title)
        return packet


class Send_Index_Req:
    def __init__(self):
        self.packet_gen = PacketHandler()

    def req_packet(self):
        #packet = self.packet_gen.index_req_handler(INDEX_REQ, user)
        print("WIP")


def main():
    print("-----MIKI PROJECT-----\n")

    request = int(input("What would you like to request:\n" \
                        "1- Wiki Page\n" \
                        "2- Index Page\n"))
    if request == 1:
        packet = Send_Page_Req().req_packet()
    elif request == 2:
        packet = Send_Index_Req.req_packet()
        #Maybe this is automated with a page_req message then a cache or file of users indexes are stored from who you have requested from 

    print(packet)


main()