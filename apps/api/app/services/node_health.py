import json
import socket
import ssl
import time
from shared import models
from shared.config import get_settings

settings = get_settings()


def _meta(node: models.Node):
    try:
        return json.loads(node.meta_json or '{}')
    except Exception:
        return {}


def tcp_tls_check(host: str, port: int, sni: str):
    start = time.perf_counter()
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        with socket.create_connection((host, port), timeout=4) as sock:
            with ctx.wrap_socket(sock, server_hostname=sni) as ssock:
                ssock.do_handshake()
        return {'ok': True, 'latency_ms': round((time.perf_counter() - start) * 1000, 2), 'detail': 'tls handshake ok', 'confidence': 'high'}
    except Exception as exc:
        return {'ok': False, 'latency_ms': None, 'detail': f'tls failed: {exc}', 'confidence': 'high'}


def udp_probe(host: str, port: int):
    start = time.perf_counter()
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(2)
            sock.sendto(b'ping', (host, port))
            try:
                sock.recvfrom(64)
                detail = 'udp response received'
            except socket.timeout:
                detail = 'udp sent, no response'
        return {'ok': True, 'latency_ms': round((time.perf_counter() - start) * 1000, 2), 'detail': detail, 'confidence': 'medium'}
    except Exception as exc:
        return {'ok': False, 'latency_ms': None, 'detail': f'udp failed: {exc}', 'confidence': 'medium'}


def check_node(node: models.Node):
    meta = _meta(node)
    if node.type == 'reality':
        return {'name': node.name, 'type': node.type, 'enabled': node.enabled, 'check': tcp_tls_check(node.server, node.port, meta.get('sni', settings.reality_sni))}
    if node.type == 'hy2':
        return {'name': node.name, 'type': node.type, 'enabled': node.enabled, 'check': udp_probe(node.server, node.port)}
    return {'name': node.name, 'type': node.type, 'enabled': node.enabled, 'check': {'ok': False, 'latency_ms': None, 'detail': 'unknown type', 'confidence': 'low'}}
