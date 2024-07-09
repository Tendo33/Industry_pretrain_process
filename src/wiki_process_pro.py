import json


def clean_wiki_data(wiki_data: dict) -> dict:
    content = wiki_data['content']
    content_list = content.split('\n')
    cleaned_content = []
    skip_next = False

    for i in range(len(content_list)):
        if skip_next:
            skip_next = False
            continue

        if content_list[i].startswith('=='):

            if i + 1 < len(content_list) and content_list[i + 1].startswith('=='):
                skip_next = True
                continue
            elif i == len(content_list) - 1 or "外部连结" in content_list[i]:
                break

            cleaned_content.append(f"{content_list[i].strip('=').strip()}:")
        elif "外部连结" in content_list[i] or "参考文献" in content_list[i]:
            break
        else:

            cleaned_content.append(content_list[i].strip('*').strip())

    wiki_data['content'] = '\n'.join(cleaned_content)
    return wiki_data


def main(file_path: str, out_path: str) -> None:
    with open(file_path, 'r', encoding='utf-8') as f:
        with open(out_path, 'w', encoding='utf-8') as fw:
            for line in f:
                data = json.loads(line)
                data = clean_wiki_data(data)
                fw.write(json.dumps(data, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    file_path = r"/workspace/share_data/data/MNBVC/wiki_filter/20230198_new.jsonl"
    out_file = r"/workspace/share_data/data/MNBVC/wiki_filter/wiki_filter_01.jsonl"
    main(file_path, out_file)
