# markdown转图片

## 参考

https://doc.courtbouillon.org/weasyprint/stable/

https://doc.courtbouillon.org/weasyprint/stable/index.html


## 需求与实现

用python 如何实现以下需求：
将一段markdown格式的文本， 变成一张图片，文本要按格式进行渲染。

要将一段Markdown格式的文本转换成一张图片，并且确保文本按照Markdown格式进行渲染，你可以采用以下步骤：

1. 解析Markdown文本：使用Python的一个库来解析Markdown文本并将其转换为HTML。markdown库是一个不错的选择。
2. 渲染HTML到图片：将HTML转换为图片并不是一个直接的过程，
但是可以通过使用像Pillow这样的图像处理库以及weasyprint或者pyppeteer这样的工具来完成。

weasyprint可以直接将HTML转换为图像（通过先转换为PDF然后转为图像），

而pyppeteer则可以控制无头浏览器（如Chrome或Chromium）来渲染网页并将页面截图保存为图片。

下面是一个简单的例子，演示如何结合markdown和weasyprint实现这一目标：

首先，你需要安装必要的包：
```bash

pip install markdown weasyprint pillow

```

然后，你可以使用如下代码来完成任务：
```
import markdown
from weasyprint import HTML
from PIL import Image
示例Markdown文本
md_text = """
标题

这是一个段落，包含加粗和斜体文本。
列表项1
列表项2
"""
将Markdown文本转换为HTML
html_text = markdown.markdown(md_text)
使用WeasyPrint将HTML转换为PDF（中间文件）

pdf_file = 'output.pdf'
HTML(string=html_text).write_pdf(pdf_file)

使用Pillow打开PDF并转换为图片
img = Image.open(pdf_file)
rgb_img = img.convert('RGB')
output_image_path = 'output.jpg'
rgb_img.save(output_image_path)

print(f"图片已保存至 {output_image_path}")

```

注意，上述代码中，我们使用了一个中间PDF文件来从HTML过渡到图片格式。
实际上，weasyprint本身支持直接输出PNG等图片格式，但这里为了简化说明，采用了这种方式。
根据你的具体需求调整细节，例如调整输出图片的质量、大小等参数。

此外，如果需要更精确地控制页面布局或样式，可以向HTML文本中添加CSS样式。
对于更复杂的场景，考虑使用pyppeteer来进行网页截图可能会更加灵活。


```
pip install markdown weasyprint pillow

python md2png_lib.py test_md2img
```


ubuntu系统 base环境下运行报错：

```
  File "/root/anaconda3/lib/python3.9/site-packages/cffi/api.py", line 838, in accessor_function
    value = backendlib.load_function(BType, name)
AttributeError: function/symbol 'pango_context_set_round_glyph_positions' not found in library 'libpango-1.0.so.0': /usr/lib/x86_64-linux-gnu/libpango-1.0.so.0: undefined symbol: pango_context_set_round_glyph_positions

```

方案：降级版本

```
pip uninstall weasyprint

pip install "weasyprint==52.5"
```

验证：
```
from weasyprint import HTML
HTML(string="<h1>Test</h1>").write_png("test.png")
```

验证通过。


## 测试

从文件读取内容并转为PNG：
```
python md2png_lib.py test_file2png

图片已保存: output/md_20251105091745266776.png
```

使用模板转图片：
```
python md2png_lib.py test_template2png

INFO:root:正在加载markdown...
INFO:root:正在加载模板...
INFO:root:正在应用模板...
INFO:root:正在生成文件名...
INFO:root:正在生成png...
WARNING:weasyprint:Ignored `box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08)` at 20:13, unknown property.
WARNING:weasyprint:Ignored `overflow-x: auto` at 45:13, unknown property.
WARNING:weasyprint:Ignored `word-break: break-all` at 47:13, unknown property.
图片已保存: output/md_20251105094021880498.png

python src/md2png_lib.py test_template2png

```

## 开发概要

### 项目结构

```
markdown2png/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI 应用入口
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py    # API 路由定义
│   └── core/
│       ├── __init__.py
│       └── config.py    # 配置管理
├── src/
│   ├── md2png_lib.py    # Markdown转PNG核心功能
│   └── qiniu_lib.py     # 七牛云上传工具
├── template/            # 模板文件目录
│   ├── base.css         # 基础CSS样式
│   ├── base2.css
│   ├── basestyle.html
│   └── template_1.html  # HTML模板
├── output/              # 输出文件目录
├── tests/               # 单元测试目录
│   ├── test_md2png_lib.py  # 核心功能测试
│   └── test_api.py         # API接口测试
├── requirements.txt     # Python依赖
├── Dockerfile           # Docker镜像构建
├── docker-compose.yaml  # Docker Compose配置
└── readme.md            # 项目文档
```

### 技术栈

- **框架**: FastAPI 0.110.0
- **语言**: Python 3.10
- **Markdown解析**: markdown 3.3.4
- **HTML转PNG**: weasyprint 52.5
- **七牛云存储**: qiniu 7.17.0+
- **测试框架**: pytest 8.1.0

### API 接口

#### 健康检查

```
GET /api/health
```

**响应示例**:
```json
{
    "status": "ok",
    "app_name": "markdown2png",
    "version": "1.0.0"
}
```

#### Markdown转PNG

```
POST /api/markdown2png
```

**请求参数**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| md_text | string | 是 | - | Markdown文本内容 |
| isupload | boolean | 否 | false | 是否上传到七牛云存储 |
| cssfile | string | 否 | template/base.css | CSS样式文件路径 |
| template | string | 否 | "" | HTML模板文件路径 |

**请求示例**:
```json
{
    "md_text": "# 标题\n\n这是一段**加粗**文本。",
    "isupload": false,
    "cssfile": "template/base.css",
    "template": ""
}
```

**响应示例**:
```json
{
    "success": true,
    "message": "图片生成成功",
    "local_path": "output/md_20251105091745266776.png",
    "qiniu_url": null
}
```

### 本地开发

```bash
# 安装依赖
pip install -r requirements.txt

# 启动开发服务器
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 访问API文档
# http://localhost:8000/docs
# http://localhost:8000/redoc
```

### 单元测试

```bash
# 运行所有测试
python -m pytest tests/ -v

# 运行指定测试文件
python -m pytest tests/test_md2png_lib.py -v
python -m pytest tests/test_api.py -v

# 运行单个测试用例
python -m pytest tests/test_api.py::test_health_endpoint -v
```

### Docker 部署

```bash
# 构建并启动容器
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止容器
docker-compose down

# 配置七牛云环境变量（可选）
# 在 docker-compose.yaml 同目录下创建 .env 文件
# QINIU_ACCESS_KEY=your_access_key
# QINIU_SECRET_KEY=your_secret_key
```

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| QINIU_ACCESS_KEY | 七牛云Access Key | - |
| QINIU_SECRET_KEY | 七牛云Secret Key | - |
| QINIU_BUCKET_NAME | 七牛云存储桶名称 | kksaas |
| QINIU_BUCKET_DOMAIN | 七牛云存储域名 | https://up-kksaas.keyibao.com |



