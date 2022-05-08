import sys
import datetime
from cryptography.hazmat import backends
from cryptography.hazmat.primitives.serialization import pkcs12

from endesive.pdf import cms


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
