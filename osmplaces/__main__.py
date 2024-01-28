import os
import sys
import xml.etree.ElementTree as ET
import json
from tqdm import tqdm
import argparse 

# accept xml_file and output_dir args:
def parse_osm_and_save(xml_file, output_dir):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # initialize dict
    data_by_language = {}

    for node in tqdm(root.findall('node'), desc="Processing nodes"):
        node_id = node.get('id')
        lat = node.get('lat')
        lon = node.get('lon')

        for tag in node.findall('tag'):
            key = tag.get('k')
            if ':' in key and key.startswith('name:'):
                lang = key.split(':')[1]
                name = tag.get('v')

                if lang not in data_by_language:
                    data_by_language[lang] = []

                data_by_language[lang].append({
                    'id': node_id,
                    'lat': lat,
                    'lon': lon,
                    'name': name
                })

    # make output dirs:
    os.makedirs(output_dir, exist_ok=True)

    # write json files:
    for lang, data in data_by_language.items():
        output_file_path = os.path.join(output_dir, f'output_nodes_{lang}.json')
        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    parser = argparse.ArgumentParser(description='Process OSM files.')
    parser.add_argument('-i', '--input', required=True, help='Input OSM file path')
    parser.add_argument('-o', '--output', default='populated_places_json', help='Output directory for JSON files')

    args = parser.parse_args()

    parse_osm_and_save(args.input, args.output)

if __name__ == "__main__":
    main()
