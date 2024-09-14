from urllib.parse import quote_plus, quote
from bs4 import BeautifulSoup
from curl_cffi import requests
import json
import sqlite3

def save_dataframe_to_sqlite(df , name):
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(name)
    cursor = conn.cursor()

    # Save DataFrame to SQLite table
    df.to_sql(name, conn, if_exists='replace', index=False)
    
    # Commit and close the connection
    conn.commit()
    conn.close()
    


def fetch_ebay_data(keyword, shoe_size, max_price):
    query = keyword + " size " + shoe_size
    url = f"https://www.ebay.com/sch/i.html?_nkw={quote(query)}&_sop=12"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to retrieve data: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    items = []

    for item in soup.select(".s-item"):
        title_tag = item.select_one(".s-item__title")
        price_tag = item.select_one(".s-item__price")
        bid_tag = item.select_one(".s-item__bidCount")
        url_tag = item.select_one(".s-item__link")
        size_tag = item.find(string=lambda string: string and shoe_size in string)
        shipping_tag = item.select_one(".s-item__shipping, .s-item__freeXDays")
        image_tag = item.select_one("div.s-item__image-wrapper.image-treatment img")

        if title_tag and price_tag and url_tag and size_tag and image_tag:
            # Filter out ads or non-product items
            if "Shop on eBay" in title_tag.text or "Shop eBay" in title_tag.text:
                continue

            # Handle price ranges and bids
            price_text = price_tag.text.replace("$", "").replace(",", "").strip()
            if " to " in price_text:
                price_text = price_text.split(" to ")[0]
            try:
                price = float(price_text)
            except ValueError:
                continue

            if price <= max_price:
                shipping_cost = 0.0
                if shipping_tag:
                    shipping_text = (
                        shipping_tag.text.strip().replace("$", "").replace(",", "")
                    )
                    if "Free" not in shipping_text:
                        try:
                            shipping_cost = float(shipping_text.split()[0])
                        except ValueError:
                            shipping_cost = 0.0

                image_url = image_tag.get("src", "")  # Safely get the src attribute

                item_data = {
                    "Image": image_url,
                    "Shoe": title_tag.text,
                    "Price": price,
                    "Shipping": shipping_cost,
                    "Currency": "USD",
                    "Bids": bid_tag.text if bid_tag else "N/A",
                    "URL": url_tag["href"]
                }
                items.append(item_data)

    return items


def get_goat_info(shoe_name, productTemplateId, size, url, image_url):
    # Placeholder dictionary for result
    result = []

    # Make the request using curl_cffi
    cookies = {
        "__cf_bm": "SIlqQNGW30ThLpA0QEmU6JVGqjQ6fLWmjsPF8Wf4tcU-1722982299-1.0.1.1-GVx_q2jZjm3Y6d_BoP5l0PSBrNfT27GK.PjemsTyIyXXwssvYjq3D.lssWWPOmzyph5iKnSrrSvBYMfdMt.Jdw",
        "ConstructorioID_client_id": "2e49a720-0113-4221-a89d-4162f4298810",
        "ConstructorioID_session_id": "1",
        "ConstructorioID_session": '{"sessionId":1,"lastTime":1722982300052}',
        "locale": "en",
        "_gid": "GA1.2.1496568402.1722982301",
        "_csrf": "cScgOoPKI43LD3mUZeFIBAjO",
        "country": "IN",
        "currency": "USD",
        "_ga": "GA1.1.1771785265.1722982301",
        "_gcl_au": "1.1.1649408364.1722982301",
        "OptanonAlertBoxClosed": "2024-08-06T22:12:00.299Z",
        "OptanonConsent": "isIABGlobal=false&datestamp=Wed+Aug+07+2024+03%3A42%3A00+GMT%2B0530+(India+Standard+Time)&version=6.10.0&hosts=&consentId=5403f868-99a0-40cc-97c7-6ccaafbd55e7&interactionCount=1&landingPath=NotLandingPage&groups=C0003%3A1%2CC0001%3A1%2CC0002%3A1%2CC0004%3A1",
        "_scid": "d28e81fa-5339-4e2c-8851-e552da2a1e62",
        "_scid_r": "d28e81fa-5339-4e2c-8851-e552da2a1e62",
        "_ScCbts": "%5B%5D",
        "IR_gbd": "goat.com",
        "IR_12522": "1722982320768%7C0%7C1722982320768%7C%7C",
        "_ga_28GTCC4968": "GS1.1.1722982301.1.1.1722982355.0.0.0",
        "csrf": "oM9VH30D-jXzLlb1lT-Ew6KFaqftsbet4bag",
    }

    headers = {
        "accept": "application/json",
        "accept-language": "en-GB,en;q=0.9",
        "cookie": '__cf_bm=SIlqQNGW30ThLpA0QEmU6JVGqjQ6fLWmjsPF8Wf4tcU-1722982299-1.0.1.1-GVx_q2jZjm3Y6d_BoP5l0PSBrNfT27GK.PjemsTyIyXXwssvYjq3D.lssWWPOmzyph5iKnSrrSvBYMfdMt.Jdw; ConstructorioID_client_id=2e49a720-0113-4221-a89d-4162f4298810; ConstructorioID_session_id=1; ConstructorioID_session={"sessionId":1,"lastTime":1722982300052}; locale=en; _gid=GA1.2.1496568402.1722982301; _csrf=cScgOoPKI43LD3mUZeFIBAjO; country=IN; currency=USD; _ga=GA1.1.1771785265.1722982301; _gcl_au=1.1.1649408364.1722982301; OptanonAlertBoxClosed=2024-08-06T22:12:00.299Z; OptanonConsent=isIABGlobal=false&datestamp=Wed+Aug+07+2024+03%3A42%3A00+GMT%2B0530+(India+Standard+Time)&version=6.10.0&hosts=&consentId=5403f868-99a0-40cc-97c7-6ccaafbd55e7&interactionCount=1&landingPath=NotLandingPage&groups=C0003%3A1%2CC0001%3A1%2CC0002%3A1%2CC0004%3A1; _scid=d28e81fa-5339-4e2c-8851-e552da2a1e62; _scid_r=d28e81fa-5339-4e2c-8851-e552da2a1e62; _ScCbts=%5B%5D; IR_gbd=goat.com; IR_12522=1722982320768%7C0%7C1722982320768%7C%7C; _ga_28GTCC4968=GS1.1.1722982301.1.1.1722982355.0.0.0; csrf=oM9VH30D-jXzLlb1lT-Ew6KFaqftsbet4bag',
        "priority": "u=1, i",
        "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "x-csrf-token": "oM9VH30D-jXzLlb1lT-Ew6KFaqftsbet4bag",
    }

    params = {
        "productTemplateId": productTemplateId,
        "countryCode": "IN",
    }

    response = requests.get(
        "https://www.goat.com/web-api/v1/product_variants/buy_bar_data",
        params=params,
        cookies=cookies,
        headers=headers,
    )

    if response.status_code == 200:
        json_data = response.json()

        # Iterate through the JSON data
        for item in json_data:
            if float(item["sizeOption"]["presentation"]) > size:
                break
            # Check if the size and condition match
            if (
                float(item["sizeOption"]["presentation"]) == size
                and item["stockStatus"] != "not_in_stock"
            ):
                # Extract relevant information
                shoe_info = {
                    "Image": image_url,
                    "Shoe": shoe_name,
                    "Price": "$ "
                    + str(item["lowestPriceCents"]["amountUsdCents"] / 100),
                    "Shoe Condition": item["shoeCondition"].replace("_", " "),
                    "Box Condition": item["boxCondition"].replace("_", " "),
                    "URL": url,
                    "Source": "GOAT",
                }
                # Add to result dictionary
                result.append(shoe_info)

    return result


