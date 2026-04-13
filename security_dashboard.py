import time
import os
from security import (
    scan_directory,
    SECURITY_STATE,
    get_anomaly_report
)


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def render_header():
    print("\n🛡️ L.U.M.E.N SECURITY CONTROL CENTER")
    print("=" * 50)


def render_state():
    print("\n📊 SYSTEM STATUS")
    print(f"Threats detected: {SECURITY_STATE['threats_detected']}")
    print(f"Last scan: {SECURITY_STATE['last_scan']}")
    print("-" * 50)


def render_anomalies():
    report = get_anomaly_report()

    print("\n🧬 BEHAVIOR ANALYSIS")

    print(f"Total actions tracked: {report['total_actions']}")
    print("Action distribution:")

    for k, v in report["distribution"].items():
        print(f"  - {k}: {v}")

    print(f"Anomaly score: {report['anomaly_score']}")


def render_threats(results):
    print("\n🚨 THREAT REPORT")

    if not results:
        print("No threats detected.")
        return

    for r in results:
        print(f"\nFile: {r['file']}")
        print(f"Risk: {r['risk_score']}")
        print(f"Triggers: {', '.join(r['triggers'])}")


def run_dashboard(folder="."):
    print("\nStarting security dashboard...\n")

    while True:
        clear()

        render_header()

        results = scan_directory(folder)

        render_state()
        render_anomalies()
        render_threats(results)

        print("\nRefreshing in 10s... (CTRL+C to exit)")

        time.sleep(10)