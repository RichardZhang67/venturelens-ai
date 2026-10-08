import math

def score_startup_count(startup_count):
    """
    Score the number of startups in a category.
    Maximum score: 15 points.
    """
    if startup_count >= 20:
        return 15
    elif startup_count >= 15:
        return 12
    elif startup_count >= 10:
        return 8
    elif startup_count >= 5:
        return 5
    else:
        return 2

# %%
def score_average_funding(average_funding):
    """
    Score average funding amount.
    Maximum score: 20 points.
    """
    if average_funding is None:
        return 0

    if average_funding >= 1_000_000_000:
        return 20
    elif average_funding >= 500_000_000:
        return 16
    elif average_funding >= 100_000_000:
        return 12
    elif average_funding >= 10_000_000:
        return 8
    elif average_funding > 0:
        return 4
    else:
        return 0

# %%
MANUAL_CATEGORY_SCORES = {
    "Education Technology": {
        "growth_potential": 12,
        "problem_importance": 12,
        "teen_accessibility": 20,
        "competition_level": 12
    },
    "Artificial Intelligence": {
        "growth_potential": 15,
        "problem_importance": 12,
        "teen_accessibility": 10,
        "competition_level": 8
    },
    "Healthcare": {
        "growth_potential": 12,
        "problem_importance": 15,
        "teen_accessibility": 5,
        "competition_level": 6
    },
    "Fintech": {
        "growth_potential": 12,
        "problem_importance": 10,
        "teen_accessibility": 6,
        "competition_level": 6
    },
    "Climate Technology": {
        "growth_potential": 12,
        "problem_importance": 15,
        "teen_accessibility": 10,
        "competition_level": 12
    },
    "Gaming": {
        "growth_potential": 8,
        "problem_importance": 8,
        "teen_accessibility": 20,
        "competition_level": 8
    },
    "Consumer Apps": {
        "growth_potential": 8,
        "problem_importance": 8,
        "teen_accessibility": 16,
        "competition_level": 8
    },
    "Cybersecurity": {
        "growth_potential": 12,
        "problem_importance": 15,
        "teen_accessibility": 8,
        "competition_level": 10
    },
    "Productivity Software": {
        "growth_potential": 10,
        "problem_importance": 10,
        "teen_accessibility": 16,
        "competition_level": 10
    },
    "Robotics": {
        "growth_potential": 12,
        "problem_importance": 12,
        "teen_accessibility": 8,
        "competition_level": 10
    }
}

def calculate_opportunity_score(category, startup_count, average_funding):
    """
    Calculate the total opportunity score for a startup category.
    Maximum score: 100 points.
    """

    count_score = score_startup_count(startup_count)

    if average_funding is None or math.isnan(average_funding):
        funding_score = 0
    else:
        funding_score = score_average_funding(average_funding)

    manual_scores = MANUAL_CATEGORY_SCORES.get(category, {
        "growth_potential": 8,
        "problem_importance": 8,
        "teen_accessibility": 8,
        "competition_level": 8
    })

    growth_score = manual_scores["growth_potential"]
    problem_score = manual_scores["problem_importance"]
    teen_score = manual_scores["teen_accessibility"]
    competition_score = manual_scores["competition_level"]

    total_score = (
        count_score
        + funding_score
        + growth_score
        + problem_score
        + teen_score
        + competition_score
    )

    return {
        "category": category,
        "startup_count_score": count_score,
        "funding_score": funding_score,
        "growth_potential_score": growth_score,
        "problem_importance_score": problem_score,
        "teen_accessibility_score": teen_score,
        "competition_level_score": competition_score,
        "total_score": total_score
    }

# %%
def explain_recommendation(score_result):
    """
    Create a short explanation for a category recommendation.
    """

    category = score_result["category"]
    total_score = score_result["total_score"]

    strongest_factors = []

    if score_result["teen_accessibility_score"] >= 16:
        strongest_factors.append("high teen accessibility")

    if score_result["growth_potential_score"] >= 12:
        strongest_factors.append("strong growth potential")

    if score_result["problem_importance_score"] >= 12:
        strongest_factors.append("important problems")

    if score_result["funding_score"] >= 12:
        strongest_factors.append("strong funding signals")

    if score_result["competition_level_score"] >= 12:
        strongest_factors.append("possible student-friendly niches")

    if len(strongest_factors) == 0:
        reason = "balanced but moderate scores across the selected factors"
    else:
        reason = ", ".join(strongest_factors)

    explanation = (
        f"{category} received a score of {total_score} because it shows {reason}. "
        "This recommendation is based on a simple rule-based scoring system and should be used for exploration, not as a guaranteed prediction."
    )

    return explanation
