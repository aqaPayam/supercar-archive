"""Portable manifest fingerprints with compatibility for existing import records."""
import hashlib


def manifest_checksums(raw):
    """Return LF and legacy CRLF fingerprints, changing only line endings.

    JSON content, escaping, whitespace and field ordering remain significant.
    Existing database markers must not be rewritten during a repeat import.
    """
    lf = raw.replace(b'\r\n', b'\n')
    return (hashlib.sha256(lf).hexdigest(),
            hashlib.sha256(lf.replace(b'\n', b'\r\n')).hexdigest())
