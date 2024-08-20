import re
import json
import jionlp
from cutword import NER
from tqdm import tqdm

h2 = [
    "一、",
    "二、",
    "三、",
    "四、",
    "五、",
    "六、",
    "七、",
    "八、",
    "九、",
    "十、",
    "十一、",
    "十二、",
    "十三、",
    "十四、",
    "十五、",
    "十六、",
    "十七、",
    "十八、",
    "十九、",
    "二十、",
    "二十一",
    "二十二",
    "二十三",
    "二十四",
    "二十五",
    "二十六",
    "二十七",
    "二十八",
    "二十九",
    "三十",
]
h3 = [
    "（一）",
    "（二）",
    "（三）",
    "（四）",
    "（五）",
    "（六）",
    "（七）",
    "（八）",
    "（九）",
    "（十）",
    "（十一）",
    "（十二）",
    "（十三）",
    "（十四）",
    "（十五）",
    "（十六）",
    "（十七）",
    "（十八）",
    "（十九）",
    "（二十）",
    "（二十一）",
    "（二十二）",
    "（二十三）",
    "（二十四）",
    "（二十五）",
    "（二十六）",
    "（二十七）",
    "（二十八）",
    "（二十九）",
    "（三十）",
]
h4 = [
    "1.",
    "2.",
    "3.",
    "4.",
    "5.",
    "6.",
    "7.",
    "8.",
    "9.",
    "10.",
    "11.",
    "12.",
    "13.",
    "14.",
    "15.",
    "16.",
    "17.",
    "18.",
    "19.",
    "20.",
    "21.",
    "22.",
    "23.",
    "24.",
    "25.",
    "26.",
    "27.",
    "28.",
    "29.",
    "30.",
]


def to_html(content: str = "") -> str:
    outlines = list(map(str, content.split("\n")))
    result_html = ""
    h2 = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]
    outlines = [outline.strip() for outline in outlines]
    special_starting_sentences = [
        outline
        for outline in outlines
        if outline.startswith("（") and "）" in outline
    ]
    flag = all(len(sentence) < 20 for sentence in special_starting_sentences)

    for outline in outlines:
        outline = outline.strip()
        if not outline:
            continue
        if "（" == outline[0] and "）" in outline:
            # 拿到括号中间内容
            content_in_parentheses = outline.split("（")[1].split("）")[0]
            # 检查括号中间的内容是否都在h2里面，所有三级标题的长度是否小于20
            if all(num in h2 for num in content_in_parentheses) and flag:
                result_html += f"<h3>{outline}</h3>"
            else:
                result_html += f"<p>{outline}</p>"
        elif all(num in h2 for num in outline.split("、")[0]):
            result_html += f"<h2>{outline}</h2>"
        else:
            result_html += f"<p>{outline}</p>"

    return result_html


def dis_html(text: str) -> str:
    # 把html 标签转换成\n，返回的一个str
    pattern = re.compile(r"<[^>]+>", re.S)
    result = pattern.sub("", text)
    res = result.replace("\n\n", "\n")
    res = res.strip()
    return res.strip("\n")


def full_to_half(text: str) -> str:
    result = ""
    for char in text:
        code = ord(char)
        if code == 0x3000:
            code = 0x20
        elif 0xFF01 <= code <= 0xFF5E:
            code -= 0xFEE0
        result += chr(code)
    return result


def clean_special_char(text: str) -> str:
    special_chars = [
        "①",
        "②",
        "③",
        "④",
        "⑤",
        "⑥",
        "⑦",
        "⑧",
        "⑨",
        "⑩",
        "⑪",
        "⑫",
        "⑬",
        "⑭",
        "",
        "...",
        "…",
        "◆",
        "二OO",
        "?D",
        "√",
    ]
    for special_char in special_chars:
        text = text.replace(special_char, "")
    return text


def remove_content_with_pattern(text: str, pattern: str) -> str:
    return re.sub(pattern, "", text)


def replace_content_with_pattern(text: str, pattern: str, new_text: str) -> str:
    return re.sub(pattern, new_text, text)


