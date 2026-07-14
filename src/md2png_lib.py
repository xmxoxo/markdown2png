#!/usr/bin/env python3
#coding:utf-8

'''
__author__ = 'xmxoxo<xmxoxo@qq.com>'
'''


import os
import logging
import textwrap
import random
import time
import markdown
from weasyprint import HTML

def rand_filename(path='', pre='', ext=''):
    '''按时间戳生成文件名'''
    nowtime = time.time()
    fmttxt = time.strftime('%Y%m%d%H%M%S', time.localtime(nowtime))

    dt = int((nowtime - int(nowtime))*1000)
    rndnum = random.randint(100, 999)
    filename = '%s%s%03d%03d%s' % (pre, fmttxt, dt, rndnum, ext)
    if path:
        mkfold(path)
    fname = os.path.join(path, filename)
    return fname

def mkfold(new_dir):
    '''创建目录，支持多级子目录'''
    try:
        if new_dir == '': return
        if not os.path.exists(new_dir):
            os.makedirs(new_dir, exist_ok=True)
    except Exception as e:
        pass

def readtxtfile(fname, encoding='utf-8'):
    ''' 读取文本文件, 自动识别编码 '''

    try:
        with open(fname, 'r', encoding=encoding) as f:
            data = f.read()
        return data
    except UnicodeDecodeError as e:
        try:
            with open(fname,'r', encoding='gb2312') as f:
                data = f.read()
            return data
        except Exception as e:
            return ''
    except Exception as e:
        return ''

def readtxt(fname, encoding='utf-8'):
    ''' 读入文件'''
    try:
        with open(fname, 'r', encoding=encoding) as f:
            data = f.read()
        return data
    except Exception as e:
        return ''


def md2png(
    md_text:str,
    output_path:str,
    cssfile = "template/base.css",
    template_file:str="", dpi=96):
    ''' markdown格式转存为PNG图像
    md_text:        Markdown文本内容
    output_path:    输出目录
    cssfile         CSS样式文件；
    template_file： 模板文件
    dpi             输出的分辨率
    '''
    if md_text=="":
        return ""
    
    # 读取CSS
    css = readtxt(cssfile)
    # 处理统一缩进
    md_text = textwrap.dedent(md_text)

    logging.info('正在加载markdown...')
    html = markdown.markdown(md_text, extensions=['fenced_code', 'tables'])
    # 可选：添加基础样式
    styled_html = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <style>
        {css}
        </style>
    </head>
    <body>
    {html}
    </body>
    </html>
    """

    # 加载模板
    if template_file:
        logging.info('正在加载模板...')
        html_template = readtxt(template_file)
        # 判断是否含有标识
        text_keys = "{html}"
        if text_keys in html_template:
            logging.info('正在应用模板...')
            styled_html = html_template.replace(text_keys, html)
    
    styled_html = textwrap.dedent(styled_html)
    # 自动生成文件名
    logging.info('正在生成文件名...')
    output_filename = rand_filename(output_path, "md_", ".png")

    # 保存输出文件
    logging.info('正在生成图像...')
    obj = HTML(string=styled_html)
    # resolution 分辨率，默认是96
    obj.write_png(output_filename, resolution=dpi)

    return output_filename

def test_md2img ():
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
    ret = md2png (md_text, outpath, dpi=150)
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


