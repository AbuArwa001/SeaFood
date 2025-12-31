import requests

def fetch_iso_currencies():
    """
    Fetch ISO 4217 currencies from restcountries.com
    Returns a dictionary: {code: name}
    """
    url = "https://restcountries.com/v3.1/all/?fields=currencies"
    # url = "https://restcountries.com/v3.1/all"
    response = requests.get(url)
    data = response.json()
    
    currencies = {}
    for country in data:
        if "currencies" in country:
            for code, info in country["currencies"].items():
                if code not in currencies:
                    currencies[code] = {
                        "name": info.get("name", code),
                        "symbol": info.get("symbol", "")
                    }
    return currencies
