#!/usr/bin/env python3
#coding:utf-8

'''
__author__ = 'xmxoxo<xmxoxo@qq.com>'
'''


import asyncio
import logging
import os
import base64
import textwrap
import random
import time
import markdown
from playwright.async_api import async_playwright

def rand_filename(path="", pre="", ext=""):
    """按时间戳生成文件名，并自动创建目录"""
    nowtime = time.time()
    fmttxt = time.strftime("%Y%m%d%H%M%S", time.localtime(nowtime))
    dtime = int((nowtime - int(nowtime)) * 1000)
    rndnum = random.randint(100, 999)
    filename = f"{pre}{fmttxt}{dtime:03d}{rndnum:03d}{ext}"
    if path:
        mkfold(path)
    fname = os.path.join(path, filename)
    return fname


def mkfold(new_dir):
    '''创建目录，支持多级子目录'''
    try:
        if new_dir == '':
            return False
        if not os.path.exists(new_dir):
            os.makedirs(new_dir, exist_ok=True)
        return True
    except Exception:   # pylint: disable=broad-exception-caught
        return False

def readtxt(fname, encoding='utf-8'):
    ''' 读入文件'''
    try:
        with open(fname, 'r', encoding=encoding) as fobj:
            data = fobj.read()
        return data
    except (FileNotFoundError, PermissionError, UnicodeDecodeError, OSError) as err:
        logging.error("无法读取文件 %s: %s", fname, err)
        return ''

def md2html(md_text:str, cssfile:str="template/base.css", template_file:str=""):
    '''markdown转为HTML
    md_text:        Markdown文本内容
    cssfile:        CSS样式文件路径
    template_file： 模板文件路径
    '''
    # 默认的最简洁的模板
    page_html = """
    <html><head><meta charset="utf-8" />
    <style>{css}</style>
    </head>
    <body>
     {html}
    </body>
    </html>
    """
    page_html = textwrap.dedent(page_html)
    # markdown转为HTML
    md_text = textwrap.dedent(md_text)
    html = markdown.markdown(md_text, extensions=['fenced_code', 'tables'])
    # 加载模板文件
    html_template = readtxt(template_file)
    if "{html}" in html_template:
        page_html = html_template

    # 加载CSS
    custom_css = readtxt(cssfile)
    page_html = page_html.replace('{css}', custom_css)
    page_html = page_html.replace("{html}", html)
    return page_html

async def md_to_png(md_text:str, output_path:str,
        cssfile:str="template/base.css",
        template_file:str="", width:int=1080):
    '''markdown转PNG图（使用playwright）
    md_text:        Markdown文本内容
    output_path:    输出目录
    cssfile:        CSS样式文件路径
    template_file： 模板文件路径
    width:          输出图片宽度
    '''
    if not md_text.strip():
        return ""

    page_html = md2html(md_text, cssfile, template_file)
    output_filename = rand_filename(output_path, "md_", ".png")

    async with async_playwright() as pobj:
        browser = await pobj.chromium.launch()
        page = await browser.new_page(viewport={'width': width, 'height': 1})
        await page.set_content(page_html)

        content_height = await page.evaluate('document.body.scrollHeight')
        logging.debug("内容实际高度: %d px", content_height)
        await page.set_viewport_size({'width': width, 'height': content_height})
        await page.screenshot(path=output_filename, full_page=True)
        await browser.close()
    logging.debug("图片已保存:%s", output_filename)
    return output_filename


def md2png(
    md_text:str,
    output_path:str,
    cssfile = "template/base.css",
    template_file:str=""):
    ''' markdown格式转存为PNG图像（旧版，已废弃，使用md_to_png）
    md_text:        Markdown文本内容
    output_path:    输出目录
    cssfile         CSS样式文件；
    template_file： 模板文件
    '''
    return asyncio.run(md_to_png(md_text, output_path, cssfile, template_file))


def get_base64(filename:str) -> str:
    '''加载指定文件, 转为base64编码
    '''
    try:
        with open(filename, 'rb') as f:
            base64_data = base64.b64encode(f.read())
            # 使用安全的base64编码 则改为下面方式编码
            # base64_data = base64.urlsafe_b64encode(f.read())
            ret = base64_data.decode()
            return ret
    except Exception as err:
        print(err)
        return ''

def test_md2img():
    '''单元测试：各种markdown的标准格式
    '''
    # 示例Markdown文本
    md_text = """
    # 标题

    这是一个段落，包含**加粗**和*斜体*文本。
    
    这是代码：`code`

    ```
    import os
    a = b+1
    ```

    ## 二级目录

    - 列表项1
    - 列表项2

    """
    outpath = "output/"
    ret = md2png (md_text, outpath)
    print(f"图片已保存: {ret}")

def test_file2png ():
    ''' 从文件生成图
    '''
    fname = "md_news/20251105.md"
    fname = "md_news/20251102.md"
    md_text = readtxt(fname)

    outpath = "output/"
    ret = md2png (md_text, outpath)
    print(f"图片已保存: {ret}")

def test_template2png ():
    '''单元测试 模板生成
    '''
    fname = "md_news/news2.md"
    fname = "md_news/20251102.md"
    md_text = readtxt(fname)
    # 加载模板
    template_file = "template/template_1.html"
    # 生成图片
    outpath = "output/"
    ret = md2png (md_text, outpath, template_file=template_file)
    print(f"图片已保存: {ret}")

if __name__ == '__main__':
    # DEBUG  INFO ERROR  CRITICAL
    logging.basicConfig(level=logging.INFO)
    import fire
    fire.Fire()
