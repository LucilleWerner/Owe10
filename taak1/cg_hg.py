import requests
import os
import urllib2
import math
from sys import argv

jobmap = {chrm: [x for x in range((0+(chrm-1)*200),(200+(chrm-1)*200))] for chrm in range(1,27)}
chrmap = {23: 'X', 24: 'Y', 25: 'MT', 26: 'Un'}


def get_hg_chunk(chrm, chunknr):
    base_url = 'ftp://ftp.ncbi.nih.gov/genomes/Homo_sapiens/CHR_%s/hs_ref_GRCh38.p7_chr%s.fa.gz'
    if chrm in range(23, 27):
        chrm = chrmap.get(chrm)
    if isinstance(chrm, int):
        url_nr = str(chrm) if chrm > 9 else '0'+str(chrm)
    else:
        url_nr = chrm
    form_url = base_url % (url_nr, str(chrm))
    print(form_url)

    try:
        req = urllib2.urlopen(form_url)
        total_size = int(req.info().getheader('Content-Length').strip())

        chunksize = int(total_size/200)
        rest = 1 if (total_size % 200) > 0 else 0
        chunksize += rest
        cnt = 0
        # read the header, ie remove header from generator
        req.readline()
        while True:
            chunk = req.read(chunksize)
            cnt += 1
            if not chunk:
                break
            if cnt == chunknr:
                return chunk
    except urllib2.HTTPError, e:
        print "HTTP Error:",e.code , form_url
        return False
    except urllib2.URLError, e:
        print "URL Error:",e.reason , form_url
        return False


def compute_cg(jobnr):

    keys = jobmap.keys()
    chrm = [k for k in keys if jobnr in jobmap.get(k)]
    chrm = chrm[0]
    chunknr = jobmap.get(chrm).index(jobnr)

    hg_chunk = get_hg_chunk(chrm, chunknr)

    total_chars = len(hg_chunk)
    c_cont = hg_chunk.count('C')
    g_cont = hg_chunk.count('G')

    cg_cont = g_cont+c_cont

    print(total_chars)
    print(cg_cont)

if __name__ == "__main__":
    jobnr = int(argv[1])
    compute_cg(jobnr)
