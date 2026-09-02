import urllib.request
import json
import os
import re

# Colors for your custom UI style
RING_COLOR = "#d2b350" 
BG_COLOR = "#161411"

# Complete mapping of your RPG states to verified Game-icons.net filenames
states_to_icons = {
    "Accurate": "bullseye.svg",
    "Inaccurate": "broken-arrow.svg",
    "Afflicted": "poison-bottle.svg",
    "Mending": "bandage-roll.svg",
    "Bleeding": "bleeding-wound.svg",
    "Blinded": "blindfold.svg",
    "Burning": "flame.svg",
    "Fortified": "brick-wall.svg",
    "Frail": "shattered-glass.svg",
    "Guarded": "shield.svg",
    "Unguarded": "broken-shield.svg",
    "Hastened": "running-shoe.svg",
    "Hindered": "handcuffs.svg",
    "Provoked": "enrage.svg",
    "Slow": "snail.svg",
    "Swift": "sprint.svg",
    "Staggered": "knockout.svg",
    "Strong": "biceps.svg",
    "Weak": "broken-bone.svg",
    "Weary": "tired-eye.svg",
    "Willful": "brain.svg",
    
    "Bloodied": "blood.svg",
    "Defeated": "skull-crossed-bones.svg",
    "Grappled": "grab.svg",
    "Toppled": "falling.svg",
    "Shadowy": "ninja-head.svg",
    "Tenacious": "fist.svg"
}

# HIGH CONTRAST mapping for the inner icon colors
state_colors = {
    "Accurate": "#7BD3FC",      # Bright Cyan/Blue
    "Inaccurate": "#C4B4A1",    # Light Khaki/Grey
    "Afflicted": "#96E067",     # Bright Lime Green
    "Mending": "#69F0AE",       # Bright Mint/Teal
    "Bleeding": "#FF5C5C",      # Bright Red
    "Blinded": "#A696C2",       # Light Lavender
    "Burning": "#FF9E40",       # Bright Orange
    "Fortified": "#CDE0E8",     # Bright Silver
    "Frail": "#FCEAA9",         # Bright Sand
    "Guarded": "#70B0FF",       # Bright Sky Blue
    "Unguarded": "#FFA061",     # Bright Peachy Orange
    "Hastened": "#FFE342",      # Bright Yellow
    "Hindered": "#B5875E",      # Light Tan
    "Provoked": "#F55142",      # Bright Crimson
    "Slow": "#C0D194",          # Light Moss Green
    "Swift": "#5DFFED",         # Bright Aqua
    "Staggered": "#D17DFF",     # Bright Purple
    "Strong": "#FF8224",        # Bright Deep Orange
    "Weak": "#E4EBC8",          # Bright Pale Green-Yellow
    "Weary": "#B8D0EB",         # Light Pale Blue
    "Willful": "#EA7DFF",       # Bright Magenta
    "Bloodied": "#D41C1C",      # Vibrant Ruby Red
    "Defeated": "#9E9E9E",      # Light Grey (old one was too dark)
    "Grappled": "#B8B162",      # Light Olive
    "Toppled": "#C49B6C",       # Light Earth Brown
    "Shadowy": "#6387A6",       # Light Blue-Grey
    "Tenacious": "#FCE365"      # Bright Gold
}

print("Fetching Game-Icons.net repository tree from GitHub...")
url = "https://api.github.com/repos/game-icons/icons/git/trees/master?recursive=1"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (RPG Icon Downloader)'})

try:
    with urllib.request.urlopen(req) as response:
        tree_data = json.loads(response.read().decode())
except Exception as e:
    print(f"Error fetching repository tree: {e}")
    exit(1)

print("Parsing SVG paths...")
svg_paths = {
    item['path'].split('/')[-1]: item['path'] 
    for item in tree_data.get('tree', []) 
    if item['path'].endswith('.svg')
}

output_dir = os.path.join("icons", "states")
os.makedirs(output_dir, exist_ok=True)
print(f"Starting downloads into folder: {output_dir}/ \n")

for state, icon_name in states_to_icons.items():
    if icon_name in svg_paths:
        raw_url = f"https://raw.githubusercontent.com/game-icons/icons/master/{svg_paths[icon_name]}"
        output_path = os.path.join(output_dir, f"{state}.svg")
        icon_color = state_colors.get(state, "#ffffff")
        
        print(f"Formatting and downloading {state}.svg...")
        try:
            req_icon = urllib.request.Request(raw_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req_icon) as response:
                svg_data = response.read().decode('utf-8')
                
                # 1. Remove the default solid background path
                svg_data = svg_data.replace('<path d="M0 0h512v512H0z"/>', '')
                
                # 2. Change the default white icon fill to our high-contrast state color
                svg_data = svg_data.replace('fill="#fff"', f'fill="{icon_color}"')
                
                # 3. Inject Defs (Clipping), Dark Background, and the scaled group
                # top_injection = f'''
                # <defs><clipPath id="circleClip"><circle cx="256" cy="256" r="230"/></clipPath></defs>
                # <circle cx="256" cy="256" r="230" fill="{BG_COLOR}"/>
                # <g clip-path="url(#circleClip)">
                    
                # '''
                # svg_data = re.sub(r'(<svg[^>]*>)', r'\1' + top_injection, svg_data)
                
                # # 4. Close the groups and draw the golden border ON TOP
                # bottom_injection = f'''
                #     </g>
                # </g>
                # <circle cx="256" cy="256" r="230" fill="none" stroke="" stroke-width="24"/>
                # </svg>
                # '''
                # svg_data = svg_data.replace('</svg>', bottom_injection)
                
                with open(output_path, 'w', encoding='utf-8') as out_file:
                    out_file.write(svg_data)
                    
        except Exception as e:
            print(f"  Failed to download {state}.svg: {e}")
    else:
        print(f"  Could not find exact match for '{icon_name}' (State: {state}).")

print("\nFinished! Your icons are updated with high-contrast colors.")