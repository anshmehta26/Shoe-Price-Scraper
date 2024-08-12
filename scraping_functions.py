from urllib.parse import quote
from bs4 import BeautifulSoup
from curl_cffi import requests
import json

def fetch_ebay_data(keyword, shoe_size, max_price):
    url = f"https://www.ebay.com/sch/i.html?_nkw={quote(keyword)}&_sop=12"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve data: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    items = []

    for item in soup.select('.s-item'):
        title_tag = item.select_one('.s-item__title')
        price_tag = item.select_one('.s-item__price')
        bid_tag = item.select_one('.s-item__bidCount')
        url_tag = item.select_one('.s-item__link')
        size_tag = item.find(string=lambda string: string and shoe_size in string)
        shipping_tag = item.select_one('.s-item__shipping, .s-item__freeXDays')
        image_tag = item.select_one('div.s-item__image-wrapper.image-treatment img')

        if title_tag and price_tag and url_tag and size_tag and image_tag:
            # Filter out ads or non-product items
            if 'Shop on eBay' in title_tag.text or 'Shop eBay' in title_tag.text:
                continue
            
            # Handle price ranges and bids
            price_text = price_tag.text.replace('$', '').replace(',', '').strip()
            if ' to ' in price_text:
                price_text = price_text.split(' to ')[0]
            try:
                price = float(price_text)
            except ValueError:
                continue

            if price <= max_price:
                shipping_cost = 0.0
                if shipping_tag:
                    shipping_text = shipping_tag.text.strip().replace('$', '').replace(',', '')
                    if 'Free' not in shipping_text:
                        try:
                            shipping_cost = float(shipping_text.split()[0])
                        except ValueError:
                            shipping_cost = 0.0

                image_url = image_tag.get('src', '')  # Safely get the src attribute

                item_data = {
                    'title': title_tag.text,
                    'price': price,
                    'currency': 'USD',
                    'url': url_tag['href'],
                    'bids': bid_tag.text if bid_tag else 'N/A',
                    'shipping': shipping_cost,
                    'image_url': image_url  # Add image URL
                }
                items.append(item_data)

    return items

