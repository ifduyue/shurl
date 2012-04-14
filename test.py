from urlfetch import post
import random

def sigint():
    import signal
    def sig(n, f):
        import signal, os
        os.kill(0, signal.SIGTERM)
    signal.signal(signal.SIGINT, sig)

def randstr(l=4, h=8):
    import string
    chars = string.ascii_letters + string.digits
    length = random.randint(l, h)
    return ''.join(random.choice(chars) for i in xrange(length))

def run(x=0):
    response = post(
        "http://127.0.0.1:1234/",
        data = "url=http://lyxint.com/%d/" % x +randstr(1, 10),
    )
    #print response.status, response.getheader('location')

if __name__ == '__main__':
    import multiprocessing
    import sys
    try: pnum = int(sys.argv[1])
    except: pnum = 2
    try: times = int(sys.argv[2])
    except: times = 1000
    sigint()
    pool = multiprocessing.Pool(pnum)
    pool.map(run, xrange(times))
