from collections import Counter
import re


# 判断大纲序号是否为递增序列
def is_increasing(numerical_list: list[int]) -> bool:
    numerical_list.insert(0, 0)  # 在序列开头插入0，以便比较第一个数字
    for i in range(len(numerical_list) - 1):
        # 判断数字序列是否递增
        if (
            numerical_list[i + 1] - numerical_list[i] != 1
            and numerical_list[i + 1] != 1
        ):
            return False
    return True


# 筛选出符合大纲的正文,返回正文和标题
def extract_outlines_files(
    content_list: list[str], title_list: list[str]
) -> tuple[list[str], list[str]]:
    # 存储清洗后的内容列表
    cleaned_content_list = []
    # 存储清洗后的标题列表
    cleaned_title_list = []

    # 定义需要匹配的标题格式
    title_1 = "一、二、三、四、五、六、七、八、九、十、十一、十二、十三、十四、"
    title_2 = "（一）（二）（三）（四）（五）（六）（七）（八）（九）（十）（十一）（十二）（十三）（十四）"
    title_3 = "0.1.2.3.4.5.6.7.8.9.10.12.11.13.14.15.16."
    bad_case = "0、1、2、3、4、5、6、7、8、9、10、11、13、12、14、15、16、"

    # 遍历内容列表
    for index in range(len(content_list)):
        title_count = 0  # 标题计数器
        is_valid = True  # 标记是否符合条件
        numerical_list = []  # 存储特定格式的数字
        line_count = 0  # 行数计数器

        # 去掉过长或过短的内容
        if len(content_list[index]) < 100 or len(content_list[index]) > 20000:
            continue
        # 遍历每一行内容
        for line in content_list[index].split("\n"):
            # 检查是否存在不良情况
            if line[:2] in bad_case:
                is_valid = False
                break
            # 检查是否符合中文数字标题格式
            if line[:2] == "一、":
                title_count += 1
                if line_count > 7:
                    is_valid = False
                    break
            # 检查是否符合其他标题格式
            if line[:2] in title_1:
                if len(line.split("。")[0]) > 35:
                    is_valid = False
                    break
            # 检查是否符合数字序列格式
            if line[:2] in title_3:
                if len(line.split("。")[0]) * 3 > len(line):
                    is_valid = False
                    break
                numerical_list.append(int(line[0]))
            line_count += 1
        # 检查是否符合特定条件并调用is_increasing函数
        if title_count == 1 and is_valid and is_increasing(numerical_list):
            cleaned_content_list.append(content_list[index])
            # 将对应的标题添加到标题列表中
            cleaned_title_list.append(title_list[index])
    return cleaned_content_list, cleaned_title_list


# 从正文中提取大纲，返回每一篇文章的大纲
def extract_outlines(content_list: list[str]) -> list[str]:
    all_outlines = []

    title_1 = "一、二、三、四、五、六、七、八、九、十、十一、十二、十三、十四、"
    title_2 = "（一）（二）（三）（四）（五）（六）（七）（八）（九）（十）（十一）（十二）（十三）（十四）"
    title_3 = "0.1.2.3.4.5.6.7.8.9.10.12.11.13.14.15.16."

    for i, content in enumerate(content_list):
        temp = []
        line_list = content.split("\n")
        for line in line_list:
            # 判断是否为标题类型1
            if line[:2] in title_1:
                if line and len(line.split("。")[0]) < 35:
                    temp.append(line.split("。")[0].strip())
                continue
            # 判断是否为标题类型2
            if line.split("。")[0][:3] in title_2:
                if line.split("。")[0] and len(line.split("。")[0]) < 35:
                    temp.append(line.split("。")[0].strip())
                continue
        all_outlines.append("\n".join(temp))
    return all_outlines


def extract_outlines_new(content_list: list[str]) -> list[str]:
    all_outlines = []
    level_two_pattern = re.compile(r"^[一二三四五六七八九十百]+、")
    level_thr_pattern = re.compile(r"（[一二三四五六七八九十百]+）")

    for i, content in enumerate(content_list):
        content = content.split("\n")
        content = list(filter(lambda item: item != "", content))

        output_dagang = [
            element.strip()
            for element in content
            if level_two_pattern.match(element)
            or level_thr_pattern.search(element)
        ]
        output_dagang = [
            re.split("。|：|，|；", element) for element in output_dagang
        ]
        output_dagang = [
            part for element in output_dagang for part in element if part
        ]
        # 去除所有文字，只保留大纲
        output_dagang = [
            element
            for element in output_dagang
            if level_two_pattern.match(element)
            or level_thr_pattern.search(element)
        ]

        all_outlines.append("\n".join(output_dagang))
    return all_outlines


