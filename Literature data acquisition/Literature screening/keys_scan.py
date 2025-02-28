import re
from collections import Counter
import os

def keyword_search(text, keywords):
    """
    在给定的文本中筛查关键词，并统计每个关键词的出现次数。

    参数:
        text (str): 提取的文本内容。
        keywords (list): 需要筛查的关键词列表。

    返回:
        dict: 每个关键词及其出现次数的字典。
    """
    keyword_counts = Counter()
    for keyword in keywords:
        pattern = re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE)
        matches = pattern.findall(text)
        keyword_counts[keyword] = len(matches)
    return dict(keyword_counts)

def read_file(file_path):
    """
    从文件中读取内容并返回。

    参数:
        file_path (str): 文件路径。

    返回:
        str: 文件内容。
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def save_results(results, output_file):
    """
    将关键词筛查结果保存到文件中。

    参数:
        results (dict): 文件名及其关键词出现次数的字典。
        output_file (str): 输出文件路径。
    """
    # 按关键词总次数降序排序
    sorted_results = sorted(results.items(), key=lambda x: sum(x[1].values()), reverse=True)

    with open(output_file, 'w', encoding='utf-8') as file:
        for filename, keyword_counts in sorted_results:
            total_count = sum(keyword_counts.values())
            file.write(f"文件 '{filename}'，关键词出现的总次数为：{total_count}\n")
            for keyword, count in keyword_counts.items():
                file.write(f"  关键词 '{keyword}' 出现的次数为：{count}\n")
            file.write("\n")

# 主程序
if __name__ == "__main__":
    # 指定目录
    directory = r"C:\Users\Administrator\Desktop\1"  # 文本文档所在的目录
    keywords_file_path = r"C:\Users\Administrator\Desktop\keywords.txt"  # 关键词列表文件路径
    output_file_path = r"C:\Users\Administrator\Desktop\results.txt"  # 结果保存文件路径

    # 读取关键词列表
    with open(keywords_file_path, 'r', encoding='utf-8') as file:
        keywords = [line.strip() for line in file.readlines()]

    # 初始化结果字典
    all_results = {}

    # 遍历指定目录下的所有文本文档
    for filename in os.listdir(directory):
        if filename.lower().endswith(".txt"):  # 检查是否为文本文档
            file_path = os.path.join(directory, filename)
            extracted_text = read_file(file_path)
            keyword_counts = keyword_search(extracted_text, keywords)
            all_results[filename] = keyword_counts

    # 保存结果到文件
    save_results(all_results, output_file_path)

    print(f"关键词筛查结果已保存到 {output_file_path}")