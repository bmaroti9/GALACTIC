import json
import socket
import threading

BROADCATS_PORT = 17739
RECEIVER_THREAD = None
SENDER_SOCKET = None
RECEIVED_DATA = []


def send(msg):
    global SENDER_SOCKET
    if SENDER_SOCKET is None:
        print("creating sender socket")
        soc = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        soc.settimeout(0.1)
        SENDER_SOCKET = soc

    SENDER_SOCKET.sendto(json.dumps(msg).encode(),
                         ("<broadcast>", BROADCATS_PORT))


def receive():
    global RECEIVER_THREAD
    if RECEIVER_THREAD is None:
        def worker():
            try:
                print("starting receiver socket")
                soc = socket.socket(
                    socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
                soc.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

                soc.bind(("0.0.0.0", BROADCATS_PORT))
                while True:
                    msg, _ = soc.recvfrom(65536)
                    RECEIVED_DATA.append(json.loads(msg.decode()))

            finally:
                print("closing receiver socket")
                soc.close()

        RECEIVER_THREAD = threading.Thread(target=worker, daemon=True)
        RECEIVER_THREAD.start()

    global RECEIVED_DATA
    data = RECEIVED_DATA
    RECEIVED_DATA = []
    return data


def test():
    import sys
    import time
    msg = sys.argv[-1]

    num = 0
    while True:
        num += 1
        send(msg)
        time.sleep(0.1)
        print("received", num, receive())
        time.sleep(0.9)


if __name__ == '__main__':
    test()
