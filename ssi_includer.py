import re
import shutil
import os

virtual_root_directory = 'public_site'.replace('\\', '/')


def get_all_files_in_dir(dir):
    ls = []
    for i in os.listdir(dir):
        if os.path.isdir(f'{dir}\\{i}'):
            # print(f'Переходим в папку: {i}')
            res = get_all_files_in_dir(f'{dir}\\{i}')
            if bool(res):
                files = get_all_files_in_dir(f'{dir}\\{i}')
                for f in files:
                    ls.append(f)
        else:
            if i.endswith('.shtml'):
                ls.append(f'{dir}\\{i}')

    return ls

print(get_all_files_in_dir('public_site'))




def update_public_site():
    source_dir = 'site_code'
    destination_dir = 'public_site'

    shutil.rmtree(destination_dir)
    shutil.copytree(source_dir, destination_dir)


def get_sourse_of_file(path_and_file, ssi_type='virtual'):
    path_and_file.replace('\\', '/')
    if ssi_type == 'file':
        path_from_curr_file = path_and_file.split('/')[:-1]
        file_name = path_and_file.split('/')[-1]
        path_from_curr_file = '/'.join(path_from_curr_file)
        # print('path: ' + path_from_curr_file)
        path_as_virtual = f'{virtual_root_directory}/{path_from_curr_file}/{file_name}'
        end_path = path_as_virtual

    elif ssi_type == 'virtual':
        if path_and_file.startswith('/'):
            path_and_file = f'{virtual_root_directory}{path_and_file}'
        end_path = path_and_file

    else:
        print(ssi_type)
        assert False
    file = open(f'{end_path}', 'r')
    sourse = file.read()
    file.close()

    # print('FileNotFoundError')
    # sourse = '[SSI_python: FileNotFoundError]'

    return f'{sourse}'


def convert_ssi_in_text(text, virtual_root_directory=None):
    pattern = '<!-- *# *include* (file|virtual) *= *"([^(-->)]*)" *-->'
    while re.search(pattern, text):
        result = re.search(pattern, text)

        if result:
            start, stop = result.span()
            inc_type = result.group(1)
            inc_file = result.group(2)
            sourse = get_sourse_of_file(inc_file, inc_type)
            text = text[:start] + f'{sourse}' + text[stop:]
    return text


def convert_ssi_in_file(path):
    with open(path, 'r+') as file:
        sourse = file.read()
        with open(path, 'w'):
            pass
        converted_sourse = convert_ssi_in_text(sourse, virtual_root_directory)
        file.write(str(converted_sourse))


def main():
    update_public_site()
    shtml_files_pathes = get_all_files_in_dir('public_site')
    for path_and_file in shtml_files_pathes:
        print(f"trying convert: {path_and_file}")
        convert_ssi_in_file(path_and_file)


if __name__ == "__main__":
    main()
