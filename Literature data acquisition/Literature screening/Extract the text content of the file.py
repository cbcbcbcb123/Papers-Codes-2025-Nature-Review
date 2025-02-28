import fitz  # PyMuPDF
import os

def extract_text_from_pdf(pdf_path, output_text_path):
    """
    提取PDF文件中的文字内容并保存到文本文件
    """
    document = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text() + "\n"

    # 保存提取的文字内容到文本文件
    with open(output_text_path, "w", encoding="utf-8") as text_file:
        text_file.write(text)

    print(f"文字内容已保存到：{output_text_path}")

def extract_text_from_all_pdfs(directory):
    """
    遍历指定目录下的所有PDF文件，并提取文字内容保存到文本文件
    """
    # 遍历指定目录
    for filename in os.listdir(directory):
        if filename.lower().endswith(".pdf"):  # 检查是否为PDF文件
            pdf_path = os.path.join(directory, filename)
            # 生成输出文本文件的路径
            output_text_path = os.path.join(directory, filename.replace(".pdf", ".txt"))
            # 提取文字内容并保存
            extract_text_from_pdf(pdf_path, output_text_path)

# 使用示例
directory = r"C:\Users\Administrator\Desktop\1"  # 指定目录
extract_text_from_all_pdfs(directory)