# -*- coding: utf-8 -*-

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dnslog.settings")
import django
django.setup()
import copy
import re
import tempfile
from dnslib import RR, QTYPE, RCODE, TXT
from dnslib.server import DNSServer, DNSHandler, BaseResolver, DNSLogger
from logview.models import *
from dnslog import settings


class MysqlLogger():
    def log_data(self, dnsobj):
        pass

    def log_error(self, handler, e):
        pass

    def log_pass(self, *args):
        pass

    def log_prefix(self, handler):
        pass

    def log_recv(self, handler, data):
        pass

    def log_reply(self, handler, reply):
        pass

    def log_request(self, handler, request):
        domain = request.q.qname.__str__().lower()
        if domain.endswith(settings.DNS_DOMAIN + '.'):
            udomain = re.search(r'\.?([^\.]+)\.%s\.' % settings.DNS_DOMAIN,
                                domain)
            if udomain:
                user = User.objects.filter(udomain__exact=udomain.group(1))
                if not user and domain.strip(".") != settings.ADMIN_DOMAIN:
                    user = User.objects.filter(udomain__exact='@')
                if user:
                    dnslog = DNSLog(
                        user=user[0], host=domain, type=QTYPE[request.q.qtype])
                    dnslog.save()

    def log_send(self, handler, data):
        pass

    def log_truncated(self, handler, reply):
        pass


class ZoneResolver(BaseResolver):
    """
        Simple fixed zone file resolver.
    """

    def __init__(self, zone, glob=False):
        """
            Initialise resolver from zone file.
            Stores RRs as a list of (label,type,rr) tuples
            If 'glob' is True use glob match against zone file
        """
        self.zone = [(rr.rname, QTYPE[rr.rtype], rr)
                     for rr in RR.fromZone(zone)]
        self.glob = glob
        self.eq = 'matchGlob' if glob else '__eq__'

    def resolve(self, request, handler):
        """
            Respond to DNS request - parameters are request packet & handler.
            Method is expected to return DNS response
        """
        reply = request.reply()
        qname = request.q.qname
        qtype = QTYPE[request.q.qtype]
        if qtype == 'TXT':
            txtpath = os.path.join(tempfile.gettempdir(), str(qname).lower())
            if os.path.isfile(txtpath):
                reply.add_answer(
                    RR(qname, QTYPE.TXT, rdata=TXT(open(txtpath).read().strip())))
        for name, rtype, rr in self.zone:
            # Check if label & type match
            if getattr(qname,
                       self.eq)(name) and (qtype == rtype or qtype == 'ANY'
                                           or rtype == 'CNAME'):
                # If we have a glob match fix reply label
                if self.glob:
                    a = copy.copy(rr)
                    a.rname = qname
                    reply.add_answer(a)
                else:
                    reply.add_answer(rr)
                # Check for A/AAAA records associated with reply and
                # add in additional section
                if rtype in ['CNAME', 'NS', 'MX', 'PTR']:
                    for a_name, a_rtype, a_rr in self.zone:
                        if a_name == rr.rdata.label and a_rtype in [
                                'A', 'AAAA'
                        ]:
                            reply.add_ar(a_rr)
        if not reply.rr:
            reply.header.rcode = RCODE.NXDOMAIN
        return reply


def main():
    zone = '''
*.{dnsdomain}.       IN      NS      {ns1domain}.
*.{dnsdomain}.       IN      NS      {ns2domain}.
*.{dnsdomain}.       IN      A       {serverip}
{dnsdomain}.       IN      A       {serverip}
'''.format(
        dnsdomain=settings.DNS_DOMAIN,
        ns1domain=settings.NS1_DOMAIN,
        ns2domain=settings.NS2_DOMAIN,
        serverip=settings.SERVER_IP)
    resolver = ZoneResolver(zone, True)
    logger = MysqlLogger()
    print("Starting Zone Resolver (%s:%d) [%s]" % ("*", 53, "UDP"))

    udp_server = DNSServer(resolver, port=53, address='', logger=logger)
    udp_server.start()


if __name__ == '__main__':
    main()
