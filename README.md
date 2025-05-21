# Notion 博客导出工具

这是一个将 Notion 页面导出为 Markdown 格式的工具，支持图片处理（自动上传到 Cloudflare R2 存储）。适合用于博客内容管理、知识库导出等场景。
详细教程：https://www.chanblog.xyz/blog/20250520-1

## 功能特点

- 📄 获取 Notion 页面的标题、属性和内容
- 🖼️ 自动下载 Notion 图片并上传到 R2 存储
- 🔄 替换图片链接，解决 Notion 图片链接不稳定的问题
- 📝 转换为规范的 Markdown 格式，支持各种内容块类型
- 🚀 结构清晰的模块化设计，易于扩展
- 📁 生成的 Markdown 文档自动保存在 `doc` 文件夹下

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置说明

编辑 `config.py` 文件，配置以下内容：

### Notion 配置

```python
NOTION_TOKEN = "你的 Notion API Token"
PAGE_ID = "你要导出的页面 ID"
```

### R2 存储配置

```python
R2_ACCESS_KEY = "你的 R2 Access Key"
R2_SECRET_KEY = "你的 R2 Secret Key"
R2_BUCKET = "你的 R2 Bucket 名称"
R2_ENDPOINT = "https://你的 R2 Endpoint"
```

### 其他配置

```python
IMAGE_PREFIX = "notion_images"  # 图片在 R2 上的存储路径前缀
VERBOSE_OUTPUT = True  # 是否输出详细日志
CUSTOM_IMAGE_DOMAIN = "https://你的自定义图片域名"  # 生成的图片URL会以此为前缀
```

## 使用方法

### 基本用法

```bash
python main.py
```

默认使用 `config.py` 中配置的页面 ID。

### 指定页面 ID

```bash
python main.py --page-id 你的页面ID
```

## 项目结构

- `config.py` - 配置文件
- `main.py` - 主程序
- `notion_utils.py` - Notion API 工具模块
- `r2_utils.py` - R2 存储工具模块
- `md_converter.py` - Markdown 转换模块
- `doc/` - 自动生成的 Markdown 文档文件夹

