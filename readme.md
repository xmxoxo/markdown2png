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



