import argparse
import scraper

def main():
    # Create the parser
    parser = argparse.ArgumentParser(description="Add URL of the item that you want to track the price of and your email to receive notifications")

    # Add the arguments
    parser.add_argument("url", type=str, help="The URL of the product that you want to track")

    # Add the arguments
    parser.add_argument("email", type=str, help="The email to receive notifications for price drops")

    # Parse the arguments
    args = parser.parse_args()

    # get the url
    url = args.url
    print('URL: ' + url)

    #get the email
    email = args.email
    print('Email: ' + email)

    scraper.add_new_product_info(url, email)

if __name__ == "__main__":
    main()
