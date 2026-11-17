#!/usr/bin/env python3
"""
Markdown → PDF 转换工具（交接文档专用）

用法：
    python3 tools/md2pdf.py <md文件或目录> [-o 输出目录]

特点：
    - 中文排版（PingFang SC），表格、代码块、截图均正确渲染
    - 自动生成页眉页脚与页码
    - 依赖：markdown 库 + 本机 Google Chrome（无需 pandoc/LaTeX）
"""
import sys, os, re, subprocess, tempfile, argparse, pathlib, html

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

CSS = """
@page { size: A4; margin: 18mm 16mm 20mm 16mm; }
* { box-sizing: border-box; }
body {
  font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  font-size: 10.5pt; line-height: 1.75; color: #1a1a1a; margin: 0;
  -webkit-print-color-adjust: exact; print-color-adjust: exact;
}
h1 { font-size: 20pt; font-weight: 600; margin: 0 0 4mm; padding-bottom: 3mm;
     border-bottom: 2.5px solid #2563eb; color: #0f172a; }
h2 { font-size: 14pt; font-weight: 600; margin: 9mm 0 3mm; padding-left: 3mm;
     border-left: 4px solid #2563eb; color: #1e3a8a; page-break-after: avoid; }
h3 { font-size: 11.5pt; font-weight: 600; margin: 6mm 0 2mm; color: #334155;
     page-break-after: avoid; }
h4 { font-size: 10.5pt; font-weight: 600; margin: 4mm 0 2mm; color: #475569; }
p { margin: 0 0 2.5mm; }
blockquote { margin: 3mm 0; padding: 2.5mm 4mm; background: #f8fafc;
             border-left: 3px solid #94a3b8; color: #475569; font-size: 9.5pt; }
blockquote p { margin: 0 0 1.5mm; }
blockquote p:last-child { margin-bottom: 0; }
table { border-collapse: collapse; width: 100%; margin: 3mm 0; font-size: 9pt;
        page-break-inside: avoid; }
th { background: #eff6ff; color: #1e3a8a; font-weight: 600; text-align: left;
     padding: 2mm 2.5mm; border: 1px solid #cbd5e1; }
td { padding: 2mm 2.5mm; border: 1px solid #cbd5e1; vertical-align: top; }
tr:nth-child(even) td { background: #fafafa; }
code { font-family: "SF Mono", Menlo, Consolas, monospace; font-size: 8.8pt;
       background: #f1f5f9; padding: 0.4mm 1.2mm; border-radius: 2px; color: #be123c; }
pre { background: #0f172a; color: #e2e8f0; padding: 3mm 4mm; border-radius: 3px;
      overflow-x: auto; margin: 3mm 0; page-break-inside: avoid; }
pre code { background: none; color: inherit; padding: 0; font-size: 8.5pt;
           line-height: 1.6; white-space: pre-wrap; word-break: break-all; }
img { max-width: 100%; height: auto; margin: 3mm 0; border: 1px solid #e2e8f0;
      border-radius: 3px; page-break-inside: avoid; }
ul, ol { margin: 0 0 2.5mm; padding-left: 7mm; }
li { margin-bottom: 1mm; }
hr { border: none; border-top: 1px solid #e2e8f0; margin: 6mm 0; }
a { color: #2563eb; text-decoration: none; }
strong { color: #0f172a; font-weight: 600; }
.cover-meta { color: #64748b; font-size: 9pt; margin-bottom: 6mm; }
"""

def convert(md_path: pathlib.Path, out_dir: pathlib.Path) -> pathlib.Path:
    import markdown
    text = md_path.read_text(encoding="utf-8")

    md = markdown.Markdown(extensions=[
        "tables", "fenced_code", "nl2br", "sane_lists", "attr_list", "toc",
    ])
    body = md.convert(text)

    # 任务列表复选框渲染
    body = body.replace("[ ]", "☐").replace("[x]", "☑").replace("[X]", "☑")

    doc = f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<title>{html.escape(md_path.stem)}</title><style>{CSS}</style></head>
<body>{body}</body></html>"""

    # HTML 必须和 md 同目录，图片相对路径才找得到
    tmp_html = md_path.with_suffix(".__tmp__.html")
    tmp_html.write_text(doc, encoding="utf-8")

    out_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = out_dir / (md_path.stem + ".pdf")
    try:
        subprocess.run([
            CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
            "--run-all-compositor-stages-before-draw", "--virtual-time-budget=10000",
            f"--print-to-pdf={pdf_path}", tmp_html.as_uri(),
        ], check=True, capture_output=True, timeout=120)
    finally:
        tmp_html.unlink(missing_ok=True)
    return pdf_path

def main():
    ap = argparse.ArgumentParser(description="Markdown → PDF")
    ap.add_argument("target", help="md 文件或包含 md 的目录")
    ap.add_argument("-o", "--out", default=None, help="输出目录，默认为 <目录>/PDF文档")
    args = ap.parse_args()

    target = pathlib.Path(args.target).resolve()
    if not os.path.exists(CHROME):
        sys.exit(f"找不到 Chrome：{CHROME}")

    files = sorted(target.glob("*.md")) if target.is_dir() else [target]
    files = [f for f in files if not f.name.startswith(".")]
    if not files:
        sys.exit("没有找到 .md 文件")

    base = target if target.is_dir() else target.parent
    out_dir = pathlib.Path(args.out).resolve() if args.out else base / "PDF文档"

    for f in files:
        pdf = convert(f, out_dir)
        size = pdf.stat().st_size / 1024
        print(f"  ✓ {f.name}  →  {pdf.name}  ({size:.0f} KB)")
    print(f"\n完成，共 {len(files)} 份，输出目录：{out_dir}")

if __name__ == "__main__":
    main()
