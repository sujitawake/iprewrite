from pathlib import Path
from subprocess import call, DEVNULL, STDOUT, check_call
import sys
import mimetypes


# Check if required binaries exist, exit otherwise
executables = ['tcpprep', 'tcprewrite']
for each_binary in executables:
    try:
        check_call([each_binary, '--version'], stdout=DEVNULL, stderr=STDOUT)
    except OSError:
        print('%s binary missing on path' % (each_binary))
        exit(-1)


# Pull PCAPs list
# directory =  sys.argv[1]
directory = 'test'
for file in Path(directory).glob('**/*.pcap'):
    mime = mimetypes.guess_type(file)[0]
    if mime == 'application/vnd.tcpdump.pcap':
        print('[*]Generating cache for: %s..' % (file))
        check_call(['tcpprep', '--port', '-i',
            str(file), '--cachefile',
            str(file) + '.cache'
            ],
                   stdout=DEVNULL,
                   stderr=STDOUT)

        print('[*]Rewriting IP..')
        check_call(['tcprewrite', '-c', str(file) + '.cache',
                                '--endpoints', '172.16.1.10:172.16.1.254',
                                '-i', str(file),
                                '-o', str(file) + '_custom.pcap'])
        print('[+]Done..\n')
    else:
        print('[-]Ignoring non-libpcap based file')
