import sys
import argparse
import re
from email import message_from_bytes
from urllib.parse import urlparse
from collections import defaultdict

def scan_emails_for_tracking_pixels(file_path, domain=None, ignore_embedded=False, unique_names=False, max_unique_names=1000, image_domain=None, quiet=False):
    image_urls = set()
    email_data = bytearray()
    email_count = 0
    emails_with_unique_images = defaultdict(list)
    image_reference_count = defaultdict(int)

    def process_email_data():
        nonlocal email_count
        email_count += 1
        try:
            process_email(email_data, email_count, domain, ignore_embedded, unique_names, image_urls, emails_with_unique_images, image_reference_count, image_domain)
            if not quiet:
                print(f"Processed email {email_count}")
        except ValueError as error:
            print(f"Warning: An error occurred while processing email {email_count}: {error}")

    # First pass: Collect image URLs
    print("Scanning emails to collect image URLs...")
    with open(file_path, 'rb') as file:
        for line in file:
            email_data.extend(line)
            if line.startswith(b"From "):
                if email_data:
                    process_email_data()
                    email_data.clear()

    # Process the last email, if any
    if email_data:
        process_email_data()

    print("First pass completed!")

    # Process image URLs
    print("Processing image URLs...")
    for url in image_urls:
        count = image_reference_count[url]
        if unique_names and count > 1:
            continue
        print(f"\nImage URL: {url}")
        print(f"Referenced {count} time(s)")
        emails = emails_with_unique_images[url]
        for email in emails:
            print(f"Email {email['email_count']} - Date: {email['date']}, From: {email['sender']}")

def process_email(email_data, email_count, domain, ignore_embedded, unique_names, image_urls, emails_with_unique_images, image_reference_count, image_domain):
    message = message_from_bytes(email_data)
    sender_header = message['From']
    sender = str(sender_header) if sender_header is not None else None
    email_info = {
        'email_count': email_count,
        'sender': sender,
        'date': message['Date']
    }
    sender_domain = get_domain_from_email(sender)

    if sender is not None:
        for part in message.walk():
            content_type = part.get_content_type()
            if content_type.startswith('text/html'):
                html_content = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                if not domain or (domain and domain in sender):
                    extract_image_urls(html_content, image_urls, ignore_embedded, unique_names, email_info, emails_with_unique_images, image_reference_count, sender_domain, image_domain)

def extract_image_urls(html_content, image_urls, ignore_embedded, unique_names, email_info, emails_with_unique_images, image_reference_count, sender_domain, image_domain):
    soup = None
#html5lib = browser like parsing but slower, then fall back to others if it cannot handle malformed html (although html5lib is most robust)
    parsers = ['html5lib', 'lxml', 'html.parser']

    for parser in parsers:
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html_content, parser)
            break  # Break the loop if parsing is successful
        except Exception as e:
            print(f"Warning: A parsing error occurred with {parser}: {e}")
            continue  # Try the next parser

    if soup is None:
        print("Error: All parsers failed to parse the HTML content.")
        return  # Skip further processing of this email

    for img_tag in soup.find_all('img'):
        src = img_tag.get('src')
        if src and not is_embedded_image(src) and (is_different_domain(src, sender_domain, image_domain) or unique_names):
            if unique_names:
                image_url = get_image_url(src)
                image_reference_count[image_url] += 1
                if image_reference_count[image_url] > 1:
                    continue
                image_urls.add(image_url)
                emails_with_unique_images[image_url].append(email_info)
            else:
                image_urls.add(src)
                image_reference_count[src] += 1
                emails_with_unique_images[src].append(email_info)

def is_different_domain(url, sender_domain, image_domain):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()
    return domain != sender_domain or (image_domain and domain != image_domain)

def is_embedded_image(url):
    return url.lower().startswith('cid:')

def get_image_url(url):
    parsed_url = urlparse(url)
    return parsed_url.geturl()

def get_domain_from_email(email):
    try:
        if email is not None:
            email_str = str(email)
            parsed_email = email_str.split('@')
            if len(parsed_email) > 1:
                return parsed_email[1].lower()
    except Exception as e:
        print(f"Warning: Error processing email address '{email}': {e}")
    return None


# Example usage:
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Email Tracking Pixel Scanner")
    parser.add_argument("file_path", help="Path to the RFC822 file")
    parser.add_argument("-d", "--domain", help="Domain to filter for emails")
    parser.add_argument("-e", "--ignore-embedded", action="store_true", help="Ignore embedded images")
    parser.add_argument("-u", "--unique-names", action="store_true", help="Search only for images with unique names")
    parser.add_argument("-m", "--max-unique-names", type=int, default=1000, help="Maximum number of unique image names to track")
    parser.add_argument("-i", "--image-domain", action="store_true", help="Process only images from a different domain than the sender")
    parser.add_argument("-y", "--auto-proceed", action="store_true", help="Automatically proceed with the scan without confirmation")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress progress messages")
    args = parser.parse_args()

# Prompt the user to decide whether to proceed
    if not args.auto_proceed:
        print("Copyright (C) 2023 James Collings")
        print("Disclaimer: By using this software, the user agrees and understands that the writer ", end="")
        print("bears no responsibility for any consequences, direct or indirect, arising from its use. ", end="")
        print("Use of this software is at your own risk and you agree to not use the software if this disclaimer cannot be fully applied. Caveat emptor applies.")
        proceed = input("Do you wish to proceed with the scan? (y/n): ").strip().lower()
        if proceed != 'y':
            print("Operation cancelled.")
            sys.exit()

    scan_emails_for_tracking_pixels(args.file_path, args.domain, args.ignore_embedded, args.unique_names, args.max_unique_names, args.image_domain, args.quiet)