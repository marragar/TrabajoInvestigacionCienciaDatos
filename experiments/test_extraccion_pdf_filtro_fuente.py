import pdfplumber
from collections import Counter

with pdfplumber.open("ResolucionBOCYL2021.pdf") as pdf:
    page = pdf.pages[3]  

    fonts = Counter(c['fontname'] for c in page.chars)
    print("Fuentes presentes:")
    for font, count in fonts.most_common():
        print(f"  {font}: {count}")


    clean_page = page.filter(
        lambda obj: obj.get('object_type') != 'char' or 'Calibri' not in obj.get('fontname', '')
    )

    print("\n--- Texto sucio ---")
    print(page.extract_text()[:300])

    print("\n--- Texto limpio ---")
    print(clean_page.extract_text()[:300])