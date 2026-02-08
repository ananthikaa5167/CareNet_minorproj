import math

# Calculate distance between two locations
def calculate_distance(lat1, lon1, lat2, lon2):
    return math.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)


# Compute priority score based on condition and time delay
def compute_priority(condition, time_delay):
    condition_weight = {
        "injured": 3,
        "hungry": 2,
        "alone": 1
    }

    return condition_weight.get(condition, 1) + (10 - time_delay)


# Find nearest NGO
def find_nearest_ngo(report, ngos):
    nearest = None
    min_distance = float("inf")

    for ngo in ngos:
        dist = calculate_distance(
            report["lat"], report["lon"],
            ngo["lat"], ngo["lon"]
        )

        if dist < min_distance:
            min_distance = dist
            nearest = ngo

    return nearest


# Main routing algorithm
def route_vulnerability_case(report, ngos):
    priority = compute_priority(
        report["condition"],
        report["time_delay"]
    )

    assigned_ngo = find_nearest_ngo(report, ngos)

    return {
        "report_id": report["id"],
        "priority_score": priority,
        "assigned_ngo": assigned_ngo["id"],
        "status": "ASSIGNED"
    }
