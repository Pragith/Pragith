"""Synchronize the company site's CallRenard publication record."""
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('target', type=Path, help='Company app/product-facts.json path')
parser.add_argument('--check', action='store_true')
args = parser.parse_args()
source = Path(__file__).resolve().parents[1] / 'app/content/product-facts.json'
if args.check:
    if source.read_bytes() != args.target.read_bytes():
        raise SystemExit('CallRenard publication records differ')
    print('CallRenard publication records match')
else:
    args.target.write_bytes(source.read_bytes())
