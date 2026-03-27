import urllib.request, json, time

# Mix of real NY plate formats for training variety
plates = [
    'ABC1234', 'XYZ9999', 'JFK2026', 'NYC1234', 'TAX1234',
    'BUS1234', 'VAN1234', 'TRK1234', 'CAB1234', 'EMG1234',
    'GHI5678', 'MNO3456', 'PQR7890', 'STU2345', 'WXY6789',
    'AAA1111', 'BBB2222', 'CCC3333', 'DDD4444', 'EEE5555',
    '5GT1825'  # known clean baseline
]

results = []
for plate in plates:
    row = {'plate': plate, 'parking_violations': 0, 'camera_violations': 0, 'status': 'CLEAN'}
    try:
        url1 = f'https://data.cityofnewyork.us/resource/nc67-uf89.json?plate={plate}&\$limit=50'
        r1 = json.loads(urllib.request.urlopen(url1, timeout=10).read())
        row['parking_violations'] = len(r1)
        if r1:
            row['last_parking'] = r1[0].get('issue_date','')[:10]
    except: pass
    try:
        url2 = f'https://data.cityofnewyork.us/resource/pvqr-7yc4.json?plate_id={plate}&\$limit=50'
        r2 = json.loads(urllib.request.urlopen(url2, timeout=10).read())
        row['camera_violations'] = len(r2)
    except: pass
    if row['parking_violations'] > 0 or row['camera_violations'] > 0:
        row['status'] = 'VIOLATIONS'
    print(json.dumps(row))
    time.sleep(0.3)