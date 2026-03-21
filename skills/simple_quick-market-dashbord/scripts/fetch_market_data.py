import requests
import json
from datetime import datetime, timezone, timedelta
from bs4 import BeautifulSoup

# Define UTC+8 timezone
tz_utc8 = timezone(timedelta(hours=8))

def get_now_str():
    return datetime.now(tz_utc8).strftime("%Y-%m-%d %H:%M:%S (UTC+8)")

def fetch_trading_economics_category(category):
    """Fetch data from a specific TE category page."""
    url = f"https://tradingeconomics.com/{category}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        data = {}
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 4:
                    name = cols[0].get_text(strip=True).split('\n')[0].strip()
                    price = cols[1].get_text(strip=True)
                    change = cols[2].get_text(strip=True)
                    te_time = cols[3].get_text(strip=True)
                    
                    if name and price and not price.isalpha():
                        data[name] = {
                            "price": price, 
                            "change": change,
                            "date_time": f"{te_time} (TE Local/UTC)",
                            "source": "TradingEconomics"
                        }
        return data
    except Exception as e:
        return {"error": str(e)}

def fetch_wallstreetcn():
    """Fetch live news from Wallstreetcn using the PC API."""
    url = "https://api-prod.wallstreetcn.com/apiv1/content/lives/pc?channel=global-live&limit=20"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        res_json = response.json()
        
        all_items = []
        data_sections = res_json.get("data", {})
        for section_key in data_sections:
            if isinstance(data_sections[section_key], dict):
                items = data_sections[section_key].get("items", [])
                all_items.extend(items)
        
        all_items.sort(key=lambda x: x.get("display_time", 0), reverse=True)
        
        news = []
        seen_ids = set()
        for item in all_items:
            item_id = item.get("id")
            if item_id in seen_ids: continue
            seen_ids.add(item_id)
            
            title = item.get("title") or item.get("content_text")
            if title:
                title = BeautifulSoup(title, "html.parser").get_text()
                title = title.replace('\n', ' ').strip()
                title = title[:150] + "..." if len(title) > 150 else title
                
                dt = datetime.fromtimestamp(item.get("display_time"), tz=tz_utc8)
                news.append({
                    "title": title,
                    "full_time": dt.strftime("%Y-%m-%d %H:%M:%S (UTC+8)"),
                    "uri": item.get("uri"),
                    "is_breaking": "突发" in title or item.get("score", 0) > 1,
                    "source": "Wallstreetcn (华尔街见闻)"
                })
            if len(news) >= 15: break
        return news
    except Exception as e:
        return {"error": str(e)}

def fetch_polymarket():
    """Fetch trending prediction markets from Polymarket Gamma API."""
    url = "https://gamma-api.polymarket.com/events?active=true&closed=false&order=volume24hr&limit=10"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        events = response.json()
        results = []
        for event in events:
            markets = event.get("markets", [])
            if not markets: continue
            
            price = "N/A"
            try:
                if markets[0].get("outcomePrices"):
                    prices = json.loads(markets[0]["outcomePrices"])
                    if len(prices) > 0:
                        price = f"{float(prices[0]) * 100:.1f}%"
            except:
                pass

            results.append({
                "title": event.get("title"),
                "volume": f"{float(event.get('volume24hr', 0)):,.0f}",
                "price": price,
                "url": f"https://polymarket.com/event/{event.get('slug')}",
                "fetch_time": get_now_str(),
                "source": "Polymarket"
            })
        return results
    except Exception as e:
        return {"error": str(e)}

def main():
    report = {
        "report_generated_at": get_now_str(),
        "stocks": fetch_trading_economics_category("stocks"),
        "commodities": fetch_trading_economics_category("commodities"),
        "currencies": fetch_trading_economics_category("currencies"),
        "wscn": fetch_wallstreetcn(),
        "poly": fetch_polymarket()
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
