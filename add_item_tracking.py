import argparse
import scraper

def main():
    # Create the parser
    parser = argparse.ArgumentParser(description="Add URL of the item that you want to track the price of")

    # Add the arguments
    parser.add_argument("url", type=str, help="The URL of the product that you want to track")

    # Parse the arguments
    args = parser.parse_args()

    # get the url
    result = args.url
    print('URL: ' + result)

    scraper.add_new_product_info(result)

if __name__ == "__main__":
    main()
