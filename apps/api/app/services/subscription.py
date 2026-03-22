import base64
import json
from shared.config import get_settings
from shared import models

settings = get_settings()


def raw_links(user: models.User):
    reality = f"vless://{user.uuid}@{settings.server_address}:{settings.reality_port}?encryption=none&security=reality&sni={settings.reality_sni}&pbk={settings.reality_public_key}&sid={settings.reality_short_id}&type=tcp#Reality-{user.username}"
    hy2 = f"hysteria2://{user.sub_token}@{settings.server_address}:{settings.hy2_port}/?sni={settings.hy2_sni}&insecure=1#HY2-{user.username}"
    return "\n".join([reality, hy2])


def b64_links(user: models.User):
    return base64.b64encode(raw_links(user).encode()).decode()


def clash_profile(user: models.User):
    data = {
        'mixed-port': 7890,
        'mode': 'rule',
        'proxies': [
            {'name': f'Reality-{user.username}', 'type': 'vless', 'server': settings.server_address, 'port': settings.reality_port, 'uuid': user.uuid, 'tls': True, 'network': 'tcp'},
            {'name': f'HY2-{user.username}', 'type': 'hysteria2', 'server': settings.server_address, 'port': settings.hy2_port, 'password': user.sub_token, 'skip-cert-verify': True},
        ],
        'proxy-groups': [{'name': 'PROXY', 'type': 'select', 'proxies': [f'Reality-{user.username}', f'HY2-{user.username}', 'DIRECT']}],
        'rules': ['GEOIP,CN,DIRECT', 'MATCH,PROXY'],
    }
    import yaml
    return yaml.safe_dump(data, allow_unicode=True, sort_keys=False)
