import time, os, re
from seleniumbase import SB

LOCAL_PROXY = "http://127.0.0.1:8080"

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)

def find_ext_path():
    base = os.path.abspath("./nopecha_ext")
    if os.path.exists(os.path.join(base, "manifest.json")):
        return base
    for entry in os.listdir(base):
        sub = os.path.join(base, entry)
        if os.path.isdir(sub) and os.path.exists(os.path.join(sub, "manifest.json")):
            return sub
    raise FileNotFoundError(f"manifest.json not found under {base}")

ext_path = find_ext_path()
log(f"ext_path: {ext_path}")

with SB(
    uc=True,
    test=True,
    proxy=LOCAL_PROXY,
    extension_dir=ext_path,
) as sb:
    # 1. 直接看extensions页
    sb.open("chrome://extensions/")
    time.sleep(3)
    sb.save_screenshot("ext_check.png", folder=".")
    log("extensions page saved")

    # 2. 访问nopecha setup，看是否显示正常界面
    sb.open("https://nopecha.com/setup#")
    time.sleep(4)
    sb.save_screenshot("nopecha_setup.png", folder=".")
    page = sb.get_page_source()
    if "required to view" in page:
        log("❌ Extension NOT loaded")
    else:
        log("✅ Extension loaded OK")
