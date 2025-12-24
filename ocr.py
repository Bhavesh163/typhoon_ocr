import requests
import json
import os
import sys
from pathlib import Path

def extract_text_from_image(image_path, api_key, model, task_type, max_tokens, temperature, top_p, repetition_penalty, pages=None):
    url = "https://api.opentyphoon.ai/v1/ocr"

    with open(image_path, 'rb') as file:
        files = {'file': file}
        data = {
            'model': model,
            'task_type': task_type,
            'max_tokens': str(max_tokens),
            'temperature': str(temperature),
            'top_p': str(top_p),
            'repetition_penalty': str(repetition_penalty)
        }

        if pages:
            data['pages'] = json.dumps(pages)

        headers = {
            'Authorization': f'Bearer {api_key}'
        }

        response = requests.post(url, files=files, data=data, headers=headers)

        if response.status_code == 200:
            result = response.json()

            # Extract text from successful results
            extracted_texts = []
            for page_result in result.get('results', []):
                if page_result.get('success') and page_result.get('message'):
                    content = page_result['message']['choices'][0]['message']['content']
                    try:
                        # Try to parse as JSON if it's structured output
                        parsed_content = json.loads(content)
                        text = parsed_content.get('natural_text', content)
                    except json.JSONDecodeError:
                        text = content
                    extracted_texts.append(text)
                elif not page_result.get('success'):
                    print(f"Error processing {page_result.get('filename', 'unknown')}: {page_result.get('error', 'Unknown error')}")

            return '\n'.join(extracted_texts)
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None

def process_all_pdfs():
    api_key = "sk-mqnSVbHwP4aDovxg5IRaLvZ6gyVnVaWfZP3dOJVt1J2ECjD8"
    input_dir = Path("input")
    output_dir = Path("output")
    
    model = "typhoon-ocr"
    task_type = "default"
    max_tokens = 16384
    temperature = 0.1
    top_p = 0.6
    repetition_penalty = 1.2
    pages = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22]
    
    output_dir.mkdir(exist_ok=True)
    
    pdf_files = sorted(input_dir.glob("*.pdf"))
    
    if not pdf_files:
        print(f"No PDF files found in {input_dir}/")
        return
    
    print(f"Found {len(pdf_files)} PDF(s) to process.")
    print(f"Output directory: {output_dir}/")
    print("-" * 50)
    
    for i, pdf_path in enumerate(pdf_files, 1):
        print(f"[{i}/{len(pdf_files)}] Processing {pdf_path.name}...")
        
        try:
            extracted_text = extract_text_from_image(
                str(pdf_path), api_key, model, task_type, 
                max_tokens, temperature, top_p, repetition_penalty, pages
            )
            
            if extracted_text:
                output_file = output_dir / f"{pdf_path.stem}.txt"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(extracted_text)
                print(f"  Success -> {output_file.name}")
            else:
                print("  Failed to extract text")
        except Exception as e:
            print(f"  Error: {e}")
    
    print("\nOCR processing complete.")

if __name__ == "__main__":
    process_all_pdfs()
