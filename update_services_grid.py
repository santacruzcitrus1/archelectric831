#!/usr/bin/env python3

import os
import re
from pathlib import Path

# Levi's real services
SERVICES_HTML = '''                <div class="service-card">
                    <div class="service-icon">🔌</div>
                    <h3>Panel Upgrades & Changes</h3>
                    <p>Upgrading outdated electrical panels is essential for safety and modern electrical demands. We replace dangerous panels including Federal Pacific, Zinsco, and outdated fuse boxes with modern circuit breaker panels that can handle today's electrical needs.</p>
                </div>
                <div class="service-card">
                    <div class="service-icon">🚗</div>
                    <h3>EV Charger Installation</h3>
                    <p>Ready to go electric? We install Level 2 EV charging stations for Tesla, Chevy Bolt, Nissan Leaf, and all electric vehicles. From basic 240V outlets to smart charging systems with scheduling and monitoring features.</p>
                </div>
                <div class="service-card">
                    <div class="service-icon">🔋</div>
                    <h3>Solar & Battery Backup</h3>
                    <p>Maximize your solar investment with battery backup systems. We install and wire Tesla Powerwall, Enphase Encharge, and other battery storage systems to keep your lights on when the grid goes down.</p>
                </div>
                <div class="service-card">
                    <div class="service-icon">⚡</div>
                    <h3>Generator Backup Systems</h3>
                    <p>Never lose power again. We install and wire standby generators including Generac, Kohler, and other backup power systems. Automatic transfer switches ensure seamless power during outages.</p>
                </div>
                <div class="service-card">
                    <div class="service-icon">🏠</div>
                    <h3>Full House Rewiring</h3>
                    <p>Older homes need modern wiring. We specialize in complete electrical overhauls — replacing knob & tube wiring, upgrading to modern code, and ensuring your home's electrical system is safe and reliable.</p>
                </div>
                <div class="service-card">
                    <div class="service-icon">🔧</div>
                    <h3>New Construction & Commercial</h3>
                    <p>From residential new builds to commercial projects, we handle electrical rough-in, finish work, and everything in between. Licensed for both residential and commercial electrical work.</p>
                </div>'''

def update_services_grid(file_path):
    """Update the services grid in a city page"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Find and replace the services grid
    services_pattern = r'(<div class="services-grid">)(.*?)(</div>\s*<div class="center">)'
    
    match = re.search(services_pattern, content, re.DOTALL)
    if match:
        new_content = match.group(1) + '\n' + SERVICES_HTML + '\n            ' + match.group(3)
        content = re.sub(services_pattern, new_content, content, flags=re.DOTALL)
        
        # Update the section subtitle
        content = re.sub(
            r'<p class="section-sub">Full-service electrical for residential and agricultural properties\.</p>',
            '<p class="section-sub">Complete electrical solutions — residential, commercial, and new construction.</p>',
            content
        )
        
        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated services: {file_path}")
        else:
            print(f"No services changes: {file_path}")
    else:
        print(f"Services grid not found: {file_path}")

def main():
    base_dir = "/root/.openclaw/workspace/arch-electric-demo"
    
    # Find all city page directories
    city_dirs = []
    for item in os.listdir(base_dir):
        if item.startswith('electrician-') and os.path.isdir(os.path.join(base_dir, item)):
            city_dirs.append(item)
    
    print(f"Updating services grid in {len(city_dirs)} city directories")
    
    # Update each city page
    for city_dir in sorted(city_dirs):
        index_file = os.path.join(base_dir, city_dir, 'index.html')
        if os.path.exists(index_file):
            update_services_grid(index_file)
    
    print("Services grid update complete!")

if __name__ == "__main__":
    main()