"""Run real HTTP tests against the existing course FastAPI Agent."""
import argparse
import csv
import json
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent
FIELDS = ['test_type', 'query', 'expected_tool', 'success', 'status_code', 'tool_name', 'elapsed_ms', 'issue']


def load_config(root=ROOT):
    return json.loads((root / 'evaluation_config.json').read_text(encoding='utf-8'))


def run_test(case, config):
    row = {**{k: case[k] for k in FIELDS[:3]}, 'success': False,
           'status_code': None, 'tool_name': None, 'elapsed_ms': None, 'issue': ''}
    start = time.perf_counter()
    try:
        payload = {**config.get('extra_payload', {}), config['query_field']: case['query']}
        res = requests.post(config['base_url'].rstrip('/') + config['endpoint'],
                            json=payload, timeout=config.get('timeout', 120))
        row['status_code'] = res.status_code
        res.raise_for_status()
        data = res.json()
        if not isinstance(data, dict):
            raise ValueError('Expected JSON object')
        actual = data
        for key in config['tool_field'].split('.'):
            actual = actual.get(key) if isinstance(actual, dict) else None
        row['tool_name'] = actual
        success_field = config.get('success_field')
        if success_field and success_field not in data:
            row['issue'] = 'Missing success field: ' + success_field
        else:
            row['success'] = (not success_field or data.get(success_field) is True) and actual == case['expected_tool']
            if not row['success']:
                row['issue'] = f"Tool mismatch or API failure: expected={case['expected_tool']}, actual={actual}"
    except requests.RequestException as exc:
        row['issue'] = str(exc)
        if exc.response is not None:
            row['issue'] += ' | ' + exc.response.text[:500]
    except (ValueError, TypeError, AttributeError) as exc:
        row['issue'] = f'Invalid API response: {exc}'
    finally:
        row['elapsed_ms'] = round((time.perf_counter() - start) * 1000, 2)
    return row


def save_csv(path, rows, fields=FIELDS):
    if not rows:
        return
    with path.open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def run(stage, root=ROOT):
    config = load_config(root)
    output = root / 'results'
    output.mkdir(exist_ok=True)
    if stage == 'inspect':
        res = requests.get(config['base_url'].rstrip('/') + '/openapi.json', timeout=10)
        res.raise_for_status()
        print(json.dumps(res.json(), ensure_ascii=False, indent=2))
        return []
    if stage == 'before':
        if (output / 'before.csv').exists():
            raise SystemExit('before.csv already exists. Archive the old results before starting a new experiment.')
        cases = config['test_cases']
        if not cases:
            raise SystemExit('Set actual test cases in evaluation_config.json first.')
        rows = [run_test(case, config) for case in cases]
        save_csv(output / '05_mvp_evaluation.csv', rows)
        failed = next((row for row in rows if not row['success']), None)
        if failed:
            save_csv(output / 'before.csv', [failed])
            selection = {'case': {key: failed[key] for key in FIELDS[:3]}, 'config': {k: v for k, v in config.items() if k != 'test_cases'}}
            (output / 'selected_case.json').write_text(json.dumps(selection, ensure_ascii=False, indent=2), encoding='utf-8')
        else:
            print('No failed tests. Do not fabricate a failure; add genuine edge cases.')
        return rows
    if stage != 'after':
        raise ValueError('Unknown stage: ' + stage)
    if not (output / 'before.csv').exists() or not (output / 'selected_case.json').exists():
        raise SystemExit('No saved failed test. Run before first.')
    selection = json.loads((output / 'selected_case.json').read_text(encoding='utf-8'))
    row = run_test(selection['case'], selection['config'])
    save_csv(output / 'after.csv', [row])
    before = read_csv(output / 'before.csv')[0]
    compare = [{'stage': 'before', **before}, {'stage': 'after', **row}]
    save_csv(output / 'comparison.csv', compare, ['stage', *FIELDS])
    return compare


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage', choices=['inspect', 'before', 'after'])
    args = parser.parse_args()
    for record in run(args.stage):
        print(json.dumps(record, ensure_ascii=False))
