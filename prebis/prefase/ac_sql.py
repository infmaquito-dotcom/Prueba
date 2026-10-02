"""Lee los volcados SQL de AzerothCore (data/sql/base/db_world/*.sql) sin necesitar MySQL.

Cada tabla se devuelve como lista de dicts con los nombres de columna del CREATE TABLE.
"""
import pickle
import re
from pathlib import Path


def _columns(text):
    m = re.search(r"CREATE TABLE `\w+` \((.*?)\n\) ENGINE", text, re.S)
    return re.findall(r"^\s+`(\w+)`", m.group(1), re.M)


def _rows(text):
    """Recorre las tuplas de todos los INSERT ... VALUES (...),(...);"""
    i, n = 0, len(text)
    while True:
        i = text.find("INSERT INTO", i)
        if i < 0:
            return
        i = text.index("VALUES", i) + 6
        while True:
            while text[i] in " \n\r\t,":
                i += 1
            if text[i] == ";":
                break
            assert text[i] == "(", text[i:i + 50]
            i += 1
            row = []
            while True:
                c = text[i]
                if c == "'":
                    j, buf = i + 1, []
                    while True:
                        k = text[j]
                        if k == "\\":
                            buf.append({"n": "\n", "r": "\r", "t": "\t", "0": "\0"}.get(text[j + 1], text[j + 1]))
                            j += 2
                        elif k == "'":
                            if text[j + 1] == "'":
                                buf.append("'")
                                j += 2
                            else:
                                break
                        else:
                            buf.append(k)
                            j += 1
                    row.append("".join(buf))
                    i = j + 1
                else:
                    j = i
                    while text[j] not in ",)":
                        j += 1
                    tok = text[i:j].strip()
                    if tok == "NULL":
                        row.append(None)
                    else:
                        try:
                            row.append(int(tok))
                        except ValueError:
                            row.append(float(tok))
                    i = j
                if text[i] == ",":
                    i += 1
                    continue
                if text[i] == ")":
                    i += 1
                    yield row
                    break


def load(path, keep=None, where=None):
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    cols = _columns(text)
    out = []
    for r in _rows(text):
        d = dict(zip(cols, r))
        if where and not where(d):
            continue
        if keep:
            d = {k: d[k] for k in keep if k in d}
        out.append(d)
    return out


def cached(cache_dir, name, path, **kw):
    cache = Path(cache_dir) / f"{name}.pkl"
    if cache.exists():
        return pickle.loads(cache.read_bytes())
    data = load(path, **kw)
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_bytes(pickle.dumps(data))
    return data
