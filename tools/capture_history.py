"""Append canonical changes after an evidence-backed edit, before rendering/validation."""
import argparse
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.knowledge import ROOT, capture

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--observed-at', required=True)
    parser.add_argument('--effective-from', default=None)
    parser.add_argument('--reason', required=True)
    parser.add_argument('--evidence', nargs='+', required=True)
    args = parser.parse_args()
    changes = capture(ROOT, args.observed_at, args.reason, args.evidence, args.effective_from)
    print(f'Appended {len(changes)} revision(s).')
