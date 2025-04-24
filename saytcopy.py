import os, re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

os.system("clear")

print("=== (HackLab)LyonX Site Kopyalayıcı Tool ===")

def sanitize_filename(name):
    return re.sub(r'[^\w\-_.]', '_', name)

try:
    count = int(input("Kopyalamak istediğin site miktarı (Max 4): "))
    if count > 4 or count < 1:
        raise ValueError("1-4 arası rakam ver")

    urls = []
    for i in range(count):
        url = input(f"{i+1}. site linki (https:// ile): ").strip()
        urls.append(url)

    headers = {"User-Agent": "Mozilla/5.0"}
    os.makedirs("project/css", exist_ok=True)
    os.makedirs("project/js", exist_ok=True)
    os.makedirs("project/images", exist_ok=True)

    used_files = set()
    page_names = []

    for index, url in enumerate(urls, start=1):
        print(f"[{index}] {url} yükleniyor...")
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")

        # CSS
        for tag in soup.find_all("link", href=True):
            href = tag["href"]
            if ".css" in href:
                full = urljoin(url, href)
                name = sanitize_filename(os.path.basename(urlparse(href).path))
                if name not in used_files:
                    try:
                        res = requests.get(full, headers=headers)
                        with open(f"project/css/{name}", "wb") as f:
                            f.write(res.content)
                        used_files.add(name)
                    except: pass
                tag["href"] = f"css/{name}"

        # JS
        for tag in soup.find_all("script", src=True):
            src = tag["src"]
            if ".js" in src:
                full = urljoin(url, src)
                name = sanitize_filename(os.path.basename(urlparse(src).path))
                if name not in used_files:
                    try:
                        res = requests.get(full, headers=headers)
                        with open(f"project/js/{name}", "wb") as f:
                            f.write(res.content)
                        used_files.add(name)
                    except: pass
                tag["src"] = f"js/{name}"

        # IMG
        for tag in soup.find_all("img", src=True):
            src = tag["src"]
            full = urljoin(url, src)
            name = sanitize_filename(os.path.basename(urlparse(src).path))
            if name not in used_files:
                try:
                    res = requests.get(full, headers=headers)
                    with open(f"project/images/{name}", "wb") as f:
                        f.write(res.content)
                    used_files.add(name)
                except: pass
            tag["src"] = f"images/{name}"

        # Internal a tag link fix (optional)
        for tag in soup.find_all("a", href=True):
            href = tag["href"]
            if any(page_url in href for page_url in urls):
                page_index = urls.index(href) + 1
                tag["href"] = f"page{page_index}.html"

        page_file = f"page{index}.html"
        with open(f"project/{page_file}", "w", encoding="utf-8") as f:
            f.write(soup.prettify())
        page_names.append(page_file)

        print(f"[✓] Kayd edildi: project/{page_file}")

    print("\n[✓] Bütün siteler kopyalandı.")
    print("[i] HackLab tercih etdiğiniz için teşekkürler.")

except Exception as e:
    print(f"[X] Hata: {e}")