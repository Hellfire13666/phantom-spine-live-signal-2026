#!/usr/bin/env python3
"""Read-only verification of versioned PHANTOM SPINE Live package files."""
import hashlib
import json
import pathlib
import sys

HERE=pathlib.Path(__file__).resolve().parent.parent
manifest=HERE/'MANIFEST.json'
try:
    payload=json.loads(manifest.read_text(encoding='utf-8'))
    expected=payload['files']
    if payload['version']!='0.2.0' or not isinstance(expected,dict):
        raise ValueError('Unexpected manifest version/schema')
    for name,sha in expected.items():
        f=HERE/name
        if f.is_symlink() or not f.is_file() or pathlib.PurePosixPath(name).is_absolute() or '..' in pathlib.PurePosixPath(name).parts:
            raise ValueError('Unsafe or missing file: '+name)
        if hashlib.sha256(f.read_bytes()).hexdigest()!=sha:
            raise ValueError('Checksum mismatch: '+name)
    files={p.relative_to(HERE).as_posix() for p in HERE.rglob('*') if p.is_file() and p.name!='MANIFEST.json' and '__pycache__' not in p.parts}
    if files!=set(expected):
        raise ValueError('Untracked files or missing files in release')
    print(f'[PASS] PHANTOM SPINE Live v0.2.0: {len(expected)} bundled files and SHA-256 hashes verified.')
except (OSError,KeyError,ValueError,json.JSONDecodeError) as e:
    print('[FAIL] Verification: '+str(e),file=sys.stderr)
    raise SystemExit(2)
