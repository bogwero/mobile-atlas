
import logging

import dns.resolver
from mobileatlas.probe.measurement.mediator.mobile_atlas_mediator import MobileAtlasMediator
from .payload_network_base import PayloadNetworkBase, PayloadNetworkResult

logger = logging.getLogger(__name__)


class PayloadNetworkDns(PayloadNetworkBase):
    LOGGER_TAG = "payload_network_dns"

    def __init__(self, mobile_atlas_mediator: MobileAtlasMediator, payload_size):
        super().__init__(mobile_atlas_mediator, payload_size=payload_size)
        
    def send_payload(self) -> PayloadNetworkResult:
        cnt = 0
        my_resolver = dns.resolver.Resolver()
        with open("mobileatlas/probe/measurement/payload/res/tranco_V78N.txt") as file:
            for line in file:
                domain = line.strip()
                cnt += 1
                try:
                    results = my_resolver.resolve(domain, 'A', raise_on_no_answer=False)
                except (dns.resolver.LifetimeTimeout, dns.resolver.NXDOMAIN, dns.resolver.YXDOMAIN, dns.resolver.NoAnswer) as e:
                    pass                    
                if self.is_payload_consumed():
                    break
        return PayloadNetworkResult(True, None, *self.get_consumed_bytes(), cnt)
                