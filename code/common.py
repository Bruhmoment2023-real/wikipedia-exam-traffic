"""Shared helpers: paths, polite HTTP session, disk cache."""
import gzip, hashlib, json, os, re, sys, time
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CACHE = DATA / "cache"
RESULTS = ROOT / "results"
for p in (DATA, CACHE, RESULTS):
    p.mkdir(parents=True, exist_ok=True)

# Wikimedia asks every client for a descriptive User-Agent (project name and purpose; no personal address) and for
# requests to be made one at a time ("wait for each request to finish before sending another").
# https://doc.wikimedia.org/generated-data-platform/aqs/analytics-api/documentation/access-policy.html
UA = ("WikiExamTraffic/0.1 (research on exam-season pageviews; "
      "project folder D:/Research-Publishing/05-wikipedia-exam-traffic; no contact address by policy) python-requests/%s" % requests.__version__)
MIN_INTERVAL = 0.10  # seconds between requests; strictly sequential, never parallel

_session = None
_last = [0.0]


def session():
    global _session
    if _session is None:
        _session = requests.Session()
        _session.headers.update({"User-Agent": UA, "Accept-Encoding": "gzip"})
    return _session


def get(url, params=None, ok404=False, tries=6, timeout=60):
    """Sequential, rate-limited GET with exponential backoff on 429/5xx. Returns Response or None (404)."""
    for k in range(tries):
        wait = MIN_INTERVAL - (time.time() - _last[0])
        if wait > 0:
            time.sleep(wait)
        try:
            r = session().get(url, params=params, timeout=timeout)
            _last[0] = time.time()
        except requests.RequestException as e:
            print("  network error, retrying:", str(e)[:100], file=sys.stderr)
            time.sleep(5 * (k + 1))
            continue
        if r.status_code == 200:
            return r
        if r.status_code == 404 and ok404:
            return None
        if r.status_code in (429, 500, 502, 503, 504):
            ra = r.headers.get("Retry-After")
            time.sleep(float(ra) if ra and ra.isdigit() else 5 * (k + 1))
            continue
        raise RuntimeError("HTTP %s for %s" % (r.status_code, r.url))
    raise RuntimeError("gave up on %s" % url)


def cache_path(kind, key, ext=".json.gz"):
    h = hashlib.sha1(key.encode("utf8")).hexdigest()
    safe = re.sub(r"[^A-Za-z0-9_.-]", "_", key)[:60]
    d = CACHE / kind / h[:2]
    d.mkdir(parents=True, exist_ok=True)
    return d / (safe + "_" + h[:10] + ext)


def cached_json(kind, key, fetch):
    p = cache_path(kind, key)
    if p.exists():
        with gzip.open(p, "rt", encoding="utf8") as f:
            return json.load(f)
    obj = fetch()
    tmp = p.with_suffix(".tmp")
    with gzip.open(tmp, "wt", encoding="utf8") as f:
        json.dump(obj, f, ensure_ascii=False)
    os.replace(tmp, p)
    return obj


def mw_api(lang, **params):
    """Call the MediaWiki Action API of <lang>.wikipedia.org (or wikidata if lang == 'wikidata')."""
    host = "www.wikidata.org" if lang == "wikidata" else "%s.wikipedia.org" % lang
    params.update(format="json", formatversion=2, maxlag=5)
    return get("https://%s/w/api.php" % host, params=params).json()


def chunks(seq, n):
    seq = list(seq)
    for i in range(0, len(seq), n):
        yield seq[i:i + n]
