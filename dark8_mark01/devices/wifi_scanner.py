import subprocess


def scan_wifi_networks():
    """
    Skaner Wi‑Fi dla DARK8‑OS (Linux / własny OS).
    Zakładamy dostępność narzędzi systemowych (np. nmcli / iwlist).
    """

    try:
        result = subprocess.check_output(
            ["nmcli", "-t", "-f", "SSID,SIGNAL", "device", "wifi", "list"],
            encoding="utf-8",
            errors="ignore",
        )
    except Exception:
        return []

    networks = []

    for line in result.splitlines():
        if not line.strip():
            continue
        parts = line.split(":")
        if len(parts) >= 2:
            ssid = parts[0].strip()
            signal = parts[1].strip()
            networks.append({"ssid": ssid, "signal": signal})

    return networks
