import sqlite3
import json

def parse_api_ans(api_ans):
    try:
        json_data = json.loads(api_ans)
        key_data = json_data.get("Keys", [])
        wps_data = json_data.get("WPS", [])
        return key_data, wps_data
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        print(f"Invalid JSON data: {api_ans}")
        return [], []

def export_to_json(database_path):
    data = []
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("SELECT SSID, BSSID, API_ANS FROM networks")
    rows = cursor.fetchall()
    for row in rows:
        key_data, wps_data = parse_api_ans(row[2])
        network_data = {
            "essid": row[0],
            "bssid": row[1] if row[1] else "<no wireless>",
            "password": ", ".join(key_data) if key_data else "-",
            "wpsCode": ", ".join(wps_data) if wps_data else "",
            "adminLogin": "pusto",
            "adminPass": "pusto"
        }
        data.append(network_data)
    conn.close()

    file_path = "output.json"

    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=2)
    print("Export to JSON completed successfully")
    print(f"Data saved to {file_path}")

if __name__ == "__main__":
    base_path = input("Specify the path to the database: ")
    export_to_json(base_path)
