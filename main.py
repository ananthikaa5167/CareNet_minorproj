# Entry point for CareNet Algorithm

from data.sample_inputs import reports, ngos
from algorithm.routing_algorithm import route_vulnerability_case


def main():
    print("\n=== CareNet : Vulnerability Routing Algorithm ===\n")

    for report in reports:
        result = route_vulnerability_case(report, ngos)
        print("Input Report ID:", report["id"])
        print("Output:", result)
        print("-" * 50)


if __name__ == "__main__":
    main()
