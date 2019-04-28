#!/usr/bin/env python


NAME = 'Wordfence (Feedjit)'


def is_waf(self):
    # Wordfence sometimes returns 403 to the directory in which
    # it is installed, hence using a more elaborate attack detection
    # method accurately detects the WAF, plus it requires only a
    # single request instead of two.
    for attack in self.attacks:
        r = attack(self)
        if r is None:
            return
        _, page = r
        # Separated the all in all fingerprint
        if b'Generated by Wordfence' in page:
            return True
        # Sometimes, the blockpage doesn't return the 'Generated by Wordfence' fingerprint
        if all(i in page for i in (b'A potentially unsafe operation has been detected in your request', b"Your computer's time:")):
            return True
    return False