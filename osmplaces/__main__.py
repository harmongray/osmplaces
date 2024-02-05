import os
import json
import subprocess
import stat
import argparse
import logging
from tqdm import tqdm
import xml.etree.ElementTree as ET

# set xattributes with subprocess call (xattr library is not working for this)
def set_xattr(file_path, country, lang):
    """
    Set 'country' and 'lang' as extended attributes for the final .json file
    using the `setfattr` command line tool.
    """
    try:
        subprocess.run(['setfattr', '-n', 'user.osmplaces.country', '-v', country, file_path], check=True, capture_output=True, text=True)
        subprocess.run(['setfattr', '-n', 'user.osmplaces.language', '-v', lang, file_path], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to set extended attribute: {e}")

# accept xml_file and output_dir args:
def parse_osm_and_save(xml_file, output_dir, alt_names, xattr, base_language):
    """
    Parse a STANDARD ouput containing nodes and write a .json file containing 
    """

    tree = ET.parse(xml_file)
    root = tree.getroot()

    country = os.path.splitext(os.path.basename(xml_file))[0]
    # initialize dict
    data_by_language = {}

    for node in tqdm(root.findall('node'), desc="Processing OSM nodes"):

        # reset nodes from previous:
        node_id = []
        lat = []
        lon = []
        lang = []
        name = []
        base_lang = []


        node_id = node.get('id')
        lat = node.get('lat')
        lon = node.get('lon')

        if base_language:
            base_lang = base_language
            try:
                for tag in node.findall('tag'):
                    key = tag.get('k')
                    if ':' in key and key.startswith(f'name:{base_lang}'):
                        base_name = tag.get('v')
            except Exception:
                pass

        for tag in node.findall('tag'):
            key = tag.get('k')
            if ':' in key and key.startswith('name:'):
                lang = key.split(':')[1]
                name = tag.get('v')

                if lang not in data_by_language:
                    data_by_language[lang] = []

                if not base_language:
                    data_by_language[lang].append({
                        'id': node_id,
                        'lat': lat,
                        'lon': lon,
                        'name': name,
                    })

                else: 
                    data_by_language[lang].append({
                        'id': node_id,
                        'lat': lat,
                        'lon': lon,
                        'name': name,
                        'base_language': base_lang,
                        'base_name': base_name 
                        })

            elif alt_names and key.startswith('alt_name:'):
                lang = key.split(':')[1]  
                alt_name = tag.get('v')

                # add alt_names if necessary: 
                if lang in data_by_language:
                    if 'alt_names' not in data_by_language[lang][-1]:
                        data_by_language[lang][-1]['alt_names'] = []
                        data_by_language[lang][-1]['alt_names'].append(alt_name)

    # make output dirs:
    os.makedirs(output_dir, exist_ok=True)

    # write json files:
    for lang, data in data_by_language.items():
        output_file_path = os.path.join(output_dir, f'{country}_places_{lang}.json')
        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        if xattr:
            os.chmod(output_file_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
            set_xattr(output_file_path, country, lang)


def main():
    parser = argparse.ArgumentParser(description='Process OSM files.')
     
    # input
    parser.add_argument('-i', '--input', required=True, help='Input OSM file path')

    # output dir
    parser.add_argument('-o', '--output', default='data', help='Output directory for JSON files')

    # keep base language
    parser.add_argument('-L', '--base-language', required=False, help='Parses each node node and keeps an additional element of each place name in the language of your choosing by ISO 639-1 Code')

    # write xattr
    parser.add_argument('-x', '--xattr', action='store_true', required=False, help='Write country/language xattributes as tag (requires files system compatible with xattributes')

    # alt names:
    parser.add_argument('-a', '--alt-names', action='store_true', required=False, help='Store alt names in each language')

    # parse args
    args = parser.parse_args()

    if args.base_language:
            base_lang = args.base_language
    
    parse_osm_and_save(args.input, args.output, args.alt_names, args.xattr, args.base_language)

if __name__ == "__main__":
    main()
