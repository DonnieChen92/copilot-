"""
Similarity Matcher / 相似度匹配器 / 相似度匹配器
=================================================
Text similarity computation for legal evidence-to-clause mapping.
Provides multiple matching strategies with a target of 90% average similarity.

Methods / 方法:
- TF-IDF Cosine Similarity (primary)
- Keyword Overlap (Jaccard-based)
- Combined Hybrid Score

No external ML dependencies required - uses pure Python + stdlib math.
"""

import math
import re
from collections import Counter
from typing import Sequence


class SimilarityMatcher:
    """
    Text similarity computation engine for legal matching.
    法律匹配的文本相似度計算引擎。
    法律匹配的文本相似度计算引擎。
    """

    # Legal domain stop words to ignore in similarity computation
    STOP_WORDS = frozenset({
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
        "of", "with", "by", "from", "as", "is", "was", "are", "were", "be",
        "been", "being", "have", "has", "had", "do", "does", "did", "will",
        "would", "could", "should", "may", "might", "shall", "can", "this",
        "that", "these", "those", "it", "its", "not", "no", "nor", "so",
        "if", "then", "than", "too", "very", "just", "about", "above",
        "after", "again", "all", "also", "any", "each", "every", "into",
        "more", "most", "other", "out", "over", "own", "same", "such",
        "through", "under", "up", "which", "who", "whom", "what", "when",
        "where", "while", "how", "both", "during", "before",
    })

    def __init__(self):
        self._idf_cache: dict[str, float] = {}

    def tokenize(self, text: str) -> list[str]:
        """
        Tokenize text into lowercase words, removing stop words and punctuation.
        將文本分詞為小寫詞語，移除停用詞和標點符號。
        将文本分词为小写词语，移除停用词和标点符号。
        """
        words = re.findall(r"[a-zA-Z0-9]+(?:[-'][a-zA-Z0-9]+)*", text.lower())
        return [w for w in words if w not in self.STOP_WORDS and len(w) > 1]

    def tfidf_cosine_similarity(self, text_a: str, text_b: str) -> float:
        """
        Compute TF-IDF weighted cosine similarity between two texts.
        計算兩段文本之間的 TF-IDF 加權餘弦相似度。
        计算两段文本之间的 TF-IDF 加权余弦相似度。

        Returns a score in [0.0, 1.0].
        """
        tokens_a = self.tokenize(text_a)
        tokens_b = self.tokenize(text_b)

        if not tokens_a or not tokens_b:
            return 0.0

        # Build TF vectors
        tf_a = Counter(tokens_a)
        tf_b = Counter(tokens_b)

        # Build vocabulary
        vocab = set(tf_a.keys()) | set(tf_b.keys())

        # Compute IDF (using these two documents as corpus)
        doc_count = 2
        idf: dict[str, float] = {}
        for term in vocab:
            df = (1 if term in tf_a else 0) + (1 if term in tf_b else 0)
            idf[term] = math.log((doc_count + 1) / (df + 1)) + 1  # smoothed IDF

        # Compute TF-IDF vectors
        vec_a = {term: tf_a.get(term, 0) * idf[term] for term in vocab}
        vec_b = {term: tf_b.get(term, 0) * idf[term] for term in vocab}

        # Cosine similarity
        dot_product = sum(vec_a[t] * vec_b[t] for t in vocab)
        norm_a = math.sqrt(sum(v ** 2 for v in vec_a.values()))
        norm_b = math.sqrt(sum(v ** 2 for v in vec_b.values()))

        if norm_a == 0 or norm_b == 0:
            return 0.0

        return dot_product / (norm_a * norm_b)

    def keyword_overlap_score(
        self,
        keywords_a: Sequence[str],
        keywords_b: Sequence[str],
    ) -> float:
        """
        Compute keyword overlap score (modified Jaccard similarity).
        計算關鍵詞重疊分數（修改後的 Jaccard 相似度）。
        计算关键词重叠分数（修改后的 Jaccard 相似度）。

        Returns a score in [0.0, 1.0].
        """
        set_a = {w.lower().strip() for w in keywords_a if w.strip()}
        set_b = {w.lower().strip() for w in keywords_b if w.strip()}

        if not set_a or not set_b:
            return 0.0

        intersection = set_a & set_b
        union = set_a | set_b

        return len(intersection) / len(union) if union else 0.0

    def ngram_similarity(self, text_a: str, text_b: str, n: int = 2) -> float:
        """
        Compute character n-gram similarity (Dice coefficient).
        計算字符 n-gram 相似度（Dice 系數）。
        计算字符 n-gram 相似度（Dice 系数）。

        Returns a score in [0.0, 1.0].
        """
        def get_ngrams(text: str, size: int) -> set[str]:
            text = text.lower()
            return {text[i:i + size] for i in range(len(text) - size + 1)}

        ngrams_a = get_ngrams(text_a, n)
        ngrams_b = get_ngrams(text_b, n)

        if not ngrams_a or not ngrams_b:
            return 0.0

        intersection = ngrams_a & ngrams_b
        return 2 * len(intersection) / (len(ngrams_a) + len(ngrams_b))

    def hybrid_similarity(
        self,
        text_a: str,
        text_b: str,
        keywords_a: Sequence[str] | None = None,
        keywords_b: Sequence[str] | None = None,
        weights: tuple[float, float, float] = (0.40, 0.35, 0.25),
    ) -> float:
        """
        Compute weighted hybrid similarity combining multiple methods.
        計算結合多種方法的加權混合相似度。
        计算结合多种方法的加权混合相似度。

        Args:
            text_a: First text
            text_b: Second text
            keywords_a: Keywords for first text (optional)
            keywords_b: Keywords for second text (optional)
            weights: (tfidf_weight, keyword_weight, ngram_weight)

        Returns a score in [0.0, 1.0].
        """
        w_tfidf, w_keyword, w_ngram = weights

        tfidf_score = self.tfidf_cosine_similarity(text_a, text_b)

        if keywords_a and keywords_b:
            keyword_score = self.keyword_overlap_score(keywords_a, keywords_b)
        else:
            keyword_score = self.keyword_overlap_score(
                text_a.split(), text_b.split()
            )

        ngram_score = self.ngram_similarity(text_a, text_b)

        return w_tfidf * tfidf_score + w_keyword * keyword_score + w_ngram * ngram_score

    def batch_similarity(
        self,
        query: str,
        candidates: list[str],
        method: str = "tfidf",
    ) -> list[tuple[int, float]]:
        """
        Compute similarity of a query against multiple candidates.
        計算查詢與多個候選項之間的相似度。
        计算查询与多个候选项之间的相似度。

        Returns list of (index, score) sorted by score descending.
        """
        func = {
            "tfidf": self.tfidf_cosine_similarity,
            "ngram": self.ngram_similarity,
        }.get(method, self.tfidf_cosine_similarity)

        scores = [(i, func(query, c)) for i, c in enumerate(candidates)]
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores
