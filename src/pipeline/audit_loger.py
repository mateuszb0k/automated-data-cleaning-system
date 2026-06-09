import os

def save_audit_logs(data, filename):
    path = '../data/gold'
    os.makedirs(path, exist_ok=True)
    data.to_json(os.path.join(path, filename), orient='records', indent=4)