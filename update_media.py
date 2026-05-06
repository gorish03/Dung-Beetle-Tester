import os
import json
import time
import re

# Define folders and files
media_dir = 'media'
output_file = 'wip-content.js'
html_file = 'wip.html'

# Supported formats
valid_image_exts = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
valid_video_exts = ['.mp4', '.webm', '.mov']

content_list = []

# Scan the directory and sort alphabetically (sequential order)
for filename in sorted(os.listdir(media_dir)):
    ext = os.path.splitext(filename)[1].lower()
    
    if ext in valid_image_exts or ext in valid_video_exts:
        file_type = 'video' if ext in valid_video_exts else 'image'
        
        # Format the title (e.g., "01-base-defense.jpg" -> "01 Base Defense")
        raw_title = os.path.splitext(filename)[0]
        clean_title = raw_title.replace('-', ' ').replace('_', ' ').title()

        content_list.append({
            "file": f"{media_dir}/{filename}",
            "type": file_type,
            "tag": "update",
            "title": clean_title,
            "desc": "Auto-generated entry." 
        })

# Format the output back into valid JavaScript
js_output = f"""/**
 * AUTO-GENERATED CONTENT MANIFEST
 * Run update_media.py to refresh this list after adding files.
 */

const WIP_CONTENT = {json.dumps(content_list, indent=2)};

const UPCOMING_FEATURES = [
  {{ "title": "Carrier State Overhaul", "eta": "Q3 2025", "desc": "Full rework of dung-roll physics." }},
  {{ "title": "Closed Beta", "eta": "Q4 2025", "desc": "Invite-only playtest." }}
];
"""

# 1. Write the new JS file
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(js_output)

print(f"Success! {len(content_list)} files linked in {output_file}.")

# 2. CACHE BUSTING: Auto-update the HTML file with a new timestamp
if os.path.exists(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Generate a unique timestamp based on the exact second the script is run
    version_id = int(time.time())

    # Find the script tag and replace it with the new versioned tag
    # This regex catches it whether it has a ?v= already or not
    updated_html = re.sub(
        r'<script src="wip-content\.js(\?v=\d+)?"></script>',
        f'<script src="wip-content.js?v={version_id}"></script>',
        html_content
    )

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(updated_html)

    print(f"Cache-busted {html_file}! Browser will now instantly load the fresh media.")
else:
    print(f"Warning: {html_file} not found. Could not update cache version.")