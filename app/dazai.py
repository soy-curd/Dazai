#!/usr/bin/env python
# -*- coding: utf-8 -*-
from subprocess import Popen, call
import subprocess
import datetime
import sys
import os

def main():
    if len(sys.argv) > 1:
        sys.exit(0)

    d = datetime.datetime.today()
     
    config = {  
      "booktitle": "実践　太宰治",
      "aut": "文學ラボ",
      "prt": "株式会社ポプルス",
      "pbl": "文學ラボ",
      "contact": "soycurd1@gmail.com",
      "prt_url":  "http://soy-curd.hatenablog.com/",
      "rights": d.strftime("(C) %Y @bungaku, lab"),
      "date": d.strftime("%Y年%m月%d日"),
      "pubhistory": d.strftime("%Y年%m月%d日 v1.0.0版発行")
      }
    
    preface = """
# ほげ！
    
    
## ほげほげ
ほえええええ
    
"""
    
    markdowns = ["""
# ほげ
    
ほげげ
    
## ほげ
ほげ！
    
"""]
    
    make_book(config, preface, markdowns)

def make_book(config, preface, markdowns):
    # make config.yml
    doc_dir = os.path.join(os.getcwd(), "doc")
    config_path = make_yml(
        config,
        doc_dir, 
        "config_tmpl.yml",
        os.path.join(doc_dir, 'config.yml')
        )

    # make preface
    preface_path = md2re(preface, "preface", doc_dir)

    # make chapters
    markdown_filenames = list(map(lambda x: "chap" + str(x + 1), range(len(markdowns))))
    chap_paths = map(lambda x: md2re(x[0], x[1], doc_dir), zip(markdowns, markdown_filenames))
    
    # make catalog
    catalog = {
    "PREDEF":preface_path,
    "CHAPS": chap_paths,
    "APPENDIX":"",
    "POSTDEF":""
    }
    catalog_path = make_yml(
        catalog,
        doc_dir, 
        "catalog_tmpl.yml",
        os.path.join(doc_dir, 'catalog.yml')
        )

    pdf_path = make_pdf(doc_dir)
    return pdf_path
    
    
def make_yml(config, tmpldir, tmplate, filename):
    from jinja2 import Environment, FileSystemLoader
    
    env = Environment(loader=FileSystemLoader(tmpldir, encoding='utf8'))    
    tmpl = env.get_template(tmplate)
    render = tmpl.render(**config)

    # Output to a text file
    with open(filename, 'w') as f:
        f.write(render)
        
    return filename
    
def md2re(markdown, filename, dir):
    filepath = os.path.join(dir, filename)
    
    # markdownの作成
    with open(filepath + ".md", 'w') as f1:
        f1.write(markdown)

    # reviewファイルの作成
    p1 = Popen(["md2review", filepath + ".md"], stdout=subprocess.PIPE, shell=False)
    stdout, stderr = p1.communicate()
    re_str = stdout.decode('utf-8')
    with open(filepath + ".re", 'w') as f2:
        f2.write(re_str)
    
    return filename + ".re"
    
def make_pdf(pdf_dir):
    current_dir = os.getcwd()
    os.chdir(pdf_dir)
    
    filename = "book.pdf"
    cmds = [
        ["rm", filename],
        ["rm", "-r", "book-pdf"],
        ["review-pdfmaker", "config.yml"]
    ]
    
    for cmd in cmds:
        call(cmd, shell=False)
    d = datetime.datetime.today()
    newfilename = "book_" + d.strftime("%Y%m%d%H%M%S") + ".pdf"
    os.rename(filename, "../static/pdf/" + newfilename)
    
    
    os.chdir(current_dir)

    return newfilename

if __name__ == '__main__':
    main()
