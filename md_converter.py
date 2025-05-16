"""
Markdown 转换模块。
将 Notion 内容转换为 Markdown 格式。
"""
from r2_utils import process_image
from notion_utils import extract_plain_text

def properties_to_markdown(properties):
    """
    将属性字典转为Markdown格式的字符串
    
    参数:
        properties (dict): Notion属性字典
        
    返回:
        str: Markdown格式的属性文本
    """
    lines = []
    for key, value in properties.items():
        try:
            if value["type"] == "rich_text":
                text = "".join([t.get("plain_text", "") for t in value["rich_text"]])
                lines.append(f"- {key}: {text}")
            elif value["type"] == "select":
                lines.append(f"- {key}: {value['select']['name'] if value['select'] else ''}")
            elif value["type"] == "multi_select":
                lines.append(f"- {key}: {', '.join([v['name'] for v in value['multi_select']])}")
            elif value["type"] == "date":
                lines.append(f"- {key}: {value['date']['start'] if value['date'] else ''}")
            # 其他类型可以根据需要添加
        except Exception as e:
            lines.append(f"- {key}: (解析错误: {e})")
    return "\n".join(lines)

def block_to_markdown(block):
    """
    将单个内容块转为Markdown格式
    
    参数:
        block (dict): Notion内容块
        
    返回:
        str: Markdown格式的文本
    """
    block_type = block["type"]
    content = extract_plain_text(block)
    
    if block_type == "paragraph":
        return content
    elif block_type == "heading_1":
        return f"# {content}"
    elif block_type == "heading_2":
        return f"## {content}"
    elif block_type == "heading_3":
        return f"### {content}"
    elif block_type == "bulleted_list_item":
        return f"- {content}"
    elif block_type == "numbered_list_item":
        return f"1. {content}"
    elif block_type == "to_do":
        return f"- [ ] {content}"  # 未勾选的待办项
    elif block_type == "image":
        # 处理图片：下载并上传到R2
        r2_url = process_image(content)
        return f"![图片]({r2_url})"
    elif block_type == "code":
        # 假设code块有语言类型
        code_lang = block.get("code", {}).get("language", "")
        return f"```{code_lang}\n{content}\n```"
    elif block_type == "quote":
        return f"> {content}"
    elif block_type == "divider":
        return "---"
    else:
        # 不认识的块类型，加上标记
        return f"<!-- {block_type} -->\n{content}"

def to_markdown(title, properties, blocks):
    """
    将整个页面转为Markdown字符串，自动处理段落空行和列表连续性
    
    参数:
        title (str): 页面标题
        properties (dict): 页面属性
        blocks (list): 内容块列表
        
    返回:
        str: Markdown格式的完整文档
    """
    md_lines = []
    
    # 添加标题
    md_lines.append(f"# {title}\n")
    
    # 添加属性
    if properties:
        md_lines.append(properties_to_markdown(properties))
        md_lines.append("")  # 空行
    
    prev_block_type = None
    
    # 添加内容块
    for block in blocks:
        block_type = block["type"]
        md = block_to_markdown(block)
        
        if not md.strip():
            continue
            
        # 判断是否需要空行
        if prev_block_type is not None:
            # 这些块类型之间不需要空行
            continuous_types = [
                ("bulleted_list_item", "bulleted_list_item"),
                ("numbered_list_item", "numbered_list_item"),
                ("heading_1", None),  # 标题后不加空行
                ("heading_2", None),  # 标题后不加空行
                ("heading_3", None),  # 标题后不加空行
                (None, "heading_1"),  # 标题前不加空行 
                (None, "heading_2"),  # 标题前不加空行
                (None, "heading_3"),  # 标题前不加空行
            ]
            
            if (prev_block_type, block_type) not in continuous_types and (prev_block_type, None) not in continuous_types and (None, block_type) not in continuous_types:
                md_lines.append("")
        
        md_lines.append(md)
        prev_block_type = block_type
    
    return "\n".join(md_lines) 