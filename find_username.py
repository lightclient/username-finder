import sys
import urllib.request
import itertools
import threading
from socket import timeout
import enchant

# constants
alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
         'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
         'u', 'v', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
         'y', 'z']

THREAD_COUNT = 50
LETTER_COUNT = 1
BASE_URL = 'https://github.com/'

#########################################
# check inputs to see if they are valid #
#########################################

if len(sys.argv) != 4:
    print("Error: Incorrect number of arguments.")
    print("Ussge: findUsername {THREAD COUNT} {# OF LETTERS} {BASE URL}")
    exit(1)

try:
    THREAD_COUNT = int(sys.argv[1])
except ValueError:
    print("Error: Thread count much be an integer.")
    exit(1)

try:
    LETTER_COUNT = int(sys.argv[2])
except ValueError:
    print("Error: Letter count much be an integer.")
    exit(1)


# begin program ...

combos = []
usernames = []
valid_names = []

# generate url + username combos
# and save the combo and the username
for subset in itertools.combinations_with_replacement(alpha, LETTER_COUNT):
    combos.append(BASE_URL  + ''.join(subset))
    usernames.append(''.join(subset))

def load_page(threadID, threadCount):
    i = threadID

    while(i < len(combos)):
        try:
            if threadID < 10:
                print('  %d trying combos[%d] : %s' % (threadID, i, combos[i]) )
            elif threadID < 100:
                print(' %d trying combos[%d] : %s' % (threadID, i, combos[i]) )
            else:
                print('%d trying combos[%d] : %s' % (threadID, i, combos[i]) )

            urllib.request.urlopen(combos[i], timeout=8).read().decode('utf-8')
        except urllib.error.HTTPError:
            print( 'THREAD %d FOUND VALID USERNAME COMBOS[%d]: %s' % (threadID, i, combos[i]) )
            valid_names.append(usernames[i])
        except urllib.error.URLError:
            print(' THREAD %d HAD A URL ERROR AT USERNAME COMBOS[%d]: %s' % (threadID, i, combos[i]) )
            i -= threadCount
        except timeout:
            print(' THREAD %d HAD A TIMEOUT AT USERNAME COMBOS[%d]: %s' % (threadID, i, combos[i]) )
            i -= threadCount

        i += threadCount

class Crawler(threading.Thread):
    def __init__(self, threadID, threadCount):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.threadCount = threadCount
    def run(self):
        load_page(self.threadID, self.threadCount)

# create threads
threads = []
for i in range(0,THREAD_COUNT):
    threads.append(Crawler(i, THREAD_COUNT))

# run threads
for i in range(0,THREAD_COUNT):
    threads[i].start()

# wait for threads to join
for i in range(0,THREAD_COUNT):
    threads[i].join()

print("\n")
print("\n")

if len(valid_names) != 0:
    print("Found the following available usernames:")

    for name in valid_names:
        print(name)

else:
    print("No valid usernames found. :-(")
