#!/usr/bin/env python3
import os
import argparse
from pathlib import Path
from openai import OpenAI

INPUT_DIR = Path('output')
OUTPUT_DIR = Path('output_revised')
MODEL_NAME = "google/gemini-3-flash-preview"

SYSTEM_PROMPT = """
As you are a top thai senior lawyer, could you please apply these things below to my output:
แปลงเลขไทย (๑,๒,๓,...) เป็นเลขอารบิก (1,2,3,...)
ห้ามสร้างหมายเลขคดีหรือบทบัญญัติใหม่หรือข้อกฎหมายใหม่,
ผลลัพธ์สุดท้ายเป็นไฟล์เดียว
The start of each paragraph should be the same don't mix up between paragraphs

ไม่ย่อ ไม่สรุป  รักษาโครงสร้างเดิม  ห้ามรวมหรือแยกคำพิพากษา ถ้าไม่ได้มี header ชัดเจน everything must stay the same except below:
1. เอาเลขหน้าออก,
2. แต่ละคำพิพากษาเริ่มที่ คำพิพากษาศาลฎีกาที่ xxxx/year  ขอให้เอารายชื่อและสถานะของโจทก์ พยาน ผู้ร้องและผู้คัดค้านออก (หากมี) ที่อยู่ช่วงต้นของแต่ละคำพิพากษาศาลฎีกาออก  เช่น นายมุข พิศโฉม โจทก์    บริษัทรุ่งเรืองบริการขนส่ง จำกัด จำเลย,
3. Then, there will be law references. These will be called เรื่อง. Please write down "เรื่อง:" before these groups of law references.
4. Then, there will be some paragraphs will bold letters. Please write down "ประเด็นหลัก:" before these groups of bold letter paragraphs.
5. After the end the bold paragraphs, there will be many paragraphs of light(normal) letters. Please write down "รายละเอียด:" before these groups of paragraphs.
6. แต่ละคำพิพากษาเริ่มที่ คำพิพากษาศาลฎีกาที่ xxxx/year  ขอให้เแอารายชื่อด้านท้ายของคำพิพากษาและสถานะออก เช่น (รังสรรค์ ดวงพัตรา - รีรา ไวยหงษ์ รินทร์ศรี - อาเล็ก จรรยาทรัพย์กิจ)   ประเสริฐ เสียงสุทธิวงศ์ - ย่อ     เมธี ประจงการ - ตรวจ,
"""

def get_client():
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("Error: OPENROUTER_API_KEY environment variable is not set.")
        print("Please export it: export OPENROUTER_API_KEY='sk-or-...'")
        return None
    
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

def revise_verdict(client, content, filename):
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Filename: {filename}\n\nContent:\n{content}"}
            ],
            temperature=0.1,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"  Error calling API: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Revise Thai verdicts using OpenRouter")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of files to process (0 for all)")
    parser.add_argument("--file", type=str, help="Process a specific file name")
    args = parser.parse_args()

    client = get_client()
    if not client:
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if args.file:
        files = [INPUT_DIR / args.file]
        if not files[0].exists():
            print(f"File not found: {files[0]}")
            return
    else:
        files = sorted(INPUT_DIR.glob("*.txt"))
    
    if args.limit > 0:
        files = files[:args.limit]

    print(f"Found {len(files)} files to process.")
    print(f"Output directory: {OUTPUT_DIR}")
    print("-" * 50)

    import re

    for i, file_path in enumerate(files, 1):
        print(f"[{i}/{len(files)}] Processing {file_path.name}...")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            if not content:
                print("  Skipping (empty content)")
                continue

            revised_content = revise_verdict(client, content, file_path.name)
            
            if revised_content:
                output_path = OUTPUT_DIR / file_path.name
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(revised_content)
                print("  Success")
            else:
                print("  Failed to get response")

        except Exception as e:
            print(f"  Error processing file: {e}")

    print("\nRewriting complete.")

if __name__ == "__main__":
    main()
