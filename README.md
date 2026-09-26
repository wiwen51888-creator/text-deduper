# text-deduper

文本整理工具。去重、排序、去空行、合并多个文件、统计词频。适合整理名单、日志、数据。

## 安装

无需第三方依赖，Python 3.8+ 即可。

## 用法

```bash
# 去重并输出去重后的行数
python dedup.py list.txt

# 输出去重后的文件
python dedup.py list.txt -o unique.txt

# 合并多个文件并去重
python dedup.py a.txt b.txt c.txt -o merged.txt

# 去重后按字母排序
python dedup.py list.txt --sort

# 忽略大小写去重
python dedup.py list.txt --ignore-case

# 统计重复行
python dedup.py list.txt --stats

# 词频统计（按空格分词）
python dedup.py article.txt --word-freq
```

## 参数

- `-o/--output`：输出文件
- `--sort`：输出前排序
- `--ignore-case`：忽略大小写去重
- `--keep-order`：保持原始顺序（默认）
- `--stats`：显示重复统计
- `--word-freq`：词频统计
- `--strip-empty`：去掉空行（默认开启）