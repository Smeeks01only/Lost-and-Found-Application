import zipfile
import xml.etree.ElementTree as ET
import sys

try:
    with zipfile.ZipFile("CHAPTER 1 -3.docx") as z:
        xml_content = z.read("word/document.xml")
    root = ET.fromstring(xml_content)
    # namespaces usually need to be handled carefully, but let's try finding all w:t elements
    # The namespace for w is typically http://schemas.openxmlformats.org/wordprocessingml/2006/main
    namespace = {'w': "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    
    text_content = []
    # Find all paragraphs to keep some structure? Or just all text nodes.
    # To keep structure, iterate over paragraphs (w:p) then runs (w:r) then text (w:t)
    
    for p in root.findall(".//w:p", namespace):
        para_text = ""
        for t in p.findall(".//w:t", namespace):
            if t.text:
                para_text += t.text
        if para_text.strip():
            text_content.append(para_text)
            
    with open("requirements_extracted.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(text_content))
    print("Extraction successful")
except Exception as e:
    print(f"Error: {e}")