def remove_space(text: str) -> str:
    lines = text.split("\n")
    cleaned_lines = []

    for i, line in enumerate(lines):
        if i < 3 and "各" in line:
            continue

        if any(
            line.startswith(prefix)
            for prefix in [
                "附件:",
                "附件：",
                "附：",
                "政策解读：",
                "[文件下载]",
                "AQI说明",
                "扫一扫",
                "公文相关附件",
            ]
        ):
            break

        if any(
            keyword in line
            for keyword in ["MsoNormal", "Generator", "Section", "font"]
        ):
            continue

        if any(
            keyword in line
            for keyword in [
                ".doc",
                ".pdf",
                ".xls",
                ".docx",
                ".xlsx",
                ".md",
                ".wps",
                ".PDF",
                "（Word版）",
                "（pdf版）",
                "（PDF版）",
                "（word版）",
            ]
        ):
            continue

        if len(line) < 4 and not any(line.startswith(h) for h in h2 + h3 + h4):
            continue

        line = line.strip()

        line = re.sub(r"\s+", "", line)

        cleaned_lines.append(line)
    cleaned_string = "\n".join(cleaned_lines)
    return cleaned_string


def replace_special_char(text: str) -> str:
    replacements = {
        "?": ".",
        "\n\n": "\n",
        "\t": "",
        "\n.\n": ".",
        "㈠": "（一）",
        "㈡": "（二）",
        "㈢": "（三）",
        "㈣": "（四）",
        "㈤": "（五）",
        "㈥": "（六）",
        "㈦": "（七）",
        "㈧": "（八）",
        "㈨": "（九）",
        "㈩": "（十）",
        "【": "[",
        "】": "]",
        "xxxx年xx月xx日xxxx年xx月xx日": "xxxx年xx月xx日",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def remove_data_info(text: str) -> str:
    # r'\d{1,2}月.{1,2}日',r'\d{1,4}年',
    patterns = [
        r"\d{4}\.\d{1,2}\.\d{1,2}",
        r"\d{1,4}年.{1,2}月.{1,2}日",
        r"\d{1,4}[/-].{1,2}[/-].{1,2}",
        r"[○〇零一二三四五六七八九]{1,4}年[○〇零一二三四五六七八九十]{1,3}月[○〇零一二三四五六七八九十]{1,3}日",
        r"[○〇零一二三四五六七八九]{1,4}年",
        r"[○〇零一二三四五六七八九十]{1,3}月[○〇零一二三四五六七八九十]{1,3}日",
    ]

    lines = text.split("\n")
    new_text = []

    for line in lines:
        for pattern in patterns:
            line = line.strip()
            if re.fullmatch(pattern, line):
                line = "xxxx年xx月xx日"
                break
            line = re.sub(pattern, "xxxx年xx月xx日", line)
        new_text.append(line)

    return "\n".join(new_text)


def remove_person_name(text: str) -> str:
    """
    去除文本中的人名
    Args:
        text (str): 输入的文本
    Returns:
        str: 处理后去除人名的文本
    """
    # 需要排除的人名列表
    name_list = [
        "李克强",
        "习近平",
        "李强",
        "王毅",
        "王沪宁",
        "王岐山",
        "王晨",
        "王勇",
        "邓小平",
        "习近平总书记",
        "毛泽东",
        "周恩来",
        "刘少奇",
        "朱德",
        "彭德怀",
        "林彪",
        "刘伯承",
        "陈毅",
        "罗荣桓",
        "徐向前",
        "聂荣臻",
        "叶剑英",
        "胡锦涛",
        "江泽民",
        "张德江",
        "俞正声",
        "刘云山",
        "张高丽",
        "栗战书",
        "汪洋",
        "韩正",
        "赵乐际",
        "胡春华",
        "郭声琨",
        "黄坤明",
        "蔡奇",
        "丁薛祥",
        "刘鹤",
        "杨洁篪",
        "栗战书",
        "王沪宁",
        "李鸿忠",
        "杨晓渡",
        "赵克志",
        "李希",
        "陈全国",
        "韩正",
        "汪洋",
        "刘鹤",
        "陈敏尔",
        "陈希",
        "胡春华",
        "蔡奇",
        "赵乐际",
    ]
    ner = NER()
    try:
        res = ner.predict(text, return_words=False)
        if not res or not res[0]:
            return text
        res = res[0]
    except Exception as e:
        return text

    for word in res:
        if word.ner_type_zh == "人名" and word.entity not in name_list:
            text = text.replace(word.entity, "XXX")

    return text


def new_base_clean(content_list: list[str]) -> list[str]:
    # 定义正则表达式
    patterns = [r"\(.*?〔\d+〕.*?\)", r"\（.*?〔\d+〕.*?\）", r"〔.*?〕"]
    replace_pattern = r"星期[一二三四五六日]{1}"

    for i, content in enumerate(content_list):
        # 基础清洗
        content = full_to_half(content)
        content = jionlp.clean_text(
            content,
            remove_email=False,
            remove_phone_number=False,
            remove_url=False,
            remove_parentheses=False,
            delete_prefix=True,
        )
        content = jionlp.replace_phone_number(content, token="xxx")
        content = jionlp.replace_email(content, token="xxxxx")
        content = jionlp.replace_url(content, token="xxxxxxxxx")
        content = remove_data_info(content)
        content = clean_special_char(content)
        content = remove_space(content)

        # 去除所有的 (xx〔xxx〕xx)"的内容
        for pattern in patterns:
            content = remove_content_with_pattern(content, pattern)
        content = replace_content_with_pattern(
            content, replace_pattern, "星期X"
        )
        content = replace_special_char(content).strip("\n").strip()

        # content = remove_unpaired_brackets(content)
        content_list[i] = content
    return content_list


def outline_clean(content_list: list[str]) -> list[str]:
    for i, content in enumerate(content_list):
        # 基础清洗
        content = jionlp.clean_text(
            content,
            remove_email=False,
            remove_phone_number=False,
            remove_url=False,
            remove_parentheses=False,
            delete_prefix=True,
        )
        content = content.strip()
        content_list[i] = content
    return content_list


def title_clean(content_list: list[str]) -> list[str]:
    # 定义正则表达式
    pattern = r"\(.*?〔\d+〕.*?\)"
    pattern2 = r"\（.*?〔\d+〕.*?\）"
    pattern3 = r"〔.*?〕"

    for i, content in enumerate(content_list):
        # 基础清洗
        content = jionlp.clean_text(
            content,
            remove_email=False,
            remove_phone_number=False,
            remove_url=False,
            remove_parentheses=False,
            delete_prefix=True,
        )
        content = jionlp.remove_parentheses(content, parentheses="【】")
        content = clean_special_char(content)
        content = remove_space(content)

        # 去除所有的(xx〔xxx〕xx)"的内容
        content = remove_content_with_pattern(content, pattern)
        content = remove_content_with_pattern(content, pattern2)
        content = remove_content_with_pattern(content, pattern3)
        # content = remove_unpaired_brackets(content)
        content = content.strip("#").strip("\n").strip()
        content_list[i] = content
    return content_list


def pretrain_base_clean(content_list: list[str]) -> list[str]:
    for i, content in enumerate(content_list):
        # 基础清洗
        content = dis_html(content)
        content = full_to_half(content)
        content = jionlp.clean_text(
            content,
            remove_email=False,
            remove_phone_number=False,
            remove_url=False,
            remove_parentheses=False,
            delete_prefix=True,
        )
        content = jionlp.replace_phone_number(content, token="xxx")
        content = jionlp.replace_email(content, token="xxxxx")
        content = jionlp.replace_url(content, token="xxxxxxxxx")

        content = clean_special_char(content)

        content = replace_special_char(content).strip("\n").strip()

        # content = remove_unpaired_brackets(content)
        content_list[i] = content
    return content_list


def remove_duplicates(input_file: str, output_file: str):
    # 匹配除了中文字符（包括标点符号）
    pattern = r"[^\u4e00-\u9fa5，《》<>\"\']+"
    seen_entries = set()

    with open(input_file, "r", encoding="utf-8") as f_in:
        with open(output_file, "w", encoding="utf-8") as f_out:
            for line in tqdm(f_in, desc="去重中..."):
                data = json.loads(line)
                title = data.get("title", "")
                title = jionlp.remove_parentheses(
                    title, parentheses="〔〕()（）【】"
                )
                title = title.strip("#").strip()
                title_clean = re.sub(pattern, "", title)
                if (
                    title_clean not in seen_entries
                    and "任免" not in title
                    and "任命" not in title
                    and "免去" not in title
                    and "聘任" not in title
                    and "续聘" not in title
                    and "解聘" not in title
                    and "小组" not in title
                    and "挂职" not in title
                ):
                    seen_entries.add(title_clean)
                    f_out.write(json.dumps(data, ensure_ascii=False) + "\n")
