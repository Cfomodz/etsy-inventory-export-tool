import csv
import json
import requests


def get_listing_details(shop_id, listing_id):
    cookies = {
        # your_authenticated_session_cookies
    }

    headers = {
        # your_authenticated_session_headers
    }

    params = {
        'inventory_listing_id': '12',
    }

    response = requests.get(
        f'https://www.etsy.com/api/v3/ajax/bespoke/shop/{shop_id}/listings/{listing_id}/form',
        params=params,
        cookies=cookies,
        headers=headers,
    )
    return response.json()


def parse_json_data(json_data):
    # Extract the required data
    listing = json_data["listing"]
    product_name = listing["title"]
    image_urls = " ".join(listing["images"])
    price = listing["price"]
    tags = ";".join(listing["tags"])
    color = listing["attributes"][0]["values"][0]["value"] if listing["attributes"] else ""
    description = listing["description"].replace('\n', ' ').replace('\r', ' ')
    shipping_cost = str(listing["shipping"]["entries"][0]["primary_cost"]) if listing["shipping"]["entries"] else ""

    # Return the data as a tuple
    return product_name, image_urls, price, tags, color, description, shipping_cost


def write_to_csv(data, csv_file_path):
    # Check if the CSV file exists
    file_exists = False
    try:
        with open(csv_file_path, 'r'):
            file_exists = True
    except FileNotFoundError:
        pass

    # Open the CSV file in append mode or create a new one
    with open('output.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write headers if the file is newly created
        if not file_exists:
            headers = ["Product Name", "Product Image URLs", "Price", "Tags", "Color", "Item Description",
                       "Shipping Cost"]
            writer.writerow(headers)

        # Write the data
        writer.writerow(data)


def process_json_data(json_data, csv_file_path='output.csv'):
    # Parse the JSON data
    csv_data = parse_json_data(json_data)

    # Write the data to the CSV file
    write_to_csv(csv_data, csv_file_path)

    print("Data successfully written to CSV.")


def main():
    shop_id = '12345678'  # Your shop ID
    with open('etsy_stock.csv', 'r') as f:  # CSV file containing listing URLs
        # Can be saved from Etsy using WebScraper, Link Klipper, or other extension
        reader = csv.reader(f)
        listing_ids = [line[0].split('listings/')[1].split('?')[0] for line in reader]
        print(listing_ids)
        for listing_id in listing_ids:
            print(listing_id)
            json_response = get_listing_details(shop_id=shop_id, listing_id=listing_id)
            print(json_response)
            process_json_data(json_response)


if __name__ == '__main__':
    main()
