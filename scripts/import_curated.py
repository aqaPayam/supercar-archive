"""Import a reviewed, evidence-backed batch of iconic performance cars."""
import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.import_supercars50 import apply_batch, ROOT


def import_curated(db_path, manifest_path, apply=False):
    data = json.loads(manifest_path.read_text(encoding='utf8'))
    count = data.get('expected_count')
    if type(count) is not int or not 1 <= count <= 1000:
        raise ValueError('Declare an expected_count between 1 and 1000')
    if len(data['cars']) != count:
        raise ValueError('Declared count does not match the reviewed batch')
    for car in data['cars']:
        reason = car.get('admission_reason', '')
        if not isinstance(reason, str) or len(reason.strip()) < 40:
            raise ValueError(f"Missing substantive admission reason: {car['id']}")
        if not any(fact['explanation'] == reason for fact in car['facts']):
            raise ValueError(f"Admission reason needs a sourced public fact: {car['id']}")
    return apply_batch(db_path, manifest_path, apply, expected_count=count)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db', type=Path, default=ROOT/'supercars.db')
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    import_curated(args.db, args.manifest, args.apply)
