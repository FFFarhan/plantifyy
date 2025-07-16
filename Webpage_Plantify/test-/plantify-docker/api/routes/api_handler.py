import pandas as pd
import requests
from flask import g

class APIHandler:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_df(self, pot_id: int, endpoint: str = "latest-today") -> pd.DataFrame:
        key = f"df_{endpoint}_{pot_id}"
        if not hasattr(g, key):
            setattr(g, key, self.get_data(endpoint, pot_id))
        return getattr(g, key)

    def get_data(self, endpoint: str, pot_id: int) -> pd.DataFrame:
        url = f"{self.base_url}/json/{endpoint}?pot_id={pot_id}"
        try:
            response = requests.get(url)
            return self.parse_response(response)
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return pd.DataFrame()

    def parse_response(self, response: requests.Response) -> pd.DataFrame:
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            if "created" in df.columns:
                df["created"] = pd.to_datetime(df["created"])
            numeric_columns = ["temperature", "soil_moisture", "air_humidity", "sunlight", "HoS"]
            for col in numeric_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors="coerce")
            return df
        else:
            print(f"API error {response.status_code}: {response.text}")
            return pd.DataFrame()
