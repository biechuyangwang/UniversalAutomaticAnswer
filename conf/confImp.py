import yaml
def get_yaml_file(file_path):
    with open(file_path, 'r', encoding="utf-8") as f:
        file_data = f.read()
        f.close()
        return yaml.safe_load(file_data)