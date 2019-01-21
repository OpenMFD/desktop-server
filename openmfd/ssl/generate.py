import datetime
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
import ipaddress

# from netifaces import interfaces, ifaddresses, AF_INET
#
#
# def ip4_addresses():
#     ip_list = []
#     for interface in interfaces():
#         for link in ifaddresses(interface)[AF_INET]:
#             ip_list.append(link['addr'])
#     return ip_list


def generate_instance_ssl(path: str):

    # print(ip4_addresses())
    # exit()

    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    with open(path + "/key.pem", 'wb') as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"GB"),
        # x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"CA"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"London"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"OpenMFD"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"localhost"),
    ])

    cert = x509.CertificateBuilder(
        issuer_name=issuer,
        subject_name=subject,
        public_key=key.public_key(),
        serial_number=x509.random_serial_number(),
        not_valid_before=datetime.datetime.utcnow(),
        not_valid_after=datetime.datetime.utcnow() + datetime.timedelta(days=10),
    ).sign(key, hashes.SHA256(), default_backend())

    # Write our cert out to disk.
    with open(path + "/cert.pem", "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
