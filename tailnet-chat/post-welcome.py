import urllib.request, json

url = 'http://localhost:8765/message'
msg = {
    'sender': 'Fiesta',
    'body': '## Hello from the agency\n\nWelcome to TailChat. You are now connected to the Dollar Agency network.\n\n- Built on ChAmpEredar infrastructure\n- Running on $39/month\n- Powered by glacial creep\n\nThe ledger is open. Say something.',
    'room': 'general'
}
req = urllib.request.Request(url, data=json.dumps(msg).encode(), headers={'Content-Type': 'application/json'})
r = urllib.request.urlopen(req, timeout=10)
print('SENT:', r.read().decode())
