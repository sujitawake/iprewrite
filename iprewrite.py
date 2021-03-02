from pathlib import Path
from subprocess import call, DEVNULL, STDOUT, check_call
import os
import mimetypes
import argparse


# Init parser
parser = argparse.ArgumentParser(description='Recursive IP Rewrite Tool')
parser.add_argument('--dir', '-d', type=str, help='Source PCAP directory')
parser.add_argument('--file', '-f', type=str, help='Source PCAP file')
args = parser.parse_args()


# Check if required binaries exist, exit otherwise
executables = ['tcpprep', 'tcprewrite']
for each_binary in executables:
    try:
        check_call([each_binary, '--version'], stdout=DEVNULL, stderr=STDOUT)
    except OSError:
        print('%s binary missing on path' % (each_binary))
        exit(-1)


# Pull PCAPs list
directory = args.dir
pcapfile = args.file
for file in Path(directory).glob('**/*.pcap'):
    mime = mimetypes.guess_type(file)[0]
    if mime == 'application/vnd.tcpdump.pcap':
        print('\n[*]Generating cache: %s..' % (file))
        check_call(['tcpprep', '--port', '-i',
            str(file), '--cachefile',
            str(file) + '.cache'
            ],
                   stdout=DEVNULL,
                   stderr=STDOUT)

        print('[*]Rewriting IP: 172.16.1.10 <-> 172.16.1.254')
        check_call(['tcprewrite', '-c', str(file) + '.cache',
                                '--endpoints', '172.16.1.10:172.16.1.254',
                                '-i', str(file),
                                '-o', str(file) + '_custom.pcap'])
        os.remove(str(file) + '.cache')
    else:
        print('[-]Ignored non-libpcap file..')

