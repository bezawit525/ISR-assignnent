import math
import os
import re
from collections import Counter, defaultdict


BASE_DIR = os.path.dirname(__file__)
REPO_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

CRAN_DIR = os.path.join(REPO_DIR, "datasets", "cran")
CRAN_DOCS = os.path.join(CRAN_DIR, "cran.all.1400")
CRAN_QUERIES = os.path.join(CRAN_DIR, "cran.qry")

OUT_DIR = os.path.join(BASE_DIR, "cranfield_runs")

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "has", "he", "in", "is",
    "it", "its", "of", "on", "that", "the", "to", "was", "were", "will", "with",
}


_TOKEN_RE = re.compile(r"[a-z0-9]+(?:\.[a-z0-9]+)*")


def tokenize(text: str):
    terms = []
    for m in _TOKEN_RE.finditer(text.lower()):
        t = m.group(0)
        if t and t not in STOPWORDS:
            terms.append(t)
    return terms


def parse_cran_docs(path: str):
    docs = {}
    cur_id = None
    in_w = False
    buf = []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for raw in f:
            line = raw.rstrip("\n")
            if line.startswith(".I "):
                if cur_id is not None:
                    docs[cur_id] = " ".join(buf).strip()
                cur_id = line.split()[1]
                in_w = False
                buf = []
            elif line.startswith(".W"):
                in_w = True
            elif line.startswith("."):
                in_w = False
            else:
                if in_w and cur_id is not None:
                    buf.append(line.strip())
    if cur_id is not None:
        docs[cur_id] = " ".join(buf).strip()
    return docs


def parse_cran_queries(path: str):
    queries = {}
    cur_id = None
    in_w = False
    buf = []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for raw in f:
            line = raw.rstrip("\n")
            if line.startswith(".I "):
                if cur_id is not None:
                    queries[cur_id] = " ".join(buf).strip()
                cur_id = line.split()[1]
                in_w = False
                buf = []
            elif line.startswith(".W"):
                in_w = True
            elif line.startswith("."):
                in_w = False
            else:
                if in_w and cur_id is not None:
                    buf.append(line.strip())
    if cur_id is not None:
        queries[cur_id] = " ".join(buf).strip()
    return queries


def build_inverted_index(docs: dict[str, str]):
    postings = defaultdict(dict)  # term -> docid -> (tf, positions)
    doc_len = {}
    cf = Counter()

    for docid, text in docs.items():
        terms = tokenize(text)
        doc_len[docid] = len(terms)
        positions_by_term = defaultdict(list)
        for i, t in enumerate(terms, start=1):
            positions_by_term[t].append(i)
            cf[t] += 1
        for t, pos in positions_by_term.items():
            postings[t][docid] = (len(pos), pos)

    return postings, doc_len, cf


def score_okapi_tf(query_terms: list[str], postings, doc_len, avgdl: float):
    scores = defaultdict(float)
    for t in query_terms:
        plist = postings.get(t)
        if not plist:
            continue
        for docid, (tf, _pos) in plist.items():
            dl = doc_len[docid]
            scores[docid] += tf / (tf + 0.5 + 1.5 * (dl / avgdl))
    return scores


def score_bm25(query_terms: list[str], postings, doc_len, avgdl: float, D: int):
    k1 = 1.2
    b = 0.75
    qtf = Counter(query_terms)

    scores = defaultdict(float)
    for t, tf_q in qtf.items():
        plist = postings.get(t)
        if not plist:
            continue
        df = len(plist)
        idf = math.log((D + 0.5) / (df + 0.5))
        for docid, (tf, _pos) in plist.items():
            dl = doc_len[docid]
            denom = tf + k1 * (1 - b + b * (dl / avgdl))
            scores[docid] += idf * ((tf * (k1 + 1)) / denom) * (tf_q)
    return scores


def score_lm_laplace(query_terms: list[str], postings, doc_len, V: int):
    qtf = Counter(query_terms)
    scores = defaultdict(float)

    all_docids = list(doc_len.keys())
    for docid in all_docids:
        dl = doc_len[docid]
        s = 0.0
        for t, tf_q in qtf.items():
            tf = 0
            plist = postings.get(t)
            if plist and docid in plist:
                tf = plist[docid][0]
            p = (tf + 1.0) / (dl + V)
            s += tf_q * math.log(p)
        scores[docid] = s
    return scores


def write_runfile(path: str, qid: str, scores: dict[str, float], topk: int = 1000):
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:topk]
    with open(path, "a", encoding="utf-8") as f:
        for rank, (docid, score) in enumerate(ranked, start=1):
            f.write(f"{qid} Q0 {docid} {rank} {score} Exp\n")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    docs = parse_cran_docs(CRAN_DOCS)
    queries = parse_cran_queries(CRAN_QUERIES)

    postings, doc_len, _cf = build_inverted_index(docs)
    D = len(doc_len)
    avgdl = sum(doc_len.values()) / float(D)
    V = len(postings)

    okapi_path = os.path.join(OUT_DIR, "cran_okapi_tf.run")
    bm25_path = os.path.join(OUT_DIR, "cran_bm25.run")
    laplace_path = os.path.join(OUT_DIR, "cran_lm_laplace.run")

    for p in (okapi_path, bm25_path, laplace_path):
        if os.path.exists(p):
            os.remove(p)

    for qid, qtext in queries.items():
        q_terms = tokenize(qtext)

        ok_scores = score_okapi_tf(q_terms, postings, doc_len, avgdl)
        bm_scores = score_bm25(q_terms, postings, doc_len, avgdl, D)
        lm_scores = score_lm_laplace(q_terms, postings, doc_len, V)

        write_runfile(okapi_path, qid, ok_scores)
        write_runfile(bm25_path, qid, bm_scores)
        write_runfile(laplace_path, qid, lm_scores)

    print("DONE")
    print("runs_dir=", OUT_DIR)
    print("D=", D)
    print("V=", V)


if __name__ == "__main__":
    main()
