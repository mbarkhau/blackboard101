# Super simple Elliptic Curve Presentation. No libraries, wrappers, nothing.
# For educational purposes only

# These are the public specs for Bitcoin's curve - the secp256k1

Pcurve = 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 - 1 # The proven prime
# Number of points in the field (cardinality)
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

# Parameters of the elliptic curve. y^2 = x^3 + Acurve * x + Bcurve
Acurve = 0
Bcurve = 7

import collections
ECPoint = collections.namedtuple("ECPoint", "x, y")

# This is our generator point. Trillions of dif ones possible
Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
G = ECPoint(Gx, Gy)


def modinv(a, n): # Extended Euclidean Algorithm ('division' in EC math)
    lm, hm = 1, 0
    low, high = a % n, n
    while low > 1:
        ratio = high / low
        nm = hm - lm * ratio
        new = high - low * ratio
        lm, low, hm, high = nm, new, lm, low
    return lm % n


def ECadd(p, q):
    l = ((q.y - p.y) * modinv(q.x - p.x, Pcurve)) % Pcurve
    x = (l * l - p.x - q.x) % Pcurve
    y = (l * (p.x - x) - p.y) % Pcurve
    return ECPoint(x, y)


def ECdouble(p):
    l = ((3 * p.x * p.x + Acurve) * modinv((2 * p.y), Pcurve)) % Pcurve
    x = (l * l - 2 * p.x) % Pcurve
    y = (l * (p.x - x) - p.y) % Pcurve
    return ECPoint(x, y)


def ECMultiply(p, n):
    if not (0 < n < N):
        raise Exception("Invalid Scalar/Private Key")

    q = p
    for bit in bin(n)[3:]:
        q = ECdouble(q)
        if bit == "1":
            q = ECadd(q, p)
    return q


#Individual Transaction/Personal Information
#replace with any private key
privKey = 0xA0DC65FFCA799873CBEA0AC274015B9526505DAAAED385155425F7337704883E

pubKey = ECMultiply(G, privKey)  # public key generation

print """
The private key:
{}

The uncompressed public key (not address):
{}

The official Public Key - compressed:
{}
""".format(privKey, pubKey.x, "02{:064x}".format(pubKey.x))
