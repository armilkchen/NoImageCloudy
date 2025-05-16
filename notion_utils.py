"""
Notion API 工具模块。
负责从 Notion 获取页面信息、内容块等数据。
"""
from notion_client import Client
from config import NOTION_TOKEN, VERBOSE_OUTPUT

# 初始化 Notion 客户端
notion = Client(auth=NOTION_TOKEN)

def get_page_info(page_id):
    """
    获取 Notion 页面的标题和属性
    
    参数:
        page_id (str): Notion 页面 ID
        
    返回:
        tuple: (标题, 属性字典)
    """
    try:
        if VERBOSE_OUTPUT:
            print(f"正在获取页面信息: {page_id}")
        page_info = notion.pages.retrieve(page_id)
        properties = page_info.get("properties", {})
        title = ""
        # 查找标题属性
        for prop in properties.values():
            if prop.get("type") == "title":
                title = "".join([t.get("plain_text", "") for t in prop["title"]])
        if VERBOSE_OUTPUT:
            print(f"页面标题: {title}")
        return title, properties
    except Exception as e:
        print(f"获取页面信息失败: {e}")
        return "(未知标题)", {}

def extract_plain_text(block):
    """
    从块中提取纯文本内容
    
    参数:
        block (dict): Notion 内容块
        
    返回:
        str: 提取的文本内容
    """
    block_type = block["type"]
    if "rich_text" in block[block_type]:
        texts = block[block_type]["rich_text"]
        return "".join(t.get("plain_text", "") for t in texts)
    elif block_type == "image":
        if block["image"]["type"] == "file":
            return block["image"]["file"]["url"]
        elif block["image"]["type"] == "external":
            return block["image"]["external"]["url"]
    return "(无内容)"

def read_page_blocks(page_id):
    """
    获取页面下所有内容块
    
    参数:
        page_id (str): Notion 页面 ID
        
    返回:
        list: 内容块列表
    """
    results = []
    cursor = None
    if VERBOSE_OUTPUT:
        print(f"正在获取页面内容块: {page_id}")
    while True:
        response = notion.blocks.children.list(block_id=page_id, start_cursor=cursor)
        results.extend(response['results'])
        if not response.get('has_more'):
            break
        cursor = response.get('next_cursor')
    if VERBOSE_OUTPUT:
        print(f"获取到 {len(results)} 个内容块")
    return results 