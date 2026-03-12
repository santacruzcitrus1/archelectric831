#!/usr/bin/env python3

import os
import re
from pathlib import Path

# Levi's updated business data
BUSINESS_DATA = {
    "tagline": "A+ is my only standard",
    "license": "C-10 #945992",
    "phone": "(831) 359-8747",
    "email_public": "archelectric831@gmail.com",
    "email_forms": "mentzlevi@gmail.com",
    "founding": "2004",
    "experience": "20+ years",
    "description_services": "Panel upgrades, EV chargers, solar/battery systems, generators, rewires & new construction",
    "review_url": "https://www.google.com/maps/place/Arch+Electric+%7C+831+Electrician/@36.867372,-121.7623285,10z/data=!4m6!3m5!1s0xa3d076a509efa8d7:0x40adf9248620164d!8m2!3d36.867372!4d-121.7623286!16s%2Fg%2F11v78pxtrq"
}

def update_city_page(file_path):
    """Update a single city page with Levi's business data"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Update meta description
    content = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="Licensed electrician serving {get_city_name(file_path)}, CA. {BUSINESS_DATA["description_services"]}. Family-owned, {BUSINESS_DATA["experience"]} experience. Call {BUSINESS_DATA["phone"]}.">',
        content
    )
    
    # Update OG description
    content = re.sub(
        r'<meta property="og:description" content="[^"]*">',
        f'<meta property="og:description" content="Licensed electrician serving {get_city_name(file_path)}, CA. {BUSINESS_DATA["description_services"]}. {BUSINESS_DATA["tagline"]}. Call {BUSINESS_DATA["phone"]} for a free estimate.">',
        content
    )
    
    # Update schema markup - change Electrician to ElectricalContractor
    content = re.sub(r'"@type": "Electrician"', '"@type": "ElectricalContractor"', content)
    
    # Update email in schema
    content = re.sub(r'"email": "[^"]*"', f'"email": "{BUSINESS_DATA["email_public"]}"', content)
    
    # Update license in schema
    content = re.sub(r'"identifier": "[^"]*"', f'"identifier": "{BUSINESS_DATA["license"]}"', content)
    
    # Update founding date
    content = re.sub(r'"foundingDate": "[^"]*"', f'"foundingDate": "{BUSINESS_DATA["founding"]}"', content)
    
    # Add service types to schema
    service_types = [
        "Panel Upgrades",
        "EV Charger Installation", 
        "Solar Battery Backup Systems",
        "Generator Installation",
        "Full House Rewiring",
        "New Construction Electrical",
        "Electrical Diagnostics",
        "Commercial Electrical"
    ]
    
    # Add serviceType array to schema if not present
    if '"serviceType":' not in content:
        content = re.sub(
            r'("identifier": "[^"]*")',
            r'\1,\n        "serviceType": ' + str(service_types).replace("'", '"'),
            content
        )
    
    # Update logo tagline in nav
    content = re.sub(
        r'<span class="logo-tagline">The Energy Experts</span>',
        f'<span class="logo-tagline">{BUSINESS_DATA["tagline"]}</span>',
        content
    )
    
    # Update city badges
    content = re.sub(
        r'<span class="city-badge">✓ Licensed #945992</span>',
        f'<span class="city-badge">✓ Licensed {BUSINESS_DATA["license"]}</span>',
        content
    )
    
    content = re.sub(
        r'<span class="city-badge">✓ Family Owned Since 2009</span>',
        f'<span class="city-badge">✓ {BUSINESS_DATA["experience"]} Experience</span>',
        content
    )
    
    content = re.sub(
        r'<span class="city-badge">✓ Fully Insured</span>',
        '<span class="city-badge">✓ Fully Insured & Bonded</span>',
        content
    )
    
    # Add review button to nav if not present
    if 'btn-review' not in content:
        nav_pattern = r'(<li><a href="/#portal"[^>]*>Client Portal</a></li>)'
        replacement = r'\1\n                <li><a href="' + BUSINESS_DATA["review_url"] + '" class="btn-review" target="_blank" rel="noopener">⭐ Leave a Review</a></li>'
        content = re.sub(nav_pattern, replacement, content)
    
    # Update footer tagline and description
    footer_logo_pattern = r'(<span class="logo-tagline">)[^<]*(</span>)'
    content = re.sub(footer_logo_pattern, rf'\1{BUSINESS_DATA["tagline"]}\2', content)
    
    footer_desc_pattern = r'(<p>)Full-service electrical contractor serving the Tri-County area since 2009\.(</p>)'
    content = re.sub(footer_desc_pattern, rf'\1Family-owned electrical contractor serving Santa Cruz, Monterey, San Benito & Santa Clara counties with {BUSINESS_DATA["experience"]} experience.\2', content)
    
    footer_license_pattern = r'(<p>)CA License #945992(</p>)'
    content = re.sub(footer_license_pattern, rf'\1CA License {BUSINESS_DATA["license"]}\2', content)
    
    # Update CTA text
    content = re.sub(
        r'Call today for a free estimate\. Licensed, insured, and ready to help\.',
        f'No job too big or too small. We do them all. Call today for a free estimate — licensed, insured & bonded.',
        content
    )
    
    # Only write if content changed
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {file_path}")
    else:
        print(f"No changes: {file_path}")

def get_city_name(file_path):
    """Extract city name from file path"""
    path_parts = Path(file_path).parts
    for part in path_parts:
        if part.startswith('electrician-'):
            city = part.replace('electrician-', '').replace('-', ' ').title()
            return city
    return "Unknown"

def main():
    base_dir = "/root/.openclaw/workspace/arch-electric-demo"
    
    # Find all city page directories
    city_dirs = []
    for item in os.listdir(base_dir):
        if item.startswith('electrician-') and os.path.isdir(os.path.join(base_dir, item)):
            city_dirs.append(item)
    
    print(f"Found {len(city_dirs)} city directories")
    
    # Update each city page
    for city_dir in sorted(city_dirs):
        index_file = os.path.join(base_dir, city_dir, 'index.html')
        if os.path.exists(index_file):
            update_city_page(index_file)
    
    print("City pages update complete!")

if __name__ == "__main__":
    main()