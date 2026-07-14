#!/usr/bin/env python3
#coding:utf-8

'''
__author__ = 'xmxoxo<xmxoxo@qq.com>'
七牛云 文件上传工具
pip install qiniu
'''

import os
# import logging
# import qiniu.config
from qiniu import Auth, put_file, etag
# , urlsafe_base64_encode   #, put_file_v2

# SaaS 七牛配置 七牛的 Access Key 和 Secret Key
QINIU_ACCESS_KEY = os.getenv('QINIU_ACCESS_KEY')
QINIU_SECRET_KEY = os.getenv('QINIU_SECRET_KEY')
# QINIU_ACCESS_KEY = 'sjusuhRV9Il4DXAH9UTmI2vj1i9SJF2PZX6QgaXl'
# QINIU_SECRET_KEY = 'Zpbl498c-Diwzqk_Idyqr8Noj3tV5QPX7IkM80bU'

BUCKET_NAME = 'kksaas'
BUCKET_DOMAIN = 'https://up-kksaas.keyibao.com'

def upload_to_qiniu(localfile:str, app_name:str,
    private=False, expires=3600, remove_local=False) -> str:
    ''' 文件自动发布工具：上传文件到七牛
    localfile: 本地文件路径
    remove_local: 成功后删除本地文件
    '''
    try:
        # 构建鉴权对象
        obj_qn = Auth(QINIU_ACCESS_KEY, QINIU_SECRET_KEY)

        # 上传到七牛后保存的文件名
        if app_name[-1] != "/":
            app_name += "/"
        # 生成KEY
        key = app_name + os.path.basename(localfile)
        # 生成上传 Token，可以指定过期时间等
        token = obj_qn.upload_token(BUCKET_NAME, key, 3600)
        # 上传文件
        ret, _ = put_file(token, key, localfile, version='v2')
        # ret, _ = put_file_v2(token, key, localfile)
        assert ret['key'] == key
        assert ret['hash'] == etag(localfile)
        # 上传后的文件 URL
        base_url = f'{BUCKET_DOMAIN}/{key}'
        # 生成私有访问地址，带过期时间
        if private:
            private_url = obj_qn.private_download_url(base_url, expires=expires)
            result = private_url
        else:
            result = base_url
    except Exception as err:
        print(err)
        result = ""

    # 成功后删除本地文件
    if remove_local:
        try:
            fpath = os.path.abspath(localfile)
            os.remove(fpath)
        except Exception:
            pass
    return result


def test_upload_to_qiniu():
    ''' 单元测试
    '''
    localfile = "charts/bar_20250220103756.png"
    app_name = "test"

    file_url = upload_to_qiniu(localfile, app_name)
    print(f'file_url:{file_url}')
    print()

    # 生成临时下载地址
    file_url = upload_to_qiniu(localfile, app_name, private=True, expires=3600)
    print(f'private file url:{file_url}')

if __name__ == '__main__':
    import fire
    fire.Fire()