def get_goat_info(shoe_name, productTemplateId, size, url, image_url):
# Placeholder dictionary for result
  result = []

  # Make the request using curl_cffi
  cookies = {
      '__cf_bm': 'SIlqQNGW30ThLpA0QEmU6JVGqjQ6fLWmjsPF8Wf4tcU-1722982299-1.0.1.1-GVx_q2jZjm3Y6d_BoP5l0PSBrNfT27GK.PjemsTyIyXXwssvYjq3D.lssWWPOmzyph5iKnSrrSvBYMfdMt.Jdw',
      'ConstructorioID_client_id': '2e49a720-0113-4221-a89d-4162f4298810',
      'ConstructorioID_session_id': '1',
      'ConstructorioID_session': '{"sessionId":1,"lastTime":1722982300052}',
      'locale': 'en',
      '_gid': 'GA1.2.1496568402.1722982301',
      '_csrf': 'cScgOoPKI43LD3mUZeFIBAjO',
      'country': 'IN',
      'currency': 'USD',
      '_ga': 'GA1.1.1771785265.1722982301',
      '_gcl_au': '1.1.1649408364.1722982301',
      'OptanonAlertBoxClosed': '2024-08-06T22:12:00.299Z',
      'OptanonConsent': 'isIABGlobal=false&datestamp=Wed+Aug+07+2024+03%3A42%3A00+GMT%2B0530+(India+Standard+Time)&version=6.10.0&hosts=&consentId=5403f868-99a0-40cc-97c7-6ccaafbd55e7&interactionCount=1&landingPath=NotLandingPage&groups=C0003%3A1%2CC0001%3A1%2CC0002%3A1%2CC0004%3A1',
      '_scid': 'd28e81fa-5339-4e2c-8851-e552da2a1e62',
      '_scid_r': 'd28e81fa-5339-4e2c-8851-e552da2a1e62',
      '_ScCbts': '%5B%5D',
      'IR_gbd': 'goat.com',
      'IR_12522': '1722982320768%7C0%7C1722982320768%7C%7C',
      '_ga_28GTCC4968': 'GS1.1.1722982301.1.1.1722982355.0.0.0',
      'csrf': 'oM9VH30D-jXzLlb1lT-Ew6KFaqftsbet4bag',
  }

  headers = {
      'accept': 'application/json',
      'accept-language': 'en-GB,en;q=0.9',
      'cookie': '__cf_bm=SIlqQNGW30ThLpA0QEmU6JVGqjQ6fLWmjsPF8Wf4tcU-1722982299-1.0.1.1-GVx_q2jZjm3Y6d_BoP5l0PSBrNfT27GK.PjemsTyIyXXwssvYjq3D.lssWWPOmzyph5iKnSrrSvBYMfdMt.Jdw; ConstructorioID_client_id=2e49a720-0113-4221-a89d-4162f4298810; ConstructorioID_session_id=1; ConstructorioID_session={"sessionId":1,"lastTime":1722982300052}; locale=en; _gid=GA1.2.1496568402.1722982301; _csrf=cScgOoPKI43LD3mUZeFIBAjO; country=IN; currency=USD; _ga=GA1.1.1771785265.1722982301; _gcl_au=1.1.1649408364.1722982301; OptanonAlertBoxClosed=2024-08-06T22:12:00.299Z; OptanonConsent=isIABGlobal=false&datestamp=Wed+Aug+07+2024+03%3A42%3A00+GMT%2B0530+(India+Standard+Time)&version=6.10.0&hosts=&consentId=5403f868-99a0-40cc-97c7-6ccaafbd55e7&interactionCount=1&landingPath=NotLandingPage&groups=C0003%3A1%2CC0001%3A1%2CC0002%3A1%2CC0004%3A1; _scid=d28e81fa-5339-4e2c-8851-e552da2a1e62; _scid_r=d28e81fa-5339-4e2c-8851-e552da2a1e62; _ScCbts=%5B%5D; IR_gbd=goat.com; IR_12522=1722982320768%7C0%7C1722982320768%7C%7C; _ga_28GTCC4968=GS1.1.1722982301.1.1.1722982355.0.0.0; csrf=oM9VH30D-jXzLlb1lT-Ew6KFaqftsbet4bag',
      'priority': 'u=1, i',
      'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-origin',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
      'x-csrf-token': 'oM9VH30D-jXzLlb1lT-Ew6KFaqftsbet4bag',
  }

  params = {
      'productTemplateId': productTemplateId,
      'countryCode': 'IN',
  }

  response = requests.get(
      'https://www.goat.com/web-api/v1/product_variants/buy_bar_data',
      params=params,
      cookies=cookies,
      headers=headers,
  )

  if response.status_code == 200:
      json_data = response.json()
      
      # Iterate through the JSON data
      for item in json_data:
          if item['sizeOption']['presentation'] > size:
              break
          # Check if the size and condition match
          if item['sizeOption']['presentation'] == size and item["stockStatus"]!="not_in_stock":
              # Extract relevant information
              shoe_info = {
                  'name': shoe_name,
                  #'price':  "$" + (item['lowestPriceCents'])[0:-2],
                  'price':  "$ " + str(item['lowestPriceCents']['amountUsdCents']/100),
                  'shoe_condition': item['shoeCondition'].replace("_", " "),
                  'box_condition': item['boxCondition'].replace("_", " "),
                  "url" : url,
                  "image_url" : image_url,
                  'source': 'GOAT'
              }
              # Add to result dictionary
              result.append(shoe_info)

  return result

def get_goat_data(query):
  headers = {
      'accept': '*/*',
      'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,hi;q=0.7',
      'origin': 'https://www.goat.com',
      'priority': 'u=1, i',
      'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'cross-site',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
  }

  params = {
      'c': 'ciojs-client-2.35.2',
      'key': 'key_XT7bjdbvjgECO5d8',
      'i': '4e67882b-cfd7-441f-a999-0c731045bfb6',
      's': '1',
      'page': '1',
      'num_results_per_page': '24',
      'sort_by': 'relevance',
      'sort_order': 'descending',
      '_dt': '1722542412951',
  }

  url = f'https://ac.cnstrc.com/search/{quote(query)}'
  response = requests.get(url, params=params, headers=headers)
  
  if response.status_code != 200:
      print(f"Failed to retrieve data: {response.status_code}")
      return []

  try:
      data = response.json()  # Attempt to parse JSON
  except json.JSONDecodeError:
      print("Error parsing JSON response")
      print("Response content:", response.text)  # Debugging: print the response content
      return []

  return data.get('response', {}).get('results', [])

def extract_shoe_data(results,size):
  shoe_data = []
  for product in results:
      name = product.get('value', 'N/A')
      shoe_id = product['data']['id']
      image_url = product.get('data', {}).get('image_url', 'N/A')
      shoe_url = "https://www.goat.com/sneakers/" + product.get('data').get('slug')
      shoe_data.extend(get_goat_info(name, shoe_id, size, shoe_url, image_url))

  return shoe_data