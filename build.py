import json

def get_secret_properties():
    try:
        with open('./secret-properties.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: './secret-properties.json' not found.")
        raise
    except json.JSONDecodeError:
        print("Error: Could not decode JSON from './secret-properties.json'.")
        raise

def validate_secret_properties(secret_properties):
    if not isinstance(secret_properties, dict):
        return False
    return 'MLB' in secret_properties and \
           'SystemSerialNumber' in secret_properties and \
           'SystemUUID' in secret_properties

def process_replace(secret_properties):
    config_path = './EFI/OC/config.plist'
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            original_config_plist = f.read()

        replaced_config = original_config_plist.replace(
            '${{MLB}}',
            secret_properties['MLB']
        ).replace(
            '${{SystemSerialNumber}}',
            secret_properties['SystemSerialNumber']
        ).replace(
            '${{SystemUUID}}',
            secret_properties['SystemUUID']
        )

        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(replaced_config)

    except FileNotFoundError:
        print(f"Error: '{config_path}' not found.")
        raise
    except Exception as e:
        print(f"An error occurred while processing '{config_path}': {e}")
        raise

def main():
    print('getting secret properties...')
    try:
        secret_properties = get_secret_properties()
    except Exception:
        return

    print('validate secret properties...')
    if not validate_secret_properties(secret_properties):
        raise ValueError('failed to validate secret properties!')

    print('Processing replace...')
    try:
        process_replace(secret_properties)
    except Exception:
        return

    print('Successfully built config.plist!')

if __name__ == '__main__':
    main()
