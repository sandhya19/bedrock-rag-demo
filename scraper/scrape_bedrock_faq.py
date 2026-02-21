import requests
from bs4 import BeautifulSoup
import json
import os

URL = "https://aws.amazon.com/bedrock/faqs"
OUTPUT_FILE = "bedrock_faq.json"


def fetch_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (RAG-Demo-Bot)"
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.text


# def parse_faq(html):
#     soup = BeautifulSoup(html, "html.parser")

#     faq_data = []

#     # AWS FAQ pages usually use expandable sections
#     # Questions are often in <h3> or <h2> tags
#     # Answers typically follow in <div> blocks

#     questions = soup.find_all(["h2", "h3"])

#     for q in questions:
#         question_text = q.get_text(strip=True)

#         # Try to get next sibling as answer container
#         answer_block = q.find_next_sibling()

#         if answer_block:
#             answer_text = answer_block.get_text(strip=True)

#             if question_text and answer_text:
#                 faq_data.append({
#                     "question": question_text,
#                     "answer": answer_text
#                 })

#     return faq_data

def parse_faq(html):
    soup = BeautifulSoup(html, "html.parser")
    faq_data = []

    # Find all FAQ trigger buttons
    buttons = soup.find_all("button", attrs={"aria-controls": True})

    for btn in buttons:
        question_span = btn.find("span", attrs={"data-rg-n": "UtilityText"})
        if not question_span:
            continue

        question_text = question_span.get_text(strip=True)

        # Get the linked answer div
        answer_id = btn.get("aria-controls")
        answer_div = soup.find("div", id=answer_id)

        if not answer_div:
            continue

        answer_text = answer_div.get_text(strip=True)

        if question_text and answer_text:
            faq_data.append({
                "question": question_text,
                "answer": answer_text
            })

    return faq_data

def save_to_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    html = fetch_page(URL)
    faq_pairs = parse_faq(html)

    if not faq_pairs:
        print("No FAQ data extracted. Page structure may require refinement.")
    else:
        save_to_json(faq_pairs, OUTPUT_FILE)
        print(f"Saved {len(faq_pairs)} Q&A pairs to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()