def initial_goat_scrape(query):
    headers = {
        "accept": "*/*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,hi;q=0.7",
        "origin": "https://www.goat.com",
        "priority": "u=1, i",
        "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    }

    params = {
        "c": "ciojs-client-2.35.2",
        "key": "key_XT7bjdbvjgECO5d8",
        "i": "4e67882b-cfd7-441f-a999-0c731045bfb6",
        "s": "1",
        "page": "1",
        "num_results_per_page": "24",
        "sort_by": "relevance",
        "sort_order": "descending",
        "_dt": "1722542412951",
    }

    url = f"https://ac.cnstrc.com/search/{quote_plus(query)}"
    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        print(f"Failed to retrieve data: {response.status_code}")
        return []

    try:
        data = response.json()  # Attempt to parse JSON
    except json.JSONDecodeError:
        print("Error parsing JSON response")
        print(
            "Response content:", response.text
        )  # Debugging: print the response content
        return []

    return data.get("response", {}).get("results", [])


def create_goat_list(results, size):
    shoe_data = []
    for product in results:
        name = product.get("value", "N/A")
        shoe_id = product["data"]["id"]
        image_url = product.get("data", {}).get("image_url", "N/A")
        shoe_url = "https://www.goat.com/sneakers/" + product.get("data").get("slug")
        shoe_data.extend(get_goat_info(name, shoe_id, size, shoe_url, image_url))

    return shoe_data


def get_stockx_info(shoe_name, product_id, size, url, image_url):
    cookies = {
        "stockx_device_id": "2022f346-cd49-4668-a21b-ce2ad32a295c",
        "stockx_session_id": "7f43d548-cd2f-4cb0-af31-4600826d7367",
        "stockx_session": "094af84c-6445-4eeb-9a45-566f84a0396d",
        "language_code": "en",
        "stockx_selected_region": "IN",
        "__cf_bm": "W.iZlf0D4KO_OiYcFfHFbAO_67EBkOQjwd8gcCPk62U-1723415958-1.0.1.1-hTwp6_4YWL8TTewbp5YvmnnA9eGH2NIfNCBTZKClPh1I65dMvCmfX_xEgl9c0nybTvZHSi81RtR8u7xzK1a0RQ",
        "chakra-ui-color-mode": "light",
        "is_gdpr": "false",
        "stockx_ip_region": "IN",
        "pxcts": "8c25af60-5832-11ef-9e68-2fbf68f7f773",
        "_pxvid": "8c25a59d-5832-11ef-9e65-8190730a6494",
        "cf_clearance": "1OiwVOYAdIy5iPwZE8lmpIYwNd_643myDJNDE2nuJxo-1723415960-1.0.1.1-jm5BlSmWO40jdNnQhaYlJes5qSncrJDwM9F9khUazja9YsB5h7npgh_t.twOYE9apLu22CxNohp4CupCdujaZw",
        "OptanonConsent": "isGpcEnabled=0&datestamp=Mon+Aug+12+2024+04%3A09%3A20+GMT%2B0530+(India+Standard+Time)&version=202404.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=29935e28-7183-45d9-abda-760e10d2c2c0&interactionCount=0&isAnonUser=1&landingPath=https%3A%2F%2Fstockx.com%2F&groups=C0001%3A1%2CC0002%3A1%2CC0004%3A1%2CC0005%3A1%2CC0003%3A1",
        "_px3": "2268208016b639931fc61a94ca0cf505062c02aafd5ad5b37e926686b33a06a7:WBIgcM8HnrhuuDpbdCmYSkmZMN7mUGjApKEJmq0EZLS8thjzsfUGkVS5GbiT2pjD9UK5XgmvHal4qb15CZELqg==:1000:u0h21JrR5n0aabT13t2OF4IRJRJOS0LC/x/L1KDYQuAfQ8Dw/ye9ra7ZclF1p+N8LIEaLDqBG3t0kX3SHk8zI+Akg6PmVpo13lXbaceEtiRWB8mVLNxROsyl0dTF/bIgEyWbBqrS6BKGV3yWRYCeF8GZpbtqAqaxV3EdLcj87eHcpaOxJMIpDqw6ql1KGAAv6WjabM4t806opSPCzNfXugMyZFkx3jTv1t/i2i1oqXuk7lfvOjQlSaoBsK25POeN",
        "ajs_anonymous_id": "48a9b3c6-d128-46c9-8b4c-665789e28da1",
        "_fbp": "fb.1.1723415962607.388125861695876840",
        "_gcl_au": "1.1.2131373834.1723415964",
        "rbuid": "rbos-79902881-ca4c-4c68-86fc-9c4252e5616d",
        "cto_bundle": "tj9PMl9LWnpzZU5EcTc4eXRJVjdqZll0aW5waGRFeHhkOEY1UXNtdk84YVB1NFNuc2J6QyUyRkI3dTBaUFYzMFViRWFKemhQNWlZQ3pVcFp1MlRUdlp6UGRpTzc1YmdVdDVtdU0xRWkyOXc4TDlkc2plWHdXaVJUSjdKZFhCaVRodU11S2Rx",
        "maId": '{"cid":"9892d7aeeec0d4ba65cffdb65659434a","sid":"8c9cf6d8-43ff-4902-a979-d6f18a7ae668","isSidSaved":true,"sessionStart":"2024-08-11T22:39:24.000Z"}',
        "stockx_dismiss_modal": "true",
        "stockx_dismiss_modal_set": "2024-08-11T22%3A39%3A30.039Z",
        "stockx_dismiss_modal_expiration": "2025-08-11T22%3A39%3A30.039Z",
        "display_location_selector": "false",
        "__ssid": "5d053a0d5d1f7092f14dd910e0eee55",
        "QuantumMetricSessionID": "57eb934ad2996dd1bd85c6c782c1bebc",
        "QuantumMetricUserID": "34e7bc00945b1b59d6c6c71e2e3ab324",
        "__gads": "ID=d0546857ad16a589:T=1723415970:RT=1723415970:S=ALNI_Mbz4qGQsgeqqX5fonFEsEykO9VN1w",
        "__gpi": "UID=00000ec9a59fc15c:T=1723415970:RT=1723415970:S=ALNI_MYJkqcHHzugXcqrI58mM4TU7jV9Vw",
        "__eoi": "ID=053a68b58bfb260f:T=1723415970:RT=1723415970:S=AA-AfjbA6FOT84dZFfIpMtff8juo",
        "lastRskxRun": "1723415971021",
        "rskxRunCookie": "0",
        "rCookie": "tpx6z04joghfro6xgwwwz6lzq5ddxv",
        "_ga_TYYSNQDG4W": "GS1.1.1723415998.1.0.1723415998.0.0.0",
        "_ga": "GA1.1.648523887.1723415998",
        "_pxde": "a511519b4d7aaae67c7611a8f95c8ddb404371212f405a3be54615a88100a541:eyJ0aW1lc3RhbXAiOjE3MjM0MTU5OTc2NzUsImZfa2IiOjB9",
        "_tq_id.TV-5490813681-1.1a3e": "b4a946ad4a96330f.1723415965.0.1723415999..",
        "_dd_s": "rum=0&expire=1723416925059&logs=1&id=f3261efe-8703-4166-9a82-9188cee69b24&created=1723415960026",
        "_uetsid": "8ddff1d0583211efa66ed13c90a6a52c|1cajeoo|2|fo8|0|1684",
        "_uetvid": "8de01460583211efaed717fa4ac394e1|t079wt|1723415997814|2|1|bat.bing.com/p/insights/c/q",
    }

    headers = {
        "accept": "application/json",
        "accept-language": "en-US",
        "apollographql-client-name": "Iron",
        "apollographql-client-version": "2024.08.04.00",
        "app-platform": "Iron",
        "app-version": "2024.08.04.00",
        "content-type": "application/json",
        # 'cookie': 'stockx_device_id=2022f346-cd49-4668-a21b-ce2ad32a295c; stockx_session_id=7f43d548-cd2f-4cb0-af31-4600826d7367; stockx_session=094af84c-6445-4eeb-9a45-566f84a0396d; language_code=en; stockx_selected_region=IN; __cf_bm=W.iZlf0D4KO_OiYcFfHFbAO_67EBkOQjwd8gcCPk62U-1723415958-1.0.1.1-hTwp6_4YWL8TTewbp5YvmnnA9eGH2NIfNCBTZKClPh1I65dMvCmfX_xEgl9c0nybTvZHSi81RtR8u7xzK1a0RQ; chakra-ui-color-mode=light; is_gdpr=false; stockx_ip_region=IN; pxcts=8c25af60-5832-11ef-9e68-2fbf68f7f773; _pxvid=8c25a59d-5832-11ef-9e65-8190730a6494; cf_clearance=1OiwVOYAdIy5iPwZE8lmpIYwNd_643myDJNDE2nuJxo-1723415960-1.0.1.1-jm5BlSmWO40jdNnQhaYlJes5qSncrJDwM9F9khUazja9YsB5h7npgh_t.twOYE9apLu22CxNohp4CupCdujaZw; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Aug+12+2024+04%3A09%3A20+GMT%2B0530+(India+Standard+Time)&version=202404.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=29935e28-7183-45d9-abda-760e10d2c2c0&interactionCount=0&isAnonUser=1&landingPath=https%3A%2F%2Fstockx.com%2F&groups=C0001%3A1%2CC0002%3A1%2CC0004%3A1%2CC0005%3A1%2CC0003%3A1; _px3=2268208016b639931fc61a94ca0cf505062c02aafd5ad5b37e926686b33a06a7:WBIgcM8HnrhuuDpbdCmYSkmZMN7mUGjApKEJmq0EZLS8thjzsfUGkVS5GbiT2pjD9UK5XgmvHal4qb15CZELqg==:1000:u0h21JrR5n0aabT13t2OF4IRJRJOS0LC/x/L1KDYQuAfQ8Dw/ye9ra7ZclF1p+N8LIEaLDqBG3t0kX3SHk8zI+Akg6PmVpo13lXbaceEtiRWB8mVLNxROsyl0dTF/bIgEyWbBqrS6BKGV3yWRYCeF8GZpbtqAqaxV3EdLcj87eHcpaOxJMIpDqw6ql1KGAAv6WjabM4t806opSPCzNfXugMyZFkx3jTv1t/i2i1oqXuk7lfvOjQlSaoBsK25POeN; ajs_anonymous_id=48a9b3c6-d128-46c9-8b4c-665789e28da1; _fbp=fb.1.1723415962607.388125861695876840; _gcl_au=1.1.2131373834.1723415964; rbuid=rbos-79902881-ca4c-4c68-86fc-9c4252e5616d; cto_bundle=tj9PMl9LWnpzZU5EcTc4eXRJVjdqZll0aW5waGRFeHhkOEY1UXNtdk84YVB1NFNuc2J6QyUyRkI3dTBaUFYzMFViRWFKemhQNWlZQ3pVcFp1MlRUdlp6UGRpTzc1YmdVdDVtdU0xRWkyOXc4TDlkc2plWHdXaVJUSjdKZFhCaVRodU11S2Rx; maId={"cid":"9892d7aeeec0d4ba65cffdb65659434a","sid":"8c9cf6d8-43ff-4902-a979-d6f18a7ae668","isSidSaved":true,"sessionStart":"2024-08-11T22:39:24.000Z"}; stockx_dismiss_modal=true; stockx_dismiss_modal_set=2024-08-11T22%3A39%3A30.039Z; stockx_dismiss_modal_expiration=2025-08-11T22%3A39%3A30.039Z; display_location_selector=false; __ssid=5d053a0d5d1f7092f14dd910e0eee55; QuantumMetricSessionID=57eb934ad2996dd1bd85c6c782c1bebc; QuantumMetricUserID=34e7bc00945b1b59d6c6c71e2e3ab324; __gads=ID=d0546857ad16a589:T=1723415970:RT=1723415970:S=ALNI_Mbz4qGQsgeqqX5fonFEsEykO9VN1w; __gpi=UID=00000ec9a59fc15c:T=1723415970:RT=1723415970:S=ALNI_MYJkqcHHzugXcqrI58mM4TU7jV9Vw; __eoi=ID=053a68b58bfb260f:T=1723415970:RT=1723415970:S=AA-AfjbA6FOT84dZFfIpMtff8juo; lastRskxRun=1723415971021; rskxRunCookie=0; rCookie=tpx6z04joghfro6xgwwwz6lzq5ddxv; _ga_TYYSNQDG4W=GS1.1.1723415998.1.0.1723415998.0.0.0; _ga=GA1.1.648523887.1723415998; _pxde=a511519b4d7aaae67c7611a8f95c8ddb404371212f405a3be54615a88100a541:eyJ0aW1lc3RhbXAiOjE3MjM0MTU5OTc2NzUsImZfa2IiOjB9; _tq_id.TV-5490813681-1.1a3e=b4a946ad4a96330f.1723415965.0.1723415999..; _dd_s=rum=0&expire=1723416925059&logs=1&id=f3261efe-8703-4166-9a82-9188cee69b24&created=1723415960026; _uetsid=8ddff1d0583211efa66ed13c90a6a52c|1cajeoo|2|fo8|0|1684; _uetvid=8de01460583211efaed717fa4ac394e1|t079wt|1723415997814|2|1|bat.bing.com/p/insights/c/q',
        "origin": "https://stockx.com",
        "priority": "u=1, i",
        "referer": "https://stockx.com/nike-air-max-95-triple-black-2020",
        "sec-ch-prefers-color-scheme": "light",
        "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "selected-country": "IN",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "x-operation-name": "GetProduct",
        "x-stockx-device-id": "2022f346-cd49-4668-a21b-ce2ad32a295c",
        "x-stockx-session-id": "7f43d548-cd2f-4cb0-af31-4600826d7367",
    }

    json_data = {
        "query": "query GetProduct($id: String!, $currencyCode: CurrencyCode, $countryCode: String!, $marketName: String, $skipMerchandising: Boolean!, $skipBreadcrumbs: Boolean!, $skipResellNoFee: Boolean!, $verticalImageTestEnabled: Boolean!) {\n  product(id: $id) {\n    id\n    listingType\n    deleted\n    gender\n    browseVerticals\n    ...ProductMerchandisingFragment\n    ...BreadcrumbsFragment\n    ...BreadcrumbSchemaFragment\n    ...HazmatWarningFragment\n    ...HeaderFragment\n    ...NFTHeaderFragment\n    ...MarketActivityFragment\n    ...MediaFragment\n    ...MyPositionFragment\n    ...ProductDetailsFragment\n    ...ProductMetaTagsFragment\n    ...ProductSchemaFragment\n    ...ScreenTrackerFragment\n    ...SizeSelectorWrapperFragment\n    ...StatsForNerdsFragment\n    ...ThreeSixtyImageFragment\n    ...TrackingFragment\n    ...UtilityGroupFragment\n    ...FavoriteProductFragment\n    ...ResellNoFeeFragment\n  }\n}\n\nfragment ProductMerchandisingFragment on Product {\n  id\n  merchandising @skip(if: $skipMerchandising) {\n    title\n    subtitle\n    image {\n      alt\n      url\n    }\n    body\n    trackingEvent\n    link {\n      title\n      url\n      urlType\n    }\n  }\n}\n\nfragment BreadcrumbsFragment on Product {\n  breadcrumbs @skip(if: $skipBreadcrumbs) {\n    name\n    url\n    level\n  }\n  brands {\n    default {\n      alias\n      name\n    }\n  }\n  categories {\n    default {\n      alias\n      value\n      level\n    }\n  }\n}\n\nfragment BreadcrumbSchemaFragment on Product {\n  breadcrumbs @skip(if: $skipBreadcrumbs) {\n    name\n    url\n  }\n  brands {\n    default {\n      alias\n      name\n    }\n  }\n  categories {\n    default {\n      alias\n      value\n      level\n    }\n  }\n}\n\nfragment HazmatWarningFragment on Product {\n  id\n  hazardousMaterial {\n    lithiumIonBucket\n  }\n}\n\nfragment HeaderFragment on Product {\n  primaryTitle\n  secondaryTitle\n  condition\n  productCategory\n}\n\nfragment NFTHeaderFragment on Product {\n  primaryTitle\n  secondaryTitle\n  productCategory\n  editionType\n}\n\nfragment MarketActivityFragment on Product {\n  id\n  title\n  productCategory\n  primaryTitle\n  secondaryTitle\n  media {\n    smallImageUrl\n  }\n}\n\nfragment MediaFragment on Product {\n  id\n  productCategory\n  title\n  brand\n  urlKey\n  variants {\n    id\n    hidden\n    traits {\n      size\n    }\n  }\n  media {\n    gallery\n    imageUrl\n    videos {\n      video {\n        url\n        alt\n      }\n      thumbnail {\n        url\n        alt\n      }\n    }\n    verticalImages @include(if: $verticalImageTestEnabled)\n  }\n}\n\nfragment MyPositionFragment on Product {\n  id\n  urlKey\n}\n\nfragment ProductDetailsFragment on Product {\n  id\n  title\n  productCategory\n  contentGroup\n  browseVerticals\n  description\n  gender\n  traits {\n    name\n    value\n    visible\n    format\n  }\n}\n\nfragment ProductMetaTagsFragment on Product {\n  id\n  urlKey\n  productCategory\n  brand\n  model\n  title\n  description\n  condition\n  styleId\n  breadcrumbs @skip(if: $skipBreadcrumbs) {\n    name\n    url\n  }\n  traits {\n    name\n    value\n  }\n  media {\n    thumbUrl\n    imageUrl\n  }\n  market(currencyCode: $currencyCode) {\n    state(country: $countryCode, market: $marketName) {\n      lowestAsk {\n        amount\n      }\n      numberOfAsks\n    }\n  }\n  variants {\n    id\n    hidden\n    traits {\n      size\n    }\n    market(currencyCode: $currencyCode) {\n      state(country: $countryCode, market: $marketName) {\n        lowestAsk {\n          amount\n        }\n      }\n    }\n  }\n  seo {\n    meta {\n      name\n      value\n    }\n  }\n}\n\nfragment ProductSchemaFragment on Product {\n  id\n  urlKey\n  productCategory\n  brand\n  model\n  title\n  description\n  condition\n  styleId\n  traits {\n    name\n    value\n  }\n  media {\n    thumbUrl\n    imageUrl\n  }\n  market(currencyCode: $currencyCode) {\n    state(country: $countryCode, market: $marketName) {\n      lowestAsk {\n        amount\n      }\n      numberOfAsks\n    }\n  }\n  variants {\n    id\n    hidden\n    traits {\n      size\n    }\n    market(currencyCode: $currencyCode) {\n      state(country: $countryCode, market: $marketName) {\n        lowestAsk {\n          amount\n        }\n      }\n    }\n    gtins {\n      type\n      identifier\n    }\n  }\n}\n\nfragment ScreenTrackerFragment on Product {\n  id\n  brand\n  productCategory\n  primaryCategory\n  title\n  market(currencyCode: $currencyCode) {\n    state(country: $countryCode, market: $marketName) {\n      highestBid {\n        amount\n      }\n      lowestAsk {\n        amount\n      }\n      numberOfAsks\n      numberOfBids\n    }\n    salesInformation {\n      lastSale\n    }\n  }\n  media {\n    imageUrl\n  }\n  traits {\n    name\n    value\n  }\n  variants {\n    id\n    traits {\n      size\n    }\n    market(currencyCode: $currencyCode) {\n      state(country: $countryCode, market: $marketName) {\n        highestBid {\n          amount\n        }\n        lowestAsk {\n          amount\n        }\n        numberOfAsks\n        numberOfBids\n      }\n      salesInformation {\n        lastSale\n      }\n    }\n  }\n  tags\n}\n\nfragment SizeSelectorWrapperFragment on Product {\n  id\n  ...SizeSelectorFragment\n  ...SizeSelectorHeaderFragment\n  ...SizesFragment\n  ...SizesOptionsFragment\n  ...SizeChartFragment\n  ...SizeChartContentFragment\n  ...SizeConversionFragment\n  ...SizesAllButtonFragment\n}\n\nfragment SizeSelectorFragment on Product {\n  id\n  title\n  productCategory\n  browseVerticals\n  sizeDescriptor\n  availableSizeConversions {\n    name\n    type\n  }\n  defaultSizeConversion {\n    name\n    type\n  }\n  variants {\n    id\n    hidden\n    traits {\n      size\n    }\n    sizeChart {\n      baseSize\n      baseType\n      displayOptions {\n        size\n        type\n      }\n    }\n  }\n}\n\nfragment SizeSelectorHeaderFragment on Product {\n  sizeDescriptor\n  productCategory\n  availableSizeConversions {\n    name\n    type\n  }\n}\n\nfragment SizesFragment on Product {\n  id\n  productCategory\n  listingType\n  title\n}\n\nfragment SizesOptionsFragment on Product {\n  id\n  listingType\n  variants {\n    id\n    hidden\n    group {\n      shortCode\n    }\n    traits {\n      size\n    }\n    sizeChart {\n      baseSize\n      baseType\n      displayOptions {\n        size\n        type\n      }\n    }\n    market(currencyCode: $currencyCode) {\n      state(country: $countryCode, market: $marketName) {\n        askServiceLevels {\n          expressExpedited {\n            count\n            lowest {\n              amount\n            }\n          }\n          expressStandard {\n            count\n            lowest {\n              amount\n            }\n          }\n        }\n        lowestAsk {\n          amount\n        }\n      }\n    }\n  }\n}\n\nfragment SizeChartFragment on Product {\n  availableSizeConversions {\n    name\n    type\n  }\n  defaultSizeConversion {\n    name\n    type\n  }\n}\n\nfragment SizeChartContentFragment on Product {\n  availableSizeConversions {\n    name\n    type\n  }\n  defaultSizeConversion {\n    name\n    type\n  }\n  variants {\n    id\n    sizeChart {\n      baseSize\n      baseType\n      displayOptions {\n        size\n        type\n      }\n    }\n  }\n}\n\nfragment SizeConversionFragment on Product {\n  productCategory\n  browseVerticals\n  sizeDescriptor\n  availableSizeConversions {\n    name\n    type\n  }\n  defaultSizeConversion {\n    name\n    type\n  }\n}\n\nfragment SizesAllButtonFragment on Product {\n  id\n  sizeAllDescriptor\n  market(currencyCode: $currencyCode) {\n    state(country: $countryCode, market: $marketName) {\n      lowestAsk {\n        amount\n      }\n      askServiceLevels {\n        expressExpedited {\n          count\n          lowest {\n            amount\n          }\n        }\n        expressStandard {\n          count\n          lowest {\n            amount\n          }\n        }\n      }\n    }\n  }\n}\n\nfragment StatsForNerdsFragment on Product {\n  id\n  title\n  productCategory\n  sizeDescriptor\n  urlKey\n}\n\nfragment ThreeSixtyImageFragment on Product {\n  id\n  title\n  variants {\n    id\n  }\n  productCategory\n  media {\n    all360Images\n  }\n}\n\nfragment TrackingFragment on Product {\n  id\n  productCategory\n  primaryCategory\n  brand\n  title\n  market(currencyCode: $currencyCode) {\n    state(country: $countryCode, market: $marketName) {\n      highestBid {\n        amount\n      }\n      lowestAsk {\n        amount\n      }\n    }\n  }\n  variants {\n    id\n    market(currencyCode: $currencyCode) {\n      state(country: $countryCode, market: $marketName) {\n        highestBid {\n          amount\n        }\n        lowestAsk {\n          amount\n        }\n      }\n    }\n  }\n}\n\nfragment UtilityGroupFragment on Product {\n  id\n  ...PortfolioFragment\n  ...PortfolioContentFragment\n  ...ShareFragment\n}\n\nfragment PortfolioFragment on Product {\n  id\n  title\n  productCategory\n  variants {\n    id\n  }\n  traits {\n    name\n    value\n  }\n}\n\nfragment PortfolioContentFragment on Product {\n  id\n  productCategory\n  sizeDescriptor\n  variants {\n    id\n    traits {\n      size\n    }\n  }\n}\n\nfragment ShareFragment on Product {\n  id\n  productCategory\n  title\n  media {\n    imageUrl\n  }\n}\n\nfragment FavoriteProductFragment on Product {\n  favorite\n}\n\nfragment ResellNoFeeFragment on Product {\n  resellNoFee @skip(if: $skipResellNoFee) {\n    enabled\n    eligibilityDays\n  }\n}",
        "variables": {
            "id": product_id,
            "currencyCode": "USD",
            "countryCode": "IN",
            "marketName": "IN",
            "skipMerchandising": False,
            "skipBreadcrumbs": False,
            "skipResellNoFee": False,
            "verticalImageTestEnabled": False,
        },
        "operationName": "GetProduct",
    }

    response = requests.post(
        "https://stockx.com/api/p/e", cookies=cookies, headers=headers, json=json_data
    )

    result = []

    if response.status_code == 200:
        json_data = response.json()

        size = str(size)

        # Iterate through the JSON data
        for item in json_data["data"]["product"]["variants"]:
            # Check if the size matches
            if item["traits"]["size"] == size:
                # Extract relevant information
                shoe_info = {
                    "Image": image_url,
                    "Shoe": shoe_name,
                    "Buy Now Price": "$ "
                    + str(item["market"]["state"]["lowestAsk"]["amount"]),
                    "Highest Bid": "$ "
                    + str(item["market"]["state"]["highestBid"]["amount"]),
                    "No. of Bids": str(item["market"]["state"]["numberOfBids"]),
                    "Last Sale": "$ "
                    + str(item["market"]["salesInformation"]["lastSale"]),
                    "URL": url,
                    "Source": "StockX",
                }
                # Add to result dictionary
                result.append(shoe_info)

    return result


def initial_stockx_scrape(query):
    cookies = {
        "stockx_device_id": "2022f346-cd49-4668-a21b-ce2ad32a295c",
        "stockx_session_id": "7f43d548-cd2f-4cb0-af31-4600826d7367",
        "stockx_session": "094af84c-6445-4eeb-9a45-566f84a0396d",
        "language_code": "en",
        "stockx_selected_region": "IN",
        "__cf_bm": "W.iZlf0D4KO_OiYcFfHFbAO_67EBkOQjwd8gcCPk62U-1723415958-1.0.1.1-hTwp6_4YWL8TTewbp5YvmnnA9eGH2NIfNCBTZKClPh1I65dMvCmfX_xEgl9c0nybTvZHSi81RtR8u7xzK1a0RQ",
        "chakra-ui-color-mode": "light",
        "is_gdpr": "false",
        "stockx_ip_region": "IN",
        "pxcts": "8c25af60-5832-11ef-9e68-2fbf68f7f773",
        "_pxvid": "8c25a59d-5832-11ef-9e65-8190730a6494",
        "cf_clearance": "1OiwVOYAdIy5iPwZE8lmpIYwNd_643myDJNDE2nuJxo-1723415960-1.0.1.1-jm5BlSmWO40jdNnQhaYlJes5qSncrJDwM9F9khUazja9YsB5h7npgh_t.twOYE9apLu22CxNohp4CupCdujaZw",
        "OptanonConsent": "isGpcEnabled=0&datestamp=Mon+Aug+12+2024+04%3A09%3A20+GMT%2B0530+(India+Standard+Time)&version=202404.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=29935e28-7183-45d9-abda-760e10d2c2c0&interactionCount=0&isAnonUser=1&landingPath=https%3A%2F%2Fstockx.com%2F&groups=C0001%3A1%2CC0002%3A1%2CC0004%3A1%2CC0005%3A1%2CC0003%3A1",
        "_px3": "2268208016b639931fc61a94ca0cf505062c02aafd5ad5b37e926686b33a06a7:WBIgcM8HnrhuuDpbdCmYSkmZMN7mUGjApKEJmq0EZLS8thjzsfUGkVS5GbiT2pjD9UK5XgmvHal4qb15CZELqg==:1000:u0h21JrR5n0aabT13t2OF4IRJRJOS0LC/x/L1KDYQuAfQ8Dw/ye9ra7ZclF1p+N8LIEaLDqBG3t0kX3SHk8zI+Akg6PmVpo13lXbaceEtiRWB8mVLNxROsyl0dTF/bIgEyWbBqrS6BKGV3yWRYCeF8GZpbtqAqaxV3EdLcj87eHcpaOxJMIpDqw6ql1KGAAv6WjabM4t806opSPCzNfXugMyZFkx3jTv1t/i2i1oqXuk7lfvOjQlSaoBsK25POeN",
        "ajs_anonymous_id": "48a9b3c6-d128-46c9-8b4c-665789e28da1",
        "_fbp": "fb.1.1723415962607.388125861695876840",
        "_gcl_au": "1.1.2131373834.1723415964",
        "rbuid": "rbos-79902881-ca4c-4c68-86fc-9c4252e5616d",
        "cto_bundle": "tj9PMl9LWnpzZU5EcTc4eXRJVjdqZll0aW5waGRFeHhkOEY1UXNtdk84YVB1NFNuc2J6QyUyRkI3dTBaUFYzMFViRWFKemhQNWlZQ3pVcFp1MlRUdlp6UGRpTzc1YmdVdDVtdU0xRWkyOXc4TDlkc2plWHdXaVJUSjdKZFhCaVRodU11S2Rx",
        "maId": '{"cid":"9892d7aeeec0d4ba65cffdb65659434a","sid":"8c9cf6d8-43ff-4902-a979-d6f18a7ae668","isSidSaved":true,"sessionStart":"2024-08-11T22:39:24.000Z"}',
        "stockx_dismiss_modal": "true",
        "stockx_dismiss_modal_set": "2024-08-11T22%3A39%3A30.039Z",
        "stockx_dismiss_modal_expiration": "2025-08-11T22%3A39%3A30.039Z",
        "display_location_selector": "false",
        "__ssid": "5d053a0d5d1f7092f14dd910e0eee55",
        "QuantumMetricSessionID": "57eb934ad2996dd1bd85c6c782c1bebc",
        "QuantumMetricUserID": "34e7bc00945b1b59d6c6c71e2e3ab324",
        "__gads": "ID=d0546857ad16a589:T=1723415970:RT=1723415970:S=ALNI_Mbz4qGQsgeqqX5fonFEsEykO9VN1w",
        "__gpi": "UID=00000ec9a59fc15c:T=1723415970:RT=1723415970:S=ALNI_MYJkqcHHzugXcqrI58mM4TU7jV9Vw",
        "__eoi": "ID=053a68b58bfb260f:T=1723415970:RT=1723415970:S=AA-AfjbA6FOT84dZFfIpMtff8juo",
        "lastRskxRun": "1723415971021",
        "rskxRunCookie": "0",
        "rCookie": "tpx6z04joghfro6xgwwwz6lzq5ddxv",
        "_uetsid": "8ddff1d0583211efa66ed13c90a6a52c|1cajeoo|2|fo8|0|1684",
        "_uetvid": "8de01460583211efaed717fa4ac394e1|t079wt|1723415964408|1|1|bat.bing.com/p/insights/c/q",
        "_pxde": "f9b729bd5cc75ae69f8e9ac992ea1557ba6c02613fbc65291e09b6607857c9db:eyJ0aW1lc3RhbXAiOjE3MjM0MTU5ODU1ODEsImZfa2IiOjB9",
        "_tq_id.TV-5490813681-1.1a3e": "b4a946ad4a96330f.1723415965.0.1723415990..",
        "_dd_s": "rum=0&expire=1723416889435&logs=1&id=f3261efe-8703-4166-9a82-9188cee69b24&created=1723415960026",
    }

    headers = {
        "accept": "application/json",
        "accept-language": "en-US",
        "apollographql-client-name": "Iron",
        "apollographql-client-version": "2024.08.04.00",
        "app-platform": "Iron",
        "app-version": "2024.08.04.00",
        "content-type": "application/json",
        # 'cookie': 'stockx_device_id=2022f346-cd49-4668-a21b-ce2ad32a295c; stockx_session_id=7f43d548-cd2f-4cb0-af31-4600826d7367; stockx_session=094af84c-6445-4eeb-9a45-566f84a0396d; language_code=en; stockx_selected_region=IN; __cf_bm=W.iZlf0D4KO_OiYcFfHFbAO_67EBkOQjwd8gcCPk62U-1723415958-1.0.1.1-hTwp6_4YWL8TTewbp5YvmnnA9eGH2NIfNCBTZKClPh1I65dMvCmfX_xEgl9c0nybTvZHSi81RtR8u7xzK1a0RQ; chakra-ui-color-mode=light; is_gdpr=false; stockx_ip_region=IN; pxcts=8c25af60-5832-11ef-9e68-2fbf68f7f773; _pxvid=8c25a59d-5832-11ef-9e65-8190730a6494; cf_clearance=1OiwVOYAdIy5iPwZE8lmpIYwNd_643myDJNDE2nuJxo-1723415960-1.0.1.1-jm5BlSmWO40jdNnQhaYlJes5qSncrJDwM9F9khUazja9YsB5h7npgh_t.twOYE9apLu22CxNohp4CupCdujaZw; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Aug+12+2024+04%3A09%3A20+GMT%2B0530+(India+Standard+Time)&version=202404.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=29935e28-7183-45d9-abda-760e10d2c2c0&interactionCount=0&isAnonUser=1&landingPath=https%3A%2F%2Fstockx.com%2F&groups=C0001%3A1%2CC0002%3A1%2CC0004%3A1%2CC0005%3A1%2CC0003%3A1; _px3=2268208016b639931fc61a94ca0cf505062c02aafd5ad5b37e926686b33a06a7:WBIgcM8HnrhuuDpbdCmYSkmZMN7mUGjApKEJmq0EZLS8thjzsfUGkVS5GbiT2pjD9UK5XgmvHal4qb15CZELqg==:1000:u0h21JrR5n0aabT13t2OF4IRJRJOS0LC/x/L1KDYQuAfQ8Dw/ye9ra7ZclF1p+N8LIEaLDqBG3t0kX3SHk8zI+Akg6PmVpo13lXbaceEtiRWB8mVLNxROsyl0dTF/bIgEyWbBqrS6BKGV3yWRYCeF8GZpbtqAqaxV3EdLcj87eHcpaOxJMIpDqw6ql1KGAAv6WjabM4t806opSPCzNfXugMyZFkx3jTv1t/i2i1oqXuk7lfvOjQlSaoBsK25POeN; ajs_anonymous_id=48a9b3c6-d128-46c9-8b4c-665789e28da1; _fbp=fb.1.1723415962607.388125861695876840; _gcl_au=1.1.2131373834.1723415964; rbuid=rbos-79902881-ca4c-4c68-86fc-9c4252e5616d; cto_bundle=tj9PMl9LWnpzZU5EcTc4eXRJVjdqZll0aW5waGRFeHhkOEY1UXNtdk84YVB1NFNuc2J6QyUyRkI3dTBaUFYzMFViRWFKemhQNWlZQ3pVcFp1MlRUdlp6UGRpTzc1YmdVdDVtdU0xRWkyOXc4TDlkc2plWHdXaVJUSjdKZFhCaVRodU11S2Rx; maId={"cid":"9892d7aeeec0d4ba65cffdb65659434a","sid":"8c9cf6d8-43ff-4902-a979-d6f18a7ae668","isSidSaved":true,"sessionStart":"2024-08-11T22:39:24.000Z"}; stockx_dismiss_modal=true; stockx_dismiss_modal_set=2024-08-11T22%3A39%3A30.039Z; stockx_dismiss_modal_expiration=2025-08-11T22%3A39%3A30.039Z; display_location_selector=false; __ssid=5d053a0d5d1f7092f14dd910e0eee55; QuantumMetricSessionID=57eb934ad2996dd1bd85c6c782c1bebc; QuantumMetricUserID=34e7bc00945b1b59d6c6c71e2e3ab324; __gads=ID=d0546857ad16a589:T=1723415970:RT=1723415970:S=ALNI_Mbz4qGQsgeqqX5fonFEsEykO9VN1w; __gpi=UID=00000ec9a59fc15c:T=1723415970:RT=1723415970:S=ALNI_MYJkqcHHzugXcqrI58mM4TU7jV9Vw; __eoi=ID=053a68b58bfb260f:T=1723415970:RT=1723415970:S=AA-AfjbA6FOT84dZFfIpMtff8juo; lastRskxRun=1723415971021; rskxRunCookie=0; rCookie=tpx6z04joghfro6xgwwwz6lzq5ddxv; _uetsid=8ddff1d0583211efa66ed13c90a6a52c|1cajeoo|2|fo8|0|1684; _uetvid=8de01460583211efaed717fa4ac394e1|t079wt|1723415964408|1|1|bat.bing.com/p/insights/c/q; _pxde=f9b729bd5cc75ae69f8e9ac992ea1557ba6c02613fbc65291e09b6607857c9db:eyJ0aW1lc3RhbXAiOjE3MjM0MTU5ODU1ODEsImZfa2IiOjB9; _tq_id.TV-5490813681-1.1a3e=b4a946ad4a96330f.1723415965.0.1723415990..; _dd_s=rum=0&expire=1723416889435&logs=1&id=f3261efe-8703-4166-9a82-9188cee69b24&created=1723415960026',
        "origin": "https://stockx.com",
        "priority": "u=1, i",
        "referer": "https://stockx.com/",
        "sec-ch-prefers-color-scheme": "light",
        "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "selected-country": "IN",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "x-abtest-ids": "ab_0614202401_web.false,ab_0614202401usonly_web.neither,ab_0614202402_web.false,ab_0614202402usonly_web.neither,ab_0614202403_web.true,ab_0614202403usonly_web.neither,ab_0614202404_web.true,ab_0614202405_web.false,ab_0614202406_web.false,ab_0614202407_web.true,ab_0614202408_web.false,ab_0614202409_web.true,ab_0614202410_web.true,ab_0617202401_web.true,ab_0617202401usonly_web.neither,ab_0617202402_web.true,ab_0617202402usonly_web.neither,ab_0617202403_web.false,ab_0617202403usonly_web.neither,ab_0617202404_web.false,ab_0617202404usonly_web.neither,ab_0617202405_web.false,ab_0617202405usonly_web.neither,ab_0617202406_web.false,ab_0617202406usonly_web.neither,ab_0617202407_web.true,ab_0617202407usonly_web.neither,ab_0617202408_web.false,ab_0617202408usonly_web.neither,ab_0617202409_web.true,ab_0617202409usonly_web.neither,ab_0617202410_web.false,ab_0617202410usonly_web.neither,ab_0617202411_web.true,ab_0617202412_web.true,ab_0617202413_web.false,ab_0617202414_web.true,ab_0617202415_web.true,ab_0617202416_web.true,ab_0617202417_web.true,ab_0617202418_web.true,ab_0617202419_web.true,ab_0617202420_web.true,ab_0wvmo_web.true,ab_0xdjj_web.true,ab_12dul_all.neither,ab_18ojl_web.false,ab_1li7n_web.false,ab_2ki60_web.neither,ab_2lofw_web.true,ab_3opqo_web.true,ab_5wzq0_web.true,ab_629pr_web.neither,ab_6tgb6_web.true,ab_77or7_web.neither,ab_82d7l_web.neither1,ab_872np_web.false,ab_8ht34_web.true,ab_8ihn8_web.neither,ab_8stea_web.neither,ab_8x8am_web.true,ab_8zx87_web.true,ab_9l1lr_web.false,ab_9v8xl_web.variant,ab_9zi8a_web.true,ab_aa_continuous_all.web_a,ab_account_selling_guidance_web.variant,ab_alp05_web.true,ab_aoxjj_web.true,ab_ayu9e_web.true,ab_bhy9z_web.true,ab_cb78y_web.false,ab_cf8ly_web.true,ab_checkout_buying_table_redesign_web.variant,ab_checkout_cutoff_date_web.variant,ab_chk_place_order_verbage_web.true,ab_cs_seller_shipping_extension_web.variant,ab_discovery_color_filter_all.false,ab_drc_chk_sell_intra_zone_all_in_support_web.variant,ab_efoch_web.true,ab_ekirh_web.variant_2,ab_enable_3_CTAs_web.variant,ab_epnox_web.false,ab_eu3zm_web.neither,ab_gift_cards_v1_web.true,ab_growth_appsflyer_smart_banner_web.variant_2,ab_growth_ignore_rv_products_in_rfy_v2_web.true,ab_hd56r_web.neither,ab_hex3z_web.true,ab_hl2ow_web.false,ab_home_as_seen_on_instagram_v2_web.true,ab_home_carousel_current_asks_bids_web.true,ab_home_page_reordering_web.variant_1,ab_home_show_value_props_web.variant_2,ab_hpjqx_web.neither,ab_hsaxr_web.true,ab_ht7f1_web.false,ab_hzpar_all.neither,ab_k3z78_web.true,ab_k4o72_web.neither,ab_kq8eh_web.true,ab_kvcr0_web.true,ab_ljut9_web.true,ab_merchandising_module_pdp_v2_web.variant,ab_mh0wn_web.neither,ab_myaccount_reorg_web.true,ab_n0kpl_web.neither,ab_n87do_web.neither,ab_ngow7_web.false,ab_o95do_web.neither,ab_oybmw_web.true,ab_p57ks_web.false,ab_p814c_web.neither,ab_pirate_most_popular_around_you_module_web.neither,ab_pirate_product_cell_favorite_web_v1.true,ab_q2nhm_web.true,ab_qxy5c_web.false,ab_r84zi_web.variant,ab_sa2jv_web.1,ab_search_static_ranking_v5_web.variant,ab_swh17_web.true,ab_sx1wr_web.neither,ab_tb6az_web.neither,ab_td4g7_web.neither,ab_u13ie_web.true,ab_ubnt3_web.neither,ab_w2cvj_web.true,ab_web_aa_continuous.false,ab_xpz0k_web.false,ab_xr2kh_web.variant1,ab_xzv8z_web.false,ab_y8s2m_web.variant3,ab_zkixf_web.false,ab_zvxp0_web.neither",
        "x-operation-name": "GetSearchResults",
        "x-stockx-device-id": "2022f346-cd49-4668-a21b-ce2ad32a295c",
        "x-stockx-session-id": "7f43d548-cd2f-4cb0-af31-4600826d7367",
    }

    json_data = {
        "query": "query GetSearchResults($countryCode: String!, $currencyCode: CurrencyCode!, $filtersVersion: Int, $page: BrowsePageInput, $query: String!, $sort: BrowseSortInput, $staticRanking: BrowseExperimentStaticRankingInput, $list: String, $skipVariants: Boolean!, $marketName: String, $searchCategoriesDisabled: Boolean!) {\n  browse(\n    query: $query\n    page: $page\n    sort: $sort\n    filtersVersion: $filtersVersion\n    experiments: {staticRanking: $staticRanking}\n  ) {\n    categories @skip(if: $searchCategoriesDisabled) {\n      id\n      name\n      count\n    }\n    results {\n      edges {\n        objectId\n        node {\n          ... on Product {\n            id\n            listingType\n            urlKey\n            title\n            primaryTitle\n            secondaryTitle\n            media {\n              thumbUrl\n            }\n            brand\n            productCategory\n            market(currencyCode: $currencyCode) {\n              state(country: $countryCode, market: $marketName) {\n                askServiceLevels {\n                  expressExpedited {\n                    count\n                    lowest {\n                      amount\n                    }\n                  }\n                  expressStandard {\n                    count\n                    lowest {\n                      amount\n                    }\n                  }\n                }\n              }\n            }\n            favorite(list: $list)\n            variants @skip(if: $skipVariants) {\n              id\n            }\n          }\n          ... on Variant {\n            id\n            product {\n              id\n              listingType\n              urlKey\n              primaryTitle\n              secondaryTitle\n              media {\n                thumbUrl\n              }\n              brand\n              productCategory\n            }\n            market(currencyCode: $currencyCode) {\n              state(country: $countryCode, market: $marketName) {\n                askServiceLevels {\n                  expressExpedited {\n                    count\n                    lowest {\n                      amount\n                    }\n                  }\n                  expressStandard {\n                    count\n                    lowest {\n                      amount\n                    }\n                  }\n                }\n              }\n            }\n          }\n        }\n      }\n      pageInfo {\n        limit\n        page\n        pageCount\n        queryId\n        queryIndex\n        total\n      }\n    }\n    sort {\n      id\n      order\n    }\n  }\n}",
        "variables": {
            "countryCode": "IN",
            "currencyCode": "USD",
            "filtersVersion": 4,
            "query": query,
            "sort": {
                "id": "featured",
                "order": "DESC",
            },
            "staticRanking": {
                "enabled": True,
            },
            "skipVariants": True,
            "searchCategoriesDisabled": False,
            "marketName": None,
            "page": {
                "index": 1,
                "limit": 10,
            },
        },
        "operationName": "GetSearchResults",
    }

    response = requests.post(
        "https://stockx.com/api/p/e", cookies=cookies, headers=headers, json=json_data
    )

    try:
        data = response.json()  # Attempt to parse JSON
    except json.JSONDecodeError:
        print("Error parsing JSON response")
        print(
            "Response content:", response.text
        )  # Debugging: print the response content
        return []

    return data.get("data", {}).get("browse", {}).get("results", {}).get("edges", [])


def create_stockx_list(results, size):
    shoe_data = []
    for product in results:
        name = product.get("node", "N/A").get("title", "N.A.")
        shoe_id = product["node"]["urlKey"]
        image_url = product.get("node", {}).get("media", "N/A").get("thumbUrl", "N.A.")
        shoe_url = "https://www.stockx.com/" + shoe_id
        shoe_data.extend(get_stockx_info(name, shoe_id, size, shoe_url, image_url))
    

    return shoe_data
