import os
import fitz  # PyMuPDF库用于处理PDF文件
from collections import defaultdict


def main():
    current_dir = os.getcwd()
    target_folder_path = os.path.join(current_dir, "target_folder_path")  # 您需要修改的目标文件夹路径

    keywords_input = input("请输入由关键词组成的布尔表达式（如：'AI OR machine learning'）：")

    filepaths = []
    for dirpath, dirnames, filenames in os.walk(target_folder_path):
        filepaths.extend([os.path.join(dirpath, f) for f in filenames])

    keywords = keywords_input.strip().split()

    keyword_counts = defaultdict(int)

    total_keywords = []
    for file_path in filepaths:
        try:
            with open(file_path, 'rb') as f:
                doc = fitz.open(f, loadsalts=True)

                text = ""
                for page in doc:
                    text += page.get_text() + "\n"

                contains_keywords = False
                for keyword in keywords:
                    if keyword.lower() in text.lower():
                        keyword_counts[keyword] += 1
                        contains_keywords = True
                        break

                if contains_keywords:
                    total_keywords.append({
                        "filename": os.path.basename(file_path),
                        "total_keywords": sum(keyword_counts.values())
                    })
        except Exception as e:
            print(f"错误处理文件：{file_path}\n原因：{e}")

    if not total_keywords:
        print("没有找到符合条件的PDF文件。")
    else:
        sorted_total_keywords = sorted(total_keywords, key=lambda x: -x["total_keywords"])

        for item in sorted_total_keywords:
            print(f"{item['filename']}：关键词总数为 {item['total_keywords']}")
            for keyword, count in keyword_counts.items():
                if count > 0 and hasattr(item, 'keywords'):
                    print(f"    关键词 '{keyword}' 出现 {count} 次")
            print()


if __name__ == "__main__":
    main()
