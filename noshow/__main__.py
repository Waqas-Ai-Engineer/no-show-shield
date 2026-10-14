import argparse, sys
from .core import analyze, render

def main():
    p = argparse.ArgumentParser(prog="noshow", description="No-show risk scoring for appointments")
    p.add_argument("csv", nargs="?", default="examples/appointments.csv")
    p.add_argument("--avg-value", type=float, default=0.0, help="average revenue per appointment")
    a = p.parse_args()
    try:
        text = open(a.csv, encoding="utf-8").read()
    except OSError as e:
        sys.exit(f"cannot read {a.csv}: {e}")
    print(render(analyze(text, a.avg_value), a.avg_value))

main()
