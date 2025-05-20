"""
Notion 内容导出工具主程序。
功能：将 Notion 页面导出为 Markdown 格式，并处理图片存储。
"""
import os
import argparse
from config import PAGE_ID, VERBOSE_OUTPUT
from notion_utils import get_page_info, read_page_blocks
from md_converter import to_markdown

def process_notion_page(page_id):
    """
    处理单个 Notion 页面，输出为 Markdown 文件
    
    参数:
        page_id (str): Notion 页面 ID
        
    返回:
        str: 保存的文件路径
    """
    # 1. 获取页面标题和属性
    title, properties = get_page_info(page_id)
    
    # 2. 获取页面内容块
    blocks = read_page_blocks(page_id)
    
    # 3. 转换为 Markdown
    markdown_content = to_markdown(title, properties, blocks)
    
    # 4. 保存为 Markdown 文件到 doc 文件夹
    filename = f"{title or page_id}.md"
    filename = "".join([c if c.isalnum() or c in [' ', '.', '_', '-'] else '_' for c in filename])
    doc_dir = "doc"
    os.makedirs(doc_dir, exist_ok=True)
    file_path = os.path.join(doc_dir, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    
    if VERBOSE_OUTPUT:
        print(f"已保存为 {file_path}")
    
    return file_path

def main():
    """
    主函数，处理命令行参数并执行导出
    """
    parser = argparse.ArgumentParser(description="将 Notion 页面导出为 Markdown 格式")
    parser.add_argument("--page-id", type=str, default=PAGE_ID,
                        help="Notion 页面 ID (如果不提供，则使用配置文件中的默认值)")
    
    args = parser.parse_args()
    page_id = args.page_id
    
    try:
        output_file = process_notion_page(page_id)
        print(f"✅ 转换完成！Markdown 文件保存为：{output_file}")
    except Exception as e:
        print(f"❌ 转换失败：{e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 