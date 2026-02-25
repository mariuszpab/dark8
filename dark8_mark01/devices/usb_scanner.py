import usb.core
import usb.util

def scan_usb_devices():
    try:
        devices = usb.core.find(find_all=True)
    except Exception as e:
        return [{"error": f"USB backend not available: {e}"}]

    result = []
    for dev in devices:
        try:
            result.append({
                "vendor": hex(dev.idVendor),
                "product": hex(dev.idProduct),
                "bus": getattr(dev, "bus", None),
                "address": getattr(dev, "address", None),
            })
        except Exception:
            # ignore devices we cannot inspect
            continue

    return result