def extract_policy_files(
    content_list: list[str], title_list: list[str]
) -> list[str]:
    input_policy = []
    for i, content in enumerate(content_list):
        policies = re.findall(r"《(.*?)》", content)
        policies = list(set(policies))
        if i < len(title_list):
            title = title_list[i]
            policies = [policy for policy in policies if policy != title]

        input_policy.append(
            "\n".join(["《" + line + "》" for line in policies])
        )
    return input_policy


# 中文数到整数的映射
cn_num_map = {
    "零": 0,
    "一": 1,
    "二": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
    "十": 10,
    "百": 100,
    "千": 1000,
    "万": 10000,
}


def cn_num_to_arabic(cn_num):
    # 将中文数字转换成阿拉伯数字
    if cn_num in cn_num_map:
        return cn_num_map[cn_num]

    num = 0
    if "十" in cn_num:
        idx = cn_num.index("十")
        if idx == 0:
            num += 10
        else:
            num += cn_num_map[cn_num[idx - 1]] * 10
        if idx < len(cn_num) - 1:
            num += cn_num_map[cn_num[idx + 1]]
    return num


def validate_outline(text: str) -> bool:
    # 分割文本到行，并移除空行
    text = text.strip()
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    if len(lines) == 0 or not text.startswith("一、"):
        return False
    title1_is_ok = True
    title2_case1_is_ok = True
    title2_case2_is_ok = True

    outline_is_ok = True

    # 初始化上一个标题的阿拉伯数字序号
    last_lvl_1_num = 0
    last_lvl_2_num = 0

    # 二级标题序号
    lvl_2_nums = []

    for line in lines:
        # 检测一级标题
        lvl_1_match = re.match(r"^([一二三四五六七八九十]+)、", line)
        if lvl_1_match:
            lvl_1_num = cn_num_to_arabic(lvl_1_match.group(1))
            if lvl_1_num > last_lvl_1_num + 1 or lvl_1_num < last_lvl_1_num:
                print(f"一级标题序号跳跃： {line}")

                title1_is_ok = False
                outline_is_ok = False

            last_lvl_1_num = lvl_1_num
            last_lvl_2_num = 0  # 当检测到一个新的一级标题时重置二级标题序号
            continue

        # 检测二级标题
        lvl_2_match = re.match(r"^（([一二三四五六七八九十]+)）", line)
        if lvl_2_match:
            lvl_2_num = cn_num_to_arabic(lvl_2_match.group(1))
            if lvl_2_num > last_lvl_2_num + 1 or lvl_2_num < last_lvl_2_num:
                # print(f"二级标题序号跳跃： {line}")
                title2_case1_is_ok = False
            last_lvl_2_num = lvl_2_num
            lvl_2_nums.append(lvl_2_num)
            continue

    # 检查二级标题的第二种情况
    if title1_is_ok:
        if lvl_2_nums:
            title2_case2_is_ok = lvl_2_nums[0] == 1

            # 检查列表元素是否按顺序递增
            for i in range(1, len(lvl_2_nums)):
                if lvl_2_nums[i] != lvl_2_nums[i - 1] + 1:
                    title2_case2_is_ok = False
                    break

    outline_is_ok = title1_is_ok and (title2_case1_is_ok or title2_case2_is_ok)
    return outline_is_ok


def has_duplicates(input_list: list) -> bool:
    """
    判断列表中是否有重复元素，并打印出重复的值
    :param input_list: 需要检查的列表
    :return: 如果有重复元素返回True，否则返回False
    """
    # 使用Counter统计每个元素出现的次数
    element_counts = Counter(input_list)

    # 用于记录重复的值
    duplicates = []

    # 遍历统计结果，如果有元素出现次数大于1，则表示有重复
    for element, count in element_counts.items():
        if count > 1:
            duplicates.append(element)

    # 如果存在重复元素，打印出重复的值
    if duplicates:
        print("重复的值：", duplicates)
        return True
    else:
        return False
