
import os
import re
import time
import logging
from deep_translator import GoogleTranslator
import concurrent.futures

logging.basicConfig(level=logging.INFO, format='%(message)s', filename='translate_batch.log')

def translate_chunk(text, target_lang='ko'):
    if not text.strip(): return text
    translator = GoogleTranslator(source='auto', target=target_lang)
    for attempt in range(5):
        try:
            time.sleep(1)
            res = translator.translate(text)
            return res if res else text
        except Exception:
            time.sleep(2 + attempt)
    return text

def translate_text(text):
    # Protect inline code before splitting
    # We will replace inline code with placeholders to avoid translating it
    inline_codes = []
    def inline_replacer(match):
        inline_codes.append(match.group(0))
        return f"__INLINE_CODE_{len(inline_codes)-1}__"

    text = re.sub(r'`[^`\n]+`', inline_replacer, text)

    # Same for links, protect the URL part
    links = []
    def link_replacer(match):
        links.append(match.group(2))
        return f"[{match.group(1)}](__LINK_{len(links)-1}__)"

    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link_replacer, text)

    parts = re.split(r'(\n\n+)', text)
    translated_parts = []
    for part in parts:
        if not part.strip():
            translated_parts.append(part)
        elif part.startswith('|') and '|' in part[1:]:
            cells = part.split('|')
            new_cells = []
            for cell in cells:
                if '__INLINE_CODE_' in cell or '__LINK_' in cell or cell.strip().endswith('/') or cell.strip() == '' or re.match(r'^[-:\s]+$', cell):
                    new_cells.append(cell)
                elif len(re.findall(r'[a-zA-Z]', cell)) > 2:
                    new_cells.append(f" {translate_chunk(cell.strip())} ")
                else:
                    new_cells.append(cell)
            translated_parts.append("|".join(new_cells))
        else:
            translated_parts.append(translate_chunk(part))

    res = "".join(translated_parts)

    # Restore links
    for i, link in enumerate(links):
        res = res.replace(f"__LINK_{i}__", link)

    # Restore inline codes
    for i, code in enumerate(inline_codes):
        res = res.replace(f"__INLINE_CODE_{i}__", code)

    return res

def process_file(filepath):
    logging.info(f"Processing {filepath}")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if already translated
        # By looking at korean characters
        if len(re.findall(r'[가-힣]', content)) > 100:
            logging.info(f"Skipping {filepath}, already translated")
            return

        frontmatter_match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
        if frontmatter_match:
            fm_content = frontmatter_match.group(1)
            body = frontmatter_match.group(2)

            new_fm = []
            for line in fm_content.split('\n'):
                if line.startswith('description:'):
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        new_fm.append(f"{parts[0]}: {translate_chunk(parts[1].strip())}")
                    else:
                        new_fm.append(line)
                else:
                    new_fm.append(line)
            final_parts = [f"---\n{chr(10).join(new_fm)}\n---\n"]
        else:
            body = content
            final_parts = []

        code_pattern = re.compile(r'(```[\s\S]*?```)')
        last_pos = 0

        for match in code_pattern.finditer(body):
            start, end = match.span()
            text_chunk = body[last_pos:start]
            if text_chunk:
                final_parts.append(translate_text(text_chunk))
            final_parts.append(match.group(0))
            last_pos = end

        remaining = body[last_pos:]
        if remaining:
            final_parts.append(translate_text(remaining))

        final_content = "".join(final_parts)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(final_content)

        logging.info(f"Successfully processed {filepath}")

    except Exception as e:
        logging.error(f"Error {filepath}: {e}")

def main():
    files = []
    for root, dirs, fnames in os.walk('.'):
        if '.git' in dirs: dirs.remove('.git')
        if 'node_modules' in dirs: dirs.remove('node_modules')
        for f in fnames:
            if f.endswith('.md'):
                files.append(os.path.join(root, f))

    print(f"Total files: {len(files)}")
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        for i, _ in enumerate(executor.map(process_file, files)):
            if (i+1) % 10 == 0:
                print(f"Processed {i+1}/{len(files)}")

if __name__ == "__main__":
    main()
