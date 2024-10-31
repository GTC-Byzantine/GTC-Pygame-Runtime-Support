manifest = ['basic_class.py', 'error.py', 'basic_page.py', 'button_support.py', 'button_extensions.py',
            'progress_bar.py', 'slider.py']

with open('PRS_MAIN.py', 'w', encoding='utf-8') as f:
    f.write('import pygame\nimport os\nfrom typing import Tuple, List, Literal\npygame.init()\n')
    for item in manifest:
        with open(item, 'r', encoding='utf-8') as ff:
            lines = ff.readlines()
        in_content = False
        for line in lines:
            if line.find('#####') != -1:
                in_content = not in_content
                continue
            if in_content:
                f.write(line)
                print(line)
