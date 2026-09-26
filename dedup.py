#!/usr/bin/env python
"""文本整理工具：去重 / 排序 / 合并 / 统计。"""

import argparse
from collections import Counter
from pathlib import Path


def read_lines(paths: list[Path], strip_empty: bool) -> list[str]:
    lines: list[str] = []
    for path in paths:
        text = path.read_text(encoding="utf-8", errors="ignore")
        for line in text.splitlines():
            if strip_empty and not line.strip():
                continue
            lines.append(line.rstrip("\n"))
    return lines


def dedupe(lines: list[str], ignore_case: bool) -> tuple[list[str], int]:
    seen: set[str] = set()
    result: list[str] = []
    for line in lines:
        key = line.lower() if ignore_case else line
        if key in seen:
            continue
        seen.add(key)
        result.append(line)
    return result, len(lines) - len(result)


def main() -> int:
    parser = argparse.ArgumentParser(description="文本整理工具")
    parser.add_argument("inputs", nargs="+", help="输入文件")
    parser.add_argument("-o", "--output", help="输出文件")
    parser.add_argument("--sort", action="store_true", help="输出前排序")
    parser.add_argument("--ignore-case", action="store_true", help="忽略大小写去重")
    parser.add_argument("--stats", action="store_true", help="显示重复统计")
    parser.add_argument("--word-freq", action="store_true", help="词频统计")
    parser.add_argument("--top", type=int, default=20, help="词频显示前 N 个")
    args = parser.parse_args()

    paths = [Path(p) for p in args.inputs]
    for p in paths:
        if not p.is_file():
            print(f"[错误] 文件不存在: {p}")
            return 1

    lines = read_lines(paths, strip_empty=True)
    unique, removed = dedupe(lines, args.ignore_case)

    if args.sort:
        unique.sort(key=lambda s: s.lower())

    if args.word_freq:
        counter: Counter[str] = Counter()
        for line in unique:
            counter.update(line.split())
        print(f"共 {len(counter)} 个不同词：")
        for word, count in counter.most_common(args.top):
            print(f"  {count:>6}  {word}")

    if args.stats:
        counter2: Counter[str] = Counter(lines)
        dupes = [(line, c) for line, c in counter2.items() if c > 1]
        dupes.sort(key=lambda x: -x[1])
        print(f"\n总行数 {len(lines)}，去重后 {len(unique)}，删除重复 {removed} 行")
        if dupes:
            print("重复最多的行：")
            for line, c in dupes[:10]:
                print(f"  x{c}  {line[:60]}")

    output = "\n".join(unique) + ("\n" if unique else "")
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"已写入 {args.output}（{len(unique)} 行）")
    elif not args.stats and not args.word_freq:
        print(output, end="")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())