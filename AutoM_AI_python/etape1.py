def run():
    import os
    import xml.etree.ElementTree as ET
    import json
    import requests
    import time
    import re

    INPUT_FOLDER = "input_xml"  # Can contain files with ANY extension
    OLLAMA_URL = "http://localhost:11434/api/generate"
    MODEL_NAME = "llama3"
    MAX_RETRIES = 5
    RETRY_DELAY = 2
    all_files = []

    if not os.path.isdir(INPUT_FOLDER):
        print(f"❌ Folder '{INPUT_FOLDER}' not found.")
        return

    # Load all files (regardless of extension)
    xml_contents = []
    file_names = []

    print(f"📂 Scanning all files in: {INPUT_FOLDER}")

    for file in os.listdir(INPUT_FOLDER):
        file_path = os.path.join(INPUT_FOLDER, file)
        if os.path.isfile(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    # Quick check: does it contain XML-like structure?
                    if "<Composant-Definition" in content:
                        xml_contents.append(content)
                        file_names.append(file)
            except Exception as e:
                print(f"⚠️ Error reading file {file}: {e}")

    if not xml_contents:
        print("⚠️ No valid XML-like files found.")
        return

    wrapped_xml = f"<ROOT>{''.join(xml_contents)}</ROOT>"

    try:
        root = ET.fromstring(wrapped_xml)
    except ET.ParseError as e:
        print(f"❌ XML Parse Error: {e}")
        return

    blocks = []
    for child in root:
        if child.tag == "Composant-Definition":
            blocks.append(ET.tostring(child, encoding='unicode'))

    print(f"🧩 Found {len(blocks)} <Composant-Definition> blocks\n")

    for file_id, xml_block in enumerate(blocks, start=1):
        match = re.search(r'<Composant-Definition\s+code="([^"]+)"', xml_block)
        file_name = f"{match.group(1)}.xml" if match else f"file_{file_id}.xml"

        prompt = f"""
You are a formatter. Given the following XML content, return only this JSON structure:

{{
  "file_id": {file_id},
  "file_name": "{file_name}",
  "content": "<escaped XML string>"
}}

🟢 Instructions:
- Escape all double quotes → \\" 
- Escape newlines → \\n
- Keep the full XML string intact
- Return ONLY valid JSON (no explanation, no markdown)

Here is the XML:
{xml_block}
        """

        print(f"⏳ Processing block {file_id}: {file_name}...")

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = requests.post(
                    OLLAMA_URL,
                    json={"model": MODEL_NAME, "prompt": prompt, "stream": False}
                )
                response_text = response.json().get("response", "").strip()
                result_json = json.loads(response_text)
                all_files.append(result_json)
                print(f"✅ Processed {file_name}\n")
                break

            except json.JSONDecodeError:
                print(f"❌ Attempt {attempt}: Invalid JSON returned.")
                print("Raw output:")
                print(response_text)

                if attempt < MAX_RETRIES:
                    print(f"🔁 Retrying in {RETRY_DELAY} seconds...\n")
                    time.sleep(RETRY_DELAY)
                else:
                    print(f"⚠️ Skipping {file_name} after {MAX_RETRIES} attempts.\n")

    print("\n💾 Saving final combined_result.json...")

    final_json = {
        "total_files": len(all_files),
        "files": all_files
    }

    with open("combined_result.json", "w", encoding="utf-8") as f:
        json.dump(final_json, f, indent=2)

    print("🎉 Done! Saved to combined_result.json")


if __name__ == "__main__":
    run()
