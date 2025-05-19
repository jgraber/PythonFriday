import os
import sys
import shutil
import re

link_to_blog = re.compile(r'\(https://improveandrepeat.com/(.*?)\)')
year_and_title = re.compile(r'(?P<year>\d{4})/\d{2}/python-friday-(?P<title>\S+)/?')

def collector(folder: str) -> set:
    result = set()
    for root, dirs, files in os.walk(folder):
        # print(f"{root}, {dirs}, {files}")
        for dirName in dirs:
            if 'images' == dirName:
                continue
            result.add(dirName)
    # print(result)
    return result


def transform_folder(folder: str, source: str, target: str) -> None:
    print(folder)

    year = folder[0:4]
    print(f"Year: {year}")
    new_name = folder[25:]
    print(f"New name: {new_name}")

    new_folder_path = target + os.sep + year + os.sep + new_name + os.sep 
    print(f"New folder path: {new_folder_path}")

    with open(f"{source}{os.sep}{folder}{os.sep}index.md", 'r', encoding='utf-8') as file:
        post_orig = file.read()
    post_fixed = cleanup_post(post_orig)
    os.makedirs(new_folder_path)
    with open(f"{new_folder_path}{new_name}.md","w+", encoding='utf-8') as f:
        f.writelines(post_fixed)
    
    image_folder = f'{source}{os.sep}{folder}{os.sep}images'
    if os.path.isdir(image_folder):
        shutil.copytree(image_folder, new_folder_path, dirs_exist_ok=True)


def cleanup_post(input: str) -> str:
    output = []
    count_code_blocks = 0
    lines = input.split('\n')
    for line in lines:
        if line.startswith("date:"):
            line = line.replace("\"", "")
            line = f"{line} 20:00:00"
        
        if line.startswith("```"):
            if count_code_blocks % 2 == 0:
                line = line.replace("```", "``` py3")
            count_code_blocks += 1

        if line.startswith("This post is part of my"):
            line = "<!-- more -->"        

        if line.startswith("title:"):
            line = line.replace("Python Friday #", "#")

        if "(images/" in line:
            line = line.replace("(images/", "(")

        line = make_link_relative(line)
        line = make_link_relative(line)
        line = make_link_relative(line)

        output.append(line)
    full_post = "\n".join(output)
    if "<!-- more -->" not in full_post:
        full_post = full_post.replace("##", "<!-- more -->\n##", 1)

    return full_post


def make_link_relative(line):
    matches = link_to_blog.search(line)
    if matches and "/python-friday-" in matches.group(0):
        print(f"work on {matches.group(0)}")
        post_part = matches.group(1)
        parts = year_and_title.search(post_part)
        year = parts.group("year")
        title = parts.group("title")
        title = title.replace("?swcfpc=1", "")
        if ")" in title:
            title = title.replace(")", "")
        if "/" in title:
            title = title.replace("/", "")
        if "#" in title:
            title = title[:title.index("#")]
        line = line.replace(matches.group(0), f"(./../../{year}/{title}/{title}.md)")
    return line


if __name__ == "__main__":
    args = sys.argv[1:]
    source = args[0]
    target = args[1]
    print(f"transform_posts runs with {source} -> {target}")

    folders = collector(source)
    for folder in folders:
        transform_folder(folder, source, target)