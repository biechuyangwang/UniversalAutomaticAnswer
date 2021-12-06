import yaml
def get_yaml_file(file_path):
    with open(file_path, 'r', encoding="utf-8") as f:
        file_data = f.read()
        f.close()
        return yaml.safe_load(file_data)

if __name__ == '__main__':
    conf_data = get_yaml_file('./conf.yml')
    imgpath = conf_data['path']['imgpath']
    print(imgpath)
