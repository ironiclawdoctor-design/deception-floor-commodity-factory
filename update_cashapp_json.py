#!/usr/bin/env python3
import json

path = '/root/.openclaw/workspace/secrets/cashapp.json'
with open(path) as f:
    config = json.load(f)

# Ensure required fields for cashapp skill
config['square_access_token'] = config.get('production_token', config.get('access_token'))
config['square_environment'] = 'production' if config.get('environment') == 'production' else 'sandbox'

with open(path, 'w') as f:
    json.dump(config, f, indent=2)

print("Updated cashapp.json with square_access_token and square_environment.")