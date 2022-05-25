import datetime
import io

from PyPDF2 import PdfFileReader
from cryptography.hazmat import backends
from cryptography.hazmat.primitives.serialization import pkcs12
from endesive import pdf
from endesive.pdf import cms

from data import load_prev_block, save_new_block, BLOCK_PREFIX, load_block


def sign(path):
    date = datetime.datetime.utcnow() - datetime.timedelta(hours=12)
    date = date.strftime("D:%Y%m%d%H%M%S+00'00'")
    dct = {
        "aligned": 0,
        "sigflags": 3,
        "sigflagsft": 132,
        "sigpage": 0,
        "sigbutton": True,
        "sigfield": "Signature1",
        "auto_sigfield": True,
        "sigandcertify": True,
        "signaturebox": (470, 840, 570, 640),
        "signature": "Dokument podpisany cyfrowo na potrzeby analizy anomalii",
        "contact": "224270@edu.p.lodz.pl",
        "location": "lodz",
        "signingdate": date,
        "reason": "Dokument podpisany cyfrowo",
        "password": "1234",
    }
    with open("cert.pfx", "rb") as fp:
        p12 = pkcs12.load_key_and_certificates(
            fp.read(), b"111", backends.default_backend()
        )
    fname = path
    datau = open(fname, "rb").read()
    datas = cms.sign(datau, dct, p12[0], p12[1], p12[2], "sha256")
    fname = fname.replace(".pdf", "-signed-cms.pdf")
    with open(fname, "wb") as fp:
        fp.write(datau)
        fp.write(datas)
    return fname


def get_last_sig(pdfdata: bytes) -> str:
    n = pdfdata.rfind(b"/ByteRange")
    start = pdfdata.find(b"[", n)
    stop = pdfdata.find(b"]", start)
    assert n != -1 and start != -1 and stop != -1
    br = [int(i, 10) for i in pdfdata[start + 1: stop].split()]
    contents = pdfdata[br[0] + br[1] + 1: br[2] - 1]
    # bcontents = bytes.fromhex(contents.decode("utf8"))
    # data1 = pdfdata[br[0]: br[0] + br[1]]
    # data2 = pdfdata[br[2]: br[2] + br[3]]
    # signedData = data1 + data2
    return contents.decode("utf8")


def sign_bytes(data: bytes) -> bytes:
    date = datetime.datetime.utcnow() - datetime.timedelta(hours=12)
    date = date.strftime("D:%Y%m%d%H%M%S+00'00'")
    dct = {
        "aligned": 0,
        "sigflags": 3,
        "sigflagsft": 132,
        "sigpage": 0,
        "sigbutton": True,
        "sigfield": load_prev_block(),
        # "sigfield": "Signature1",
        "auto_sigfield": True,
        "sigandcertify": True,
        "signaturebox": (470, 840, 570, 640),
        "signature": "Dokument podpisany cyfrowo na potrzeby analizy anomalii",
        "contact": "224270@edu.p.lodz.pl",
        "location": "lodz",
        "signingdate": date,
        "reason": "Dokument podpisany cyfrowo",
        "password": "1234",
    }
    with open("cert.pfx", "rb") as fp:
        key, cert, othercerts = pkcs12.load_key_and_certificates(
            fp.read(), b"111", backends.default_backend()
        )
    # data = chain_previous(data, get_prev_sign())
    data_signed = b''.join([
        data,
        cms.sign(data, dct, key, cert, othercerts, "sha256"),
    ])
    sig = get_last_sig(data_signed)
    save_new_block(sig)
    return data_signed


def get_id_from_block(block: str) -> str:
    prefix_len = len(f'{BLOCK_PREFIX};')
    block_id_end = block.find(';', prefix_len)
    return block[prefix_len: block_id_end]


def verify_last_block(data: bytes) -> bool:
    pdf_reader = PdfFileReader(io.BytesIO(data))
    annotations = [annotation.getObject()
                   for page in pdf_reader.pages
                   for annotation in page['/Annots']
                   if '/Annots' in page
                   ]
    last_sig = get_last_sig(data)
    blocks = [annotation['/T']
              for annotation in annotations
              if '/T' in annotation and '/V' in annotation
              and str(annotation['/T']).startswith(f'{BLOCK_PREFIX};')
              and annotation['/V'].getObject()['/Contents'].hex() == last_sig
              ]
    if len(blocks) == 0:
        return False
    last_block = max(blocks, key=get_id_from_block)
    return load_block(get_id_from_block(last_block)) == last_block


def verify(data: bytes) -> bool:
    # TODO: add trusted certs?
    hashok, signatureok, certok = pdf.verify(data)
    return hashok and signatureok and verify_last_block(data)
