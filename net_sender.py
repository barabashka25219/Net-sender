import socket
import sys
import getopt

def main(argv):
    options = parse_options(argv)
    received_bytes = 0

    if options['mode'] == 'receiver':
        sock = socket.socket()
        sock.bind(('0.0.0.0', 5555))
        sock.listen(1)

        print(f"[*] Wait for connections on {options['address']}:{options['port']}")
        print(f"[*] Future saved file \"{options['file']}\"")

        client, client_addr = sock.accept()

        with open(options['file'], 'wb') as file:
            while True:
                try:
                    data = client.recv(1024)
                    file.write(data)
                    received_bytes += len(data)

                except KeyboardInterrupt:
                    file.write(data)
                    received_bytes += len(data)
                    break

        sock.close()
        print(f"[*] Success saved to {options['file']}")
        print(f"[*] Received about {received_bytes / 1000000} mb.")

    elif options['mode'] == 'sender' and options['file']:
        sock = socket.socket()
        sock.connect((options['address'], int(options['port'])))

        try:
            with open(options['file'], 'rb') as file:
                for line in file:
                    sock.send(line)

        except FileNotFoundError:
            print(f"File {options['file']} not found.")

        sock.close()

    else:
        print('Unknown mode.')


def parse_options(options):
    opt_template = 'a:m:f:p:h'
    result = {
        'address': '', 'port': '',
        'mode': 'receiver', 'file': 'wifi_sender_result',
    }

    try:
        opts, args = getopt.getopt(options, opt_template)

        for opt, arg in opts:
            if opt in ('-a'):
                result['address'] = arg

            elif opt in ('-m'):
                result['mode'] = arg

            elif opt in ('-f'):
                result['file'] = arg

            elif opt in ('-p'):
                result['port'] = arg


    except getopt.GetoptError as err:
        help()
        sys.exit(-1)

    return result

def help():
    print('Net Sender')
    print('-m, --mode - you are [receiver] or [sender], receiver default')
    print('-a, --address - target ip address')
    print('-p, --port - target server port')
    print('-f, --file - set path to saved file, \'.\' default')
    print('-h, --help - shot this note and exit')
    print('')
    print('python3 ./net_sender -m sender -a 192.168.0.20 -p 5555 file.txt')
    print('python3 ./net_sender -m receiver')

main(sys.argv[1:])
