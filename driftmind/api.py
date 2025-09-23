import requests

class DriftMindClient:
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
       

    def _headers(self):
        return {"accept": "application/json", "Auth": self.api_key}

    def create_forecaster(self, payload: dict):
        """Create a new forecaster. Returns JSON dict if available, else None."""
        url = self.base_url
        r = requests.post(
            url,
            headers={**self._headers(), "Content-Type": "application/json"},
            json=payload
        )

        if r.status_code in (200, 201):
            try:
                return r.json()
            except ValueError:
                return None  # forecaster created but no JSON body
        else:
            print("❌ Forecaster creation failed")
            print("Status:", r.status_code)
            print("Response:", r.text)
            return None

    def get_forecaster_details(self, fid: str):
        """Fetch details for a forecaster. Returns dict if available, else None."""
        url = f"{self.base_url}/forecaster/{fid}/details"
        r = requests.get(url, headers=self._headers())

        if r.status_code == 200:
            try:
                return r.json()
            except ValueError:
                print("⚠️ Forecaster details returned empty body")
                return None
        elif r.status_code == 404:
            print(f"❌ Forecaster {fid} not found")
            return None
        else:
            print("❌ Failed to fetch forecaster details")
            print("Status:", r.status_code)
            print("Response:", r.text)
            return None




    def feed_point(self, fid: str, data_point: dict) -> bool:
        """Feed a batch of data points to a forecaster. Returns True on success, else False."""
        payload = {"forecasterId": fid, "data": data_point}
        r = requests.patch(
            self.base_url,
            headers={**self._headers(), "Content-Type": "application/json"},
            json=payload
        )
        # server returns 200 on success in your working example
        if r.status_code == 200:
            return r.json()
        else:
            print("❌ Data feeding service failed")
            print("Status Code:", r.status_code)
            print("Response:", r.text)
            return False



    def feed_data(self, fid: str, data: dict) -> bool:
        return self.feed_point(fid, data)



    def forecast(self, fid: str):
        """Request a forecast from a forecaster. Returns JSON dict if available, else None."""
        url = f"{self.base_url}/forecaster/{fid}/predict"
        r = requests.get(url, headers=self._headers())

        if r.status_code == 200:
            return r.json()
        elif r.status_code == 204:
            print("⚠️ No forecast available yet")
            return None
        else:
            print("❌ Forecast request failed")
            print("Status Code:", r.status_code)
            print("Response:", r.text)
            return None

    def get_forecaster_data(self, fid: str):
        """Fetch the data currently held by a forecaster.
        Returns dict with timestamps as keys and feature values as inner dicts.
        """
        url = f"{self.base_url}/forecaster/{fid}/data"
        r = requests.get(url, headers=self._headers())

        if r.status_code == 200:
            try:
                return r.json()
            except ValueError:
                print("⚠️ Forecaster data returned empty body")
                return None
        elif r.status_code == 404:
            print(f"❌ Forecaster {fid} not found")
            return None
        else:
            print("❌ Failed to fetch forecaster data")
            print("Status:", r.status_code)
            print("Response:", r.text)
            return None
        
    

    def list_forecasters(self):
        """List all forecasters available in the system. Returns a list of dicts, one per forecaster. """
        url = f"{self.base_url}"
        r = requests.get(url, headers=self._headers())

        if r.status_code == 200:
            try:
                return r.json()
            except ValueError:
                print("⚠️ No forecasters returned in body")
                return []
        else:
            print("❌ Failed to list forecasters")
            print("Status:", r.status_code)
            print("Response:", r.text)
            return []
        

    def get_forecaster_details(self, fid: str):
        """Fetch configuration details for a specific forecaster.
        Returns a dict if available, else None.
        """
        url = f"{self.base_url}/forecaster/{fid}/details"
        r = requests.get(url, headers=self._headers())

        if r.status_code == 200:
            try:
                return r.json()
            except ValueError:
                print("⚠️ Forecaster details returned empty body")
                return None
        elif r.status_code == 404:
            print(f"❌ Forecaster {fid} not found")
            return None
        else:
            print("❌ Failed to fetch forecaster details")
            print("Status:", r.status_code)
            print("Response:", r.text)
            return None

