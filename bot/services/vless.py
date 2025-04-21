def generate_vless_link(user_uuid: str, username: str = "") -> str:
    return (
        f"vless://{user_uuid}@ge-realty.youfast.click:443"
        f"?flow=xtls-rprx-vision&security=reality&type=tcp"
        f"&alpn=http/1.1&sni=11uh.top&fp=chrome"
        f"&pbk=SbVKOEMjK0sIlbwg4akyBg5mL5KZwwB-ed4eEE7YnRc"
        f"#🇩🇪 Германия (GE)(Trial)"
    )