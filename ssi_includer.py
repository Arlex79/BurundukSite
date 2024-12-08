import re

virtual_root_directory = 'site_code'.replace('\\', '/')


def get_sourse_of_file(path, ssi_type='virtual'):
    path.replace('\\', '/')
    if ssi_type == 'virtual':

        if path.startswith('/'):
            print('ggg')
            path = f'{virtual_root_directory}{path}'
    try:
        file = open(f'{path}', 'r')
        sourse = file.read()
        file.close()
    except FileNotFoundError:
        print('FileNotFoundError')
        sourse = '[SSI_python: FileNotFoundError]'


    return f'{sourse}'


def convert_ssi_in_text(text, virtual_root_directory=None):
    pattern = '<!-- *# *(file|virtual) *= *"([^(-->)]*)" *-->'
    while re.search(pattern, text):
        result = re.search(pattern, text)

        if result:
            pass
            # mm = result.group(1)
            # dd = result.group(2)
            # yyyy = result.group(3)
            # new_date = dd + '/' + mm + '/' + yyyy
            # start, stop = result.span()

            start, stop = result.span()
            inc_type = result.group(1)
            inc_file = result.group(2)
            sourse = get_sourse_of_file(inc_file, inc_type)
            text = text[:start] + f'{sourse}' + text[stop:]
            print(f'Find at: {start}:{stop}')
            # print(result.group(1))
    return text


if __name__ == "__main__":
    text = 'HTML_<!--#virtual="/includes/header.inc"-->_page_<!--#virtual="/includes/header.inc"-->_endofpage'
    print(f'Result: {convert_ssi_in_text(text)}')
