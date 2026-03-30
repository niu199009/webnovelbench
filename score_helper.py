"""
Helper script for WebNovelBench scoring.
Takes 8 dimension scores (1-5) as arguments, computes normalized score and percentile.

Usage:
    python score_helper.py 3.5 3.5 4.0 3.8 4.1 3.9 4.1 4.0

Output (JSON):
    {"scores": [3.5, 3.5, 4.0, 3.8, 4.1, 3.9, 4.1, 4.0], "normalized_score": 0.8749, "percentile": 99.31}
"""
import json
import sys
import numpy as np
from scipy.stats import percentileofscore


SCORE_DIMENSIONS = [
    "修辞手法", "感官描述丰富度", "角色平衡度", "角色对白独特性",
    "角色一致性", "意境匹配度", "语境适配度", "跨场景衔接度"
]


def load_fixed_parameters(path="fixed_parameters.json"):
    with open(path, "r") as f:
        return json.load(f)


def compute_normalized_score(scores, params):
    mean = np.array(params["mean"])
    std = np.array(params["std"])
    weights = np.array(params["weights"])
    min_score = params["min_score"]
    max_score = params["max_score"]
    existing_scores = np.array(params["normalized_existing_scores"])

    standardized = (np.array(scores) - mean) / std
    combined = standardized.dot(weights)
    normalized = (combined - min_score) / (max_score - min_score)
    percentile = percentileofscore(existing_scores, normalized, kind='rank')

    return round(float(normalized), 4), round(float(percentile), 2)


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--dimensions":
        for i, dim in enumerate(SCORE_DIMENSIONS):
            print(f"{i+1}. {dim}")
        return

    if len(sys.argv) != 9:
        print(f"Usage: python {sys.argv[0]} <score1> <score2> ... <score8>")
        print(f"Dimensions: {', '.join(SCORE_DIMENSIONS)}")
        sys.exit(1)

    scores = [float(x) for x in sys.argv[1:9]]
    params = load_fixed_parameters()
    normalized, percentile = compute_normalized_score(scores, params)

    result = {
        "dimensions": {dim: score for dim, score in zip(SCORE_DIMENSIONS, scores)},
        "normalized_score": normalized,
        "percentile": percentile
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
