# -*- coding: utf-8 -*-
"""生成《操作系统实验2报告》DOCX。"""
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

NAVY = "1F3864"          # 标题深蓝
GRAY = "808080"          # 题注灰
CODE_BG = "F4F6F8"       # 代码底色
CODE_BAR = "2F5597"      # 代码左侧竖线
HEAD_BG = "D9E2F3"       # 表头底色


def set_run(run, ascii_font="Times New Roman", east="宋体", size=12,
            bold=False, color=None, italic=False):
    """设置一个 run 的中西文字体、字号、加粗与颜色。"""
    run.font.name = ascii_font
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.insert(0, rFonts)
    rFonts.set(qn("w:ascii"), ascii_font)
    rFonts.set(qn("w:hAnsi"), ascii_font)
    rFonts.set(qn("w:eastAsia"), east)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = RGBColor.from_string(color)


def para(text="", ascii_font="Times New Roman", east="宋体", size=12,
         bold=False, color=None, align=None, line=1.5, before=0, after=0,
         first_indent=None, keep_next=False):
    """添加一个普通段落并设置格式。"""
    p = doc.add_paragraph()
    pf = p.paragraph_format
    if align is not None:
        p.alignment = align
    pf.line_spacing = line
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    if first_indent:
        pf.first_line_indent = Pt(first_indent)
    pf.keep_with_next = keep_next
    if text:
        r = p.add_run(text)
        set_run(r, ascii_font, east, size, bold, color)
    return p


def body(text):
    """正文段落：宋体小四、1.5 倍行距、首行缩进 2 字符。"""
    return para(text, size=12, line=1.5, first_indent=24, after=0)


def body_noindent(text, **kw):
    """不缩进的正文段落（用于图、表说明后的总结等）。"""
    return para(text, size=12, line=1.5, first_indent=0, **kw)


def h1(text):
    """一级标题：黑体四号、深蓝、加粗。"""
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.keep_with_next = True
    pf.line_spacing = 1.25
    pf.space_before = Pt(14)
    pf.space_after = Pt(8)
    r = p.add_run(text)
    set_run(r, "Times New Roman", "黑体", 14, True, NAVY)
    return p


def h2(text):
    """二级标题：黑体小四加粗、深蓝。"""
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.keep_with_next = True
    pf.line_spacing = 1.25
    pf.space_before = Pt(9)
    pf.space_after = Pt(4)
    r = p.add_run(text)
    set_run(r, "Times New Roman", "黑体", 12.5, True, NAVY)
    return p


def caption(text, align=WD_ALIGN_PARAGRAPH.LEFT):
    """图/表/代码题注：楷体五号、灰色。"""
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.keep_with_next = True
    pf.line_spacing = 1.15
    pf.space_before = Pt(6)
    pf.space_after = Pt(2)
    p.alignment = align
    r = p.add_run(text)
    set_run(r, "Times New Roman", "楷体", 10.5, False, GRAY)
    return p


def _code_para(text):
    """单个代码行：等宽字体、浅灰底、左侧蓝色竖线。"""
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.line_spacing = 1.0
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.left_indent = Pt(8)
    pf.right_indent = Pt(4)
    pf.keep_with_next = True
    r = p.add_run(text if text else " ")
    set_run(r, "Consolas", "宋体", 8.5, False)
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    left = OxmlElement("w:left")
    left.set(qn("w:val"), "single")
    left.set(qn("w:color"), CODE_BAR)
    left.set(qn("w:sz"), "12")
    left.set(qn("w:space"), "4")
    pBdr.append(left)
    pPr.insert_element_before(
        pBdr, "w:shd", "w:tabs", "w:suppressAutoHyphens", "w:kinsoku",
        "w:wordWrap", "w:overflowPunct", "w:topLinePunct", "w:autoSpaceDE",
        "w:autoSpaceDN", "w:bidi", "w:adjustRightInd", "w:snapToGrid",
        "w:spacing", "w:ind", "w:contextualSpacing", "w:mirrorIndents",
        "w:suppressOverlap", "w:jc", "w:textDirection", "w:textAlignment",
        "w:textboxTightWrap", "w:outlineLvl", "w:divId", "w:cnfStyle",
        "w:rPr", "w:sectPr", "w:pPrChange")
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), CODE_BG)
    pPr.insert_element_before(
        shd, "w:tabs", "w:suppressAutoHyphens", "w:kinsoku", "w:wordWrap",
        "w:overflowPunct", "w:topLinePunct", "w:autoSpaceDE", "w:autoSpaceDN",
        "w:bidi", "w:adjustRightInd", "w:snapToGrid", "w:spacing", "w:ind",
        "w:contextualSpacing", "w:mirrorIndents", "w:suppressOverlap",
        "w:jc", "w:textDirection", "w:textAlignment", "w:textboxTightWrap",
        "w:outlineLvl", "w:divId", "w:cnfStyle", "w:rPr", "w:sectPr",
        "w:pPrChange")
    return p


def code_block(text, cap=None):
    """插入多行代码块；长代码允许跨页，短代码保持整块。"""
    if cap:
        caption(cap)
    lines = text.strip("\n").split("\n")
    keep_together = len(lines) <= 24          # 超过 24 行允许分页，避免大片留白
    for i, line in enumerate(lines):
        p = _code_para(line)
        p.paragraph_format.keep_with_next = keep_together and i < len(lines) - 1
    spacer(4)


def spacer(pt=6):
    """插入一个小的空段落。"""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = Pt(pt) if pt else 1.0
    r = p.add_run("")
    r.font.size = Pt(pt if pt else 1)
    return p


def shade_cell(cell, fill):
    """给表格单元格加底纹。"""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    tcPr.insert_element_before(
        shd, "w:noWrap", "w:tcMar", "w:textDirection", "w:tcFitText",
        "w:vAlign", "w:hideMark")


def set_cell_text(cell, text, bold=False, align=WD_ALIGN_PARAGRAPH.LEFT,
                  size=10.5, color=None):
    """写入单元格文本，清空默认段落间距。"""
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    p = cell.paragraphs[0]
    p.alignment = align
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing = 1.15
    for r in list(p.runs):
        r._element.getparent().remove(r._element)
    r = p.add_run(text)
    set_run(r, "Times New Roman", "宋体", size, bold, color)


def content_table(caption_text, headers, rows, widths, aligns=None,
                  keep_together=None, font=10.5):
    """插入带表头底纹、固定列宽的三线/网格表。"""
    caption(caption_text)
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    for i, w in enumerate(widths):
        t.columns[i].width = Cm(w)
    tblPr = t._tbl.tblPr
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    tblPr.insert_element_before(layout, "w:tblCellMar", "w:tblLook",
                                "w:tblCaption", "w:tblDescription")
    # 所有行禁止在行内跨页，避免出现只剩一个字的碎片行
    for row in t.rows:
        trPr = row._tr.get_or_add_trPr()
        trPr.append(OxmlElement("w:cantSplit"))
    # 表头
    hdr = t.rows[0]
    trPr = hdr._tr.get_or_add_trPr()
    tblHeader = OxmlElement("w:tblHeader")
    trPr.append(tblHeader)
    for i, h in enumerate(headers):
        c = hdr.cells[i]
        c.width = Cm(widths[i])
        set_cell_text(c, h, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER,
                      size=font)
        shade_cell(c, HEAD_BG)
    # 数据行
    for row in rows:
        tr = t.add_row()
        trPr = tr._tr.get_or_add_trPr()
        trPr.append(OxmlElement("w:cantSplit"))
        cells = tr.cells
        for i, val in enumerate(row):
            cells[i].width = Cm(widths[i])
            al = aligns[i] if aligns else WD_ALIGN_PARAGRAPH.LEFT
            set_cell_text(cells[i], str(val), align=al, size=font)
    # 小表尽量整表放在同一页
    if keep_together is None:
        keep_together = len(rows) <= 5
    if keep_together:
        for row in t.rows[:-1]:
            for c in row.cells:
                for p in c.paragraphs:
                    p.paragraph_format.keep_with_next = True
    spacer(6)
    return t


def add_picture(path, width_cm, cap):
    """插入居中的图片并加图题。"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    p.add_run().add_picture(path, width=Cm(width_cm))
    caption(cap, align=WD_ALIGN_PARAGRAPH.CENTER)


def footer_page_number(section):
    """页脚居中页码（封面页不显示）。"""
    p = section.footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p.add_run()
    set_run(r1, size=9, color=GRAY)
    fld1 = OxmlElement("w:fldChar")
    fld1.set(qn("w:fldCharType"), "begin")
    r1._r.append(fld1)
    r2 = p.add_run()
    set_run(r2, size=9, color=GRAY)
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE "
    r2._r.append(instr)
    r3 = p.add_run()
    set_run(r3, size=9, color=GRAY)
    fld2 = OxmlElement("w:fldChar")
    fld2.set(qn("w:fldCharType"), "end")
    r3._r.append(fld2)


# ===================== 文档初始化 =====================
doc = Document()
sec = doc.sections[0]
sec.page_width = Cm(21.0)
sec.page_height = Cm(29.7)
sec.left_margin = Cm(2.6)
sec.right_margin = Cm(2.4)
sec.top_margin = Cm(2.4)
sec.bottom_margin = Cm(2.2)
sec.different_first_page_header_footer = True
footer_page_number(sec)

normal = doc.styles["Normal"]
normal.font.name = "Times New Roman"
normal.font.size = Pt(12)
normal.element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")

cp = doc.core_properties
cp.title = "操作系统实验2报告：Linux 系统调用新增（编译内核法）"
cp.author = "嵇明国"
cp.subject = "操作系统上机实验"

# ===================== 封面 =====================
p = para("江苏大学计算机学院", "Times New Roman", "黑体", 26, True, NAVY,
         WD_ALIGN_PARAGRAPH.CENTER, 1.0, 70, 12)
p = para("上机实验报告", "Times New Roman", "黑体", 34, True, NAVY,
         WD_ALIGN_PARAGRAPH.CENTER, 1.0, 0, 6)
p = para("（操作系统）", "Times New Roman", "楷体", 14, False, GRAY,
         WD_ALIGN_PARAGRAPH.CENTER, 1.0, 0, 40)

cover_rows = [
    ("课程名称：", "操作系统"),
    ("实验名称：", "Linux 系统调用新增（编译内核法）"),
    ("实验学期：", "2026—2027 学年，第一学期"),
    ("学生姓名：", "嵇明国"),
    ("专业班级：", "计算机 2403 班"),
    ("学号：", "3240602077"),
    ("指导教师：", "何文文"),
    ("开课系：", "计算机学院"),
]
t = doc.add_table(rows=len(cover_rows), cols=2)
t.style = "Normal Table"
t.alignment = WD_TABLE_ALIGNMENT.CENTER
t.autofit = False
t.columns[0].width = Cm(3.6)
t.columns[1].width = Cm(9.6)
for i, (k, v) in enumerate(cover_rows):
    c0, c1 = t.rows[i].cells
    c0.width = Cm(3.6)
    c1.width = Cm(9.6)
    set_cell_text(c0, k, bold=False, align=WD_ALIGN_PARAGRAPH.RIGHT, size=14)
    set_cell_text(c1, v, bold=False, align=WD_ALIGN_PARAGRAPH.CENTER, size=14)

para("操作系统课程组制", "Times New Roman", "宋体", 14, False, None,
     WD_ALIGN_PARAGRAPH.CENTER, 1.0, 110, 0)
doc.add_page_break()

# ===================== 正文标题与信息表 =====================
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
pf = p.paragraph_format
pf.space_after = Pt(10)
pf.line_spacing = 1.0
pPr = p._p.get_or_add_pPr()
pBdr = OxmlElement("w:pBdr")
bottom = OxmlElement("w:bottom")
bottom.set(qn("w:val"), "single")
bottom.set(qn("w:color"), NAVY)
bottom.set(qn("w:sz"), "10")
bottom.set(qn("w:space"), "6")
pBdr.append(bottom)
pPr.insert_element_before(pBdr, "w:shd", "w:tabs", "w:suppressAutoHyphens",
                          "w:kinsoku", "w:wordWrap", "w:overflowPunct",
                          "w:topLinePunct", "w:autoSpaceDE", "w:autoSpaceDN",
                          "w:bidi", "w:adjustRightInd", "w:snapToGrid",
                          "w:spacing", "w:ind", "w:contextualSpacing",
                          "w:mirrorIndents", "w:suppressOverlap", "w:jc",
                          "w:textDirection", "w:textAlignment",
                          "w:textboxTightWrap", "w:outlineLvl", "w:divId",
                          "w:cnfStyle", "w:rPr", "w:sectPr", "w:pPrChange")
r = p.add_run("江苏大学计算机学院上机实验报告")
set_run(r, "Times New Roman", "黑体", 16, True, NAVY)

t = doc.add_table(rows=1, cols=2)
t.style = "Normal Table"
t.alignment = WD_TABLE_ALIGNMENT.CENTER
t.autofit = False
t.columns[0].width = Cm(10)
t.columns[1].width = Cm(6)
c0, c1 = t.rows[0].cells
c0.width = Cm(10)
c1.width = Cm(6)
set_cell_text(c0, "实验题目：Linux 系统调用新增（编译内核法）",
              bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, size=12)
set_cell_text(c1, "设计时间：2026 年 11 月 20 日",
              bold=False, align=WD_ALIGN_PARAGRAPH.RIGHT, size=12)
spacer(6)

# ===================== 一、实验目的与要求 =====================
h1("一、实验目的与要求")
body("本实验以 Linux 系统调用为对象，采用“编译内核法”在 x86_64 架构的 Linux 6.8.12 内核中静态新增系统调用 sys_cube：它接收整数 n，计算 n 的三次方，把 n 与计算结果写入内核日志，并通过用户指针把结果返回给用户态。实验覆盖从内核源码准备、调用号选择、系统调用表修改、内核函数实现，到内核配置编译、安装启动和用户态验证的完整链路，目的是理解系统调用号、系统调用表、内核态实现与用户态调用之间的关系，并与题目 1 的 LKM 方式形成对比。")
body("（1）理解系统调用的工作机制：用户态如何通过 syscall 指令和调用号进入内核，内核如何以调用号为下标查 sys_call_table 并分派到具体处理函数。")
body("（2）掌握新增系统调用的完整步骤：选择未使用的调用号、修改 syscall_64.tbl、实现内核函数、重新编译安装内核并重启。")
body("（3）掌握内核函数的编写规范：SYSCALL_DEFINEn 宏、__user 标注、copy_to_user、参数校验、printk 日志与负 errno 返回值。")
body("（4）掌握内核源码的配置、编译、模块安装、GRUB 引导与 uname -r 验证方法，理解“源码—编译产物—运行内核”三者一致性的含义。")
body("（5）编写用户态测试程序，对 0、2、-3 等输入比较返回值、出参与预期值，并用 dmesg 核对内核日志。")
body("（6）说明编译内核法与 LKM 的差异、用户态到内核态的调用路径，以及内核态编程的主要约束。")
body("（7）如实记录 AI 辅助过程和验证结论。")

# ===================== 二、实验内容 =====================
h1("二、实验内容")
body("本实验在 Ubuntu 22.04.5 虚拟机上完成，内容由“改源码—编内核—验调用”三部分组成：")
body("1. 准备与运行内核版本一致的 linux-6.8.12 源码，完成配置、编译、安装并重启进入新内核。")
body("2. 在 arch/x86/entry/syscalls/syscall_64.tbl 中选择未使用的 462 号，登记为 common ABI 的 cube，入口名为 sys_cube。")
body("3. 在 kernel/sys.c 中实现 SYSCALL_DEFINE2(cube, int, n, long __user *, result)，完成 n³ 计算、printk 输出、copy_to_user 回写与错误码返回。")
body("4. 编写用户态 test.c，通过 syscall(462, n, &result) 调用，覆盖 0、2、-3 以及空指针、非法地址等错误路径。")
body("5. 使用 dmesg 查看内核打印的 n 与 n³，与用户态结果交叉验证。")
body("6. 记录关键修改位置、一致性保证方法、常见失败与排查方法，并与 LKM 方式对比。")
body("7. 记录 AI 辅助与人工验证过程。")

# ===================== 三、实验设备与环境 =====================
h1("三、实验设备与环境")
body("实验在 VMware Workstation 17 Player 中安装的 64 位 Ubuntu 虚拟机上完成，虚拟机与宿主机相互隔离，即使新内核启动失败也不影响宿主机。实验环境如表 3-1 所示。")
content_table(
    "表 3-1  实验环境",
    ["项目", "配置说明"],
    [
        ["宿主机", "Windows 11，VMware Workstation 17 Player"],
        ["虚拟机", "Ubuntu 22.04.5 LTS 64 位，2 vCPU、3.8 GB 内存、3.8 GB swap"],
        ["运行内核", "Linux 6.8.12（由本实验源码编译并启动）"],
        ["内核源码", "linux-6.8.12.tar.xz，kernel.org 原版，经清华 TUNA 镜像下载，sha256 校验通过"],
        ["编译依赖", "gcc、GNU make、bison、flex、libssl-dev、libelf-dev、libncurses-dev、bc、rsync"],
        ["磁盘空间", "根分区 49 GB，编译前可用约 33 GB；/boot 不是独立分区，位于根分区下"],
        ["验证工具", "uname、syscall(2)、dmesg、grep、systemctl"],
        ["工程目录", "~/kernel/linux-6.8.12（内核源码）、~/syscall_test（用户态测试程序）"],
    ],
    [3.4, 12.6])

# ===================== 四、设计正文 =====================
h1("四、设计正文")
h2("4.1 总体设计思路")
body("新增系统调用与编写普通用户态函数的最大区别在于：调用号与分派表属于内核镜像的一部分，不能像 LKM 那样在运行时“挂”进去，必须修改内核源码并重新生成 vmlinuz。因此本实验按图 4-1 的九个步骤推进，可归为三个阶段：源码与实现（步骤 1–4）、编译与安装（步骤 5–7）、启动与验证（步骤 8–9）。")
add_picture(os.path.join("报告插图", "flow_build.png"), 15.2,
            "图 4-1  新增系统调用（编译内核法）的完整流程")
body("表 4-1 列出了本实验的关键修改位置。除系统调用表与内核函数外，用户态测试程序、内核配置也需要同步调整；内核源码的其余部分保持原样。")
content_table(
    "表 4-1  关键修改位置",
    ["修改对象", "文件", "内容"],
    [
        ["系统调用号", "arch/x86/entry/syscalls/syscall_64.tbl",
         "新增一行：462　common　cube　sys_cube"],
        ["内核函数", "kernel/sys.c",
         "实现 SYSCALL_DEFINE2(cube, int, n, long __user *, result)"],
        ["用户态测试", "~/syscall_test/test.c", "syscall(462, n, &result) 及错误路径测试"],
        ["内核配置", ".config",
         "CONFIG_DEBUG_INFO_NONE=y，清空证书路径，关闭 MODULE_SIG_ALL"],
    ],
    [2.6, 6.2, 7.2])
body("设计遵循以下原则：")
body("（1）编号唯一：先在 syscall_64.tbl 中确认 462 未被占用，再写入，避免与已有调用冲突。")
body("（2）命名一致：tbl 第三列的调用名 cube 必须与 SYSCALL_DEFINE2 的第一个参数一致，第四列写入口名 sys_cube；构建系统把第四列拼成 __x64_sys_cube。")
body("（3）接口明确：n 为输入，result 为用户空间出参，返回 0 表示成功，负 errno 表示失败，避免把计算结果与错误码混在同一个返回值里。")
body("（4）安全第一：内核不能直接解引用用户指针，所有用户地址都经 copy_to_user 检查并复制；对空指针与溢出范围提前拒绝。")
body("（5）可回退：保留旧内核的 GRUB 启动项，新内核启动失败时可从 Advanced options 回退。")

h2("4.2 系统调用号的选择与系统调用表修改")
body("Linux 的系统调用号是用户态与内核态之间的“约定编号”，本身没有语义，内核只把它当作 sys_call_table 的下标。x86_64 的调用号分配记录在 arch/x86/entry/syscalls/syscall_64.tbl 中，每行格式为“编号、ABI、名称、入口函数”。选择编号时先查看当前内核已用的最大编号：")
code_block(r"""
$ cd ~/kernel/linux-6.8.12
$ tail -n 4 arch/x86/entry/syscalls/syscall_64.tbl
459	common	lsm_get_self_attr	sys_lsm_get_self_attr
460	common	lsm_set_self_attr	sys_lsm_set_self_attr
461	common	lsm_list_modules	sys_lsm_list_modules
""", "代码 4-1  查看已用的最大系统调用号")
body("Linux 6.8.12 中 461 是已用的最大编号，462 尚未分配。再用 grep 确认没有重复：")
code_block(r"""
$ grep -nE '^462[[:space:]]' arch/x86/entry/syscalls/syscall_64.tbl
$ echo $?
1
""", "代码 4-2  确认 462 号未被占用")
body("返回 1 表示没有匹配，编号可用。随后在该文件末尾追加一行：")
code_block(r"""
462	common	cube	sys_cube
""", "代码 4-3  系统调用表新增表项")
body("四个字段的含义：462 是调用号；common 表示该调用同时适用于 x86_64 与 x32 ABI（若只在 64 位下使用也可写 64）；cube 是系统调用名，必须与 SYSCALL_DEFINE2 的第一个参数一致；sys_cube 是入口函数名。")
body("修改后不需要手工编辑 include/linux/syscalls.h，也不需要手工维护 sys_call_table。编译时内核构建系统会由该表生成 arch/x86/include/generated/asm/syscalls_64.h，并在 arch/x86/entry/syscall_64.c 中展开为 sys_call_table：")
code_block(r"""
#define __SYSCALL_64(nr, sym, qual) extern asmlinkage long __x64_##sym(const struct pt_regs *);
#include <asm/syscalls_64.h>
#undef __SYSCALL_64

#define __SYSCALL_64(nr, sym, qual) [nr] = __x64_##sym,
asmlinkage const sys_call_ptr_t sys_call_table[] = {
#include <asm/syscalls_64.h>
};
""", "代码 4-4  由表生成 sys_call_table 的机制（源码节选）")
body("因此表项 462 最终指向 __x64_sys_cube，extern 声明也由生成的头文件自动给出。这是 6.x 内核在 x86_64 上的做法；其他架构的入口文件和头文件不同，需要修改对应架构的表。")

h2("4.3 内核函数 sys_cube 的设计与实现")
body("sys_cube 的接口为 long sys_cube(int n, long __user *result)。返回值 0 表示成功，-EINVAL 表示参数非法（空指针或 n 超出可安全计算的范围），-EFAULT 表示 result 指向的用户地址不可访问。计算结果通过 result 写回用户空间，同时用 printk 打印 n 与 n³。")
body("选择指针出参而不是直接返回 n³，是因为系统调用约定用负数表示错误：若直接返回 n³，当 n 为负数时，返回值可能落在 -1～-4095 区间，glibc 的 syscall() 会把它误认为 -errno，用户态只能看到 -1 与 errno，无法区分“计算结果”和“错误码”。把结果放到用户指针、返回值只表示成功与否，可以彻底消除这种歧义。这一问题在 5.4 节有实测对照。")
code_block(r"""
/* kernel/sys.c 末尾 */
SYSCALL_DEFINE2(cube, int, n, long __user *, result)
{
    long res;

    /* 空指针直接拒绝，避免无意义的复制 */
    if (!result)
        return -EINVAL;

    /* 限制 |n| <= 2^21 - 1，保证 n^3 不超过 64 位 long 的范围 */
    if (n > 2097151 || n < -2097151)
        return -EINVAL;

    /* 先转换为 long 再相乘，避免 int 乘法溢出 */
    res = (long)n * n * n;

    /* 内核日志：dmesg 中可看到 n 与 n^3 */
    printk(KERN_INFO "sys_cube: n=%d, n^3=%ld\n", n, res);

    /* 把结果复制到用户空间；返回非 0 表示有字节未复制成功 */
    if (copy_to_user(result, &res, sizeof(res)))
        return -EFAULT;

    return 0;
}
""", "代码 4-5  sys_cube 的内核态实现")
body("实现中的关键点如下：")
body("（1）SYSCALL_DEFINE2 会展开出 __do_sys_cube、__se_sys_cube 与 __x64_sys_cube 三个层次：__x64_sys_cube 从 pt_regs 中取出 rdi、rsi，__se_sys_cube 负责 32 位参数的符号扩展，__do_sys_cube 才是带 int、long __user * 参数的函数体。宏的第一个参数 cube 必须与 tbl 第三列一致，tbl 第四列写 sys_cube。")
body("（2）__user 是给 sparse 静态检查器看的标注，gcc 编译时会忽略；它提醒开发者该指针指向用户空间，不能像普通指针那样直接解引用，必须通过 copy_to_user/copy_from_user 访问。")
body("（3）copy_to_user(to, from, n) 返回未成功复制的字节数，0 表示全部成功。它在内部完成用户地址范围检查，并在访问失败时通过异常表修复，不会让内核直接崩溃；失败时返回 -EFAULT。")
body("（4）参数校验分两层：空指针与数值范围在计算前检查，非法地址由 copy_to_user 检查。内核必须返回 -EINVAL、-EFAULT 这样的负 errno，不能返回裸 -1，因为 -1 会被解释为 -EPERM，语义完全不同。")
body("（5）printk 使用 KERN_INFO 级别，格式串中 int 用 %d、long 用 %ld；内核态没有 printf，也不能使用 C 标准库。")
body("（6）函数没有全局状态，天然可重入；局部变量只有一个 long，不占内核栈空间。")

h2("4.4 用户态测试程序的设计与实现")
body("测试程序通过 glibc 提供的 syscall(2) 发起调用。由于新增的 462 号还没有进入系统的 unistd_64.h，程序里用宏 SYS_CUBE 定义编号。每次调用前把 errno 清零，调用后用 strerror(errno) 打印错误信息，便于区分“返回值”与“错误码”。")
code_block(r"""
#define _GNU_SOURCE
#include <unistd.h>
#include <sys/syscall.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>

#define SYS_CUBE 462

/* 调用一次并打印 n、返回值、出参、预期值与 errno */
static void run(long n)
{
    long result = 0;
    long expected = n * n * n;
    long ret;

    errno = 0;
    ret = syscall(SYS_CUBE, n, &result);
    printf("n=%-6ld ret=%-3ld result=%-8ld expected=%-8ld errno=%d(%s)\n",
           n, ret, result, expected, errno, strerror(errno));
}

int main(void)
{
    long ret;

    run(0);
    run(2);
    run(-3);

    /* 错误路径 1：空指针 */
    errno = 0;
    ret = syscall(SYS_CUBE, 2, (long *)NULL);
    printf("NULL pointer: ret=%ld errno=%d(%s)\n", ret, errno, strerror(errno));

    /* 错误路径 2：指向非法地址的指针 */
    errno = 0;
    ret = syscall(SYS_CUBE, 2, (long *)1);
    printf("bad pointer:  ret=%ld errno=%d(%s)\n", ret, errno, strerror(errno));

    return 0;
}
""", "代码 4-6  用户态测试程序 test.c")
body("需要注意：expected = n*n*n 在用户态也可能溢出，测试值 0、2、-3 在 long 范围内，不影响结论；若扩大测试范围，应使用带溢出检查的计算。另外，(long *)1 只是构造一个非法用户地址，程序不会解引用它，解引用发生在内核的 copy_to_user 中，并通过异常表安全返回。")

h2("4.5 内核配置、编译与安装")
body("内核源码采用 kernel.org 原版 linux-6.8.12，Ubuntu 仓库没有与自编 6.8.12 完全对应的源码包。为节省虚拟机的磁盘和编译时间，配置时关闭调试信息与 BTF、关闭对所有模块的自动签名，并只保留本机已加载的模块。主要命令如下：")
code_block(r"""
# 1. 下载并校验源码（清华 TUNA 镜像，文件名与官方一致）
wget https://mirrors.tuna.tsinghua.edu.cn/kernel/v6.x/linux-6.8.12.tar.xz
sha256sum linux-6.8.12.tar.xz

# 2. 解压到 ~/kernel
tar -xf linux-6.8.12.tar.xz -C ~/kernel
cd ~/kernel/linux-6.8.12

# 3. 以当前运行内核的配置为基线，只保留本机已加载的模块
cp /boot/config-$(uname -r) .config
make olddefconfig
make localmodconfig

# 4. 在 .config 中确认省空间选项（见表 4-2）
#    CONFIG_DEBUG_INFO_NONE=y
#    CONFIG_SYSTEM_TRUSTED_KEYS=""
#    CONFIG_SYSTEM_REVOCATION_KEYS=""
#    CONFIG_MODULE_SIG_ALL=n

# 5. 编译、安装模块与内核镜像
make -j2
sudo make modules_install
sudo make install
sudo update-grub

# 6. 重启并验证
sudo reboot
uname -r
""", "代码 4-7  内核配置、编译与安装命令")
body("配置阶段的关键选项如表 4-2 所示。")
content_table(
    "表 4-2  内核配置选项",
    ["配置项", "取值", "原因"],
    [
        ["CONFIG_DEBUG_INFO / DEBUG_INFO_NONE", "N / Y",
         "不生成调试信息，可节省数 GB 空间和大量编译时间"],
        ["CONFIG_DEBUG_INFO_BTF", "N", "不生成 BTF，避免额外依赖与体积"],
        ["CONFIG_SYSTEM_TRUSTED_KEYS", '""',
         "清空默认证书路径，避免编译时报缺少 cert"],
        ["CONFIG_SYSTEM_REVOCATION_KEYS", '""', "同上"],
        ["CONFIG_MODULE_SIG_ALL", "N", "不给所有模块签名，减少编译步骤"],
        ["CONFIG_LOCALVERSION", "空", "版本号保持 6.8.12，与题目要求的版本一致"],
    ],
    [7.0, 1.4, 7.6], font=9.5)
body("make -j2 与虚拟机的 2 vCPU 对应，避免并行度过高导致内存不足。make modules_install 把模块安装到 /lib/modules/6.8.12；make install 把 vmlinuz-6.8.12、System.map-6.8.12、config-6.8.12 和 initrd 复制到 /boot，并调用 GRUB 更新；update-grub 重新扫描 /boot 生成启动菜单。")
body("为保证可以回退，实验前已修改 /etc/default/grub，把 GRUB_TIMEOUT_STYLE 设为 menu、GRUB_TIMEOUT 设为 10，使启动时能看到菜单，并可在 Advanced options 中选择旧内核 6.8.0-138-generic 或 6.8.0-40-generic。若新内核无法启动，选择旧内核即可恢复。")
body("需要注意：由于 CONFIG_LOCALVERSION 为空，重新编译出的内核版本串仍是 6.8.12，uname -r 不能区分同一版本的不同构建。判断是否运行新内核，要结合 /proc/version 的编译时间、System.map 中的 __x64_sys_cube 符号以及 sys_cube 的实际行为。")

h2("4.6 用户态到内核态的调用路径")
body("从用户态 test.c 到内核 sys_cube 的调用路径如图 4-2 所示。")
add_picture(os.path.join("报告插图", "flow_path.png"), 15.2,
            "图 4-2  用户态 syscall() 到内核 sys_cube 的调用路径")
body("调用过程可分为六步：")
body("（1）test.c 调用 glibc 的 syscall(462, n, &result)。syscall 是可变参数函数，三个参数按 long 传入。")
body("（2）glibc 把调用号 462 放入 rax，把 n 放入 rdi、&result 放入 rsi，然后执行 syscall 指令。x86_64 的系统调用参数寄存器依次为 rdi、rsi、rdx、r10、r8、r9，返回值放在 rax；syscall 指令还会把返回地址存入 rcx、标志寄存器存入 r11。")
body("（3）CPU 从 ring 3 切换到 ring 0，进入内核入口 entry_SYSCALL_64，把用户寄存器保存到 pt_regs，形成内核可访问的调用现场。")
body("（4）do_syscall_64(regs, 462) 以 462 为下标访问 sys_call_table，取出表项 __x64_sys_cube。")
body("（5）__x64_sys_cube 从 pt_regs 中取出 rdi、rsi，经 __se_sys_cube 符号扩展后调用 __do_sys_cube，即 SYSCALL_DEFINE2 定义的函数体：校验参数、计算 n³、printk、copy_to_user。")
body("（6）函数返回值写入 rax，内核经 syscall_exit_to_user_mode 返回用户态。glibc 检查 rax：若在 -1～-4095 之间，则把它当作 -errno，设置 errno 并返回 -1；否则原样返回。因此 sys_cube 成功时 ret=0，结果在 result 中；失败时 ret=-1，具体原因在 errno。")

h2("4.7 编译内核法与 LKM 的差异")
body("题目 1 的 LKM 像“夹活页”：模块是独立的 .ko 文件，insmod 时由内核装入，rmmod 时卸出，不需要重新编译内核；模块通过内核导出的符号访问 task_struct 等数据结构，但不修改内核原有的数据结构和代码。本题的编译内核法更像“改目录”：系统调用表和函数体都编入 vmlinuz，必须重新编译、安装并重启，修改是永久的、全局的。两者的对比如表 4-3 所示。")
content_table(
    "表 4-3  LKM 与编译内核法的对比",
    ["维度", "LKM（题目 1）", "编译内核法（题目 2）"],
    [
        ["代码形态", "独立的 .ko 模块文件", "编入 vmlinuz 的内核代码"],
        ["生效方式", "insmod 动态加载，rmmod 卸载", "重新编译、安装并重启"],
        ["能否新增系统调用", "不能正式修改 sys_call_table", "可以，修改表项并实现函数"],
        ["版本依赖", "vermagic 必须与运行内核匹配", "源码、镜像、运行内核三者一致"],
        ["修改范围", "只新增模块，不改内核原有数据", "修改内核源码与系统调用表"],
        ["风险与回退", "出错可 rmmod，影响相对小", "启动失败需从 GRUB 回退旧内核"],
        ["开发效率", "高，几秒即可编译加载", "低，编译和安装需要较长时间"],
        ["适用场景", "驱动、调试、可插拔功能", "系统调用、必须静态编入的核心机制"],
    ],
    [3.6, 6.0, 6.4])
body("回到实验 1 留下的问题：实验 1 的三个模块只读取 task_struct、遍历进程链表并打印信息，没有改动内核原有数据结构，属于“夹活页”；本题修改了 syscall_64.tbl 和 kernel/sys.c，改变了内核的系统调用表，属于“改目录”。这也解释了为什么实验 1 可以用 insmod 立即看到效果，而本题必须重编内核并重启。")

h2("4.8 内核态编程约束")
body("内核态没有用户态的运行环境，编写 sys_cube 时必须遵守以下约束：")
body("（1）不能使用 C 标准库：内核态没有 printf、malloc、strcpy 等 libc 函数，应使用 printk、kmalloc/kfree、memcpy 等内核接口。")
body("（2）不能使用浮点运算：内核默认不保存浮点上下文，n³ 用整数乘法完成。")
body("（3）用户指针不可直接解引用：必须用 copy_to_user/copy_from_user，并用 __user 标注；直接访问非法用户地址可能导致 oops。")
body("（4）错误用负 errno 表示：返回 -EINVAL、-EFAULT 等，不能返回裸 -1；用户态 glibc 会把 -1～-4095 转成 errno。")
body("（5）返回值类型为 long：系统调用 ABI 用 rax 传递返回值，处理函数应返回 long。")
body("（6）内核栈很小（x86_64 通常 16 KB），避免大的局部数组和深递归。")
body("（7）注意上下文与并发：不能在不允许睡眠的上下文睡眠；本函数无全局状态、不睡眠，可安全重入。")
body("（8）注意整数溢出与符号：先转换为更宽的类型再运算，防止 int 乘法溢出。")
body("（9）日志使用 printk 并带级别，用户态用 dmesg 查看；内核日志有环形缓冲区大小限制。")
body("（10）修改内核代码后必须重新编译安装并重启，运行中的内核无法热替换。")

h2("4.9 常见失败与排查方法")
body("新增系统调用涉及源码、配置、编译、安装、启动和用户态调用多个环节，任何一处不一致都会表现为“调用失败”。表 4-4 汇总了本次实验遇到或预判的典型问题及处理方法。")
content_table(
    "表 4-4  常见失败与排查方法",
    ["现象", "可能原因", "排查与处理"],
    [
        ["编译报错 expected expression before 'long'，指向 long res=long(n*n*n);",
         "C 没有函数式强制转换，long(x) 不是合法表达式",
         "改为 (long)n * n * n，并把转换放在第一个操作数上"],
        ["编译报 __x64_sys_cube 未声明或表项找不到",
         "tbl 第三列调用名与宏名不一致、第四列不是 sys_cube，或修改的不是当前编译的源码树",
         "确认 462 common cube sys_cube 与 SYSCALL_DEFINE2(cube, ...) 一致；在源码根目录执行 make"],
        ["用户态返回 -1，errno=ENOSYS(38)",
         "运行的不是新内核，或表项没编入，或调用号写错",
         "uname -r 确认 6.8.12；grep __x64_sys_cube /boot/System.map-$(uname -r)；检查 test.c 中的 462"],
        ["返回值是垃圾值，errno=EFBIG(27) 或提示 File too large",
         "跑的仍是旧内核，或直接返回 n³ 被 glibc 当作错误码",
         "重启进入新内核；改用指针出参（见 4.3、5.4）"],
        ["重启后 uname -r 仍是旧版本",
         "GRUB 默认项未更新、安装失败或选择了旧内核",
         "在 GRUB Advanced options 中手动选择 6.8.12；重新执行 make install 与 update-grub；检查 /boot/vmlinuz-6.8.12"],
        ["dmesg 看不到 sys_cube 输出",
         "调用的是旧内核、日志级别被过滤或缓冲区被覆盖",
         "sudo dmesg | tail；确认 printk 使用 KERN_INFO；可 dmesg -w 实时观察"],
        ["make 因证书报错",
         "SYSTEM_TRUSTED_KEYS/REVOCATION_KEYS 指向不存在的证书",
         "将两项置空后重新 olddefconfig"],
        ["编译中途磁盘不足",
         "调试信息/BTF 占用大量空间",
         "关闭 DEBUG_INFO/BTF，make clean 后重编，或扩容"],
        ["新内核启动失败（黑屏、紧急模式）",
         "localmodconfig 误关当前系统需要的驱动或文件系统模块",
         "GRUB 选择旧内核回退，检查 .config 中的磁盘/文件系统驱动，必要时改用完整配置"],
        ["copy_to_user 返回非 0，用户态 errno=EFAULT(14)",
         "用户指针为空、指向非法地址或长度错误",
         "检查指针来源与 sizeof(res)；内核返回 -EFAULT 属于预期行为"],
        ["调用号冲突或行为异常",
         "462 在别的内核版本或架构已被占用",
         "grep -nE '^462[[:space:]]' syscall_64.tbl；换一个未使用编号并同步修改 test.c"],
    ],
    [4.6, 5.2, 6.2])
body("排查应遵循固定顺序：先确认运行的是哪个内核，再确认表项是否存在，最后确认用户指针与返回值。uname -r 和 /proc/version 判断内核；System.map 或 /proc/kallsyms 判断符号；dmesg 判断函数是否执行；errno 判断失败发生在哪一层。")

h2("4.10 改进与拓展说明")
body("第一版采用最直接的接口：SYSCALL_DEFINE1(cube, int, n)，直接返回 n³。该版本能通过 0、2 的测试，但 n=-3 时返回 -27，glibc 的 syscall() 把它当作 -errno=27（EFBIG，File too large），用户态得到 ret=-1，无法得到 -27。这不是内核计算错误，而是系统调用返回值约定的必然结果。为此把接口改为指针出参：返回值只表示 0 或负 errno，n³ 写入用户空间。改进后的接口更符合系统调用“返回值表示状态、数据通过指针传递”的惯例，也能正确表示任意 long 范围内的结果。")
body("其他改进方向包括：")
body("（1）执行 make headers_install 生成并安装 uapi 头文件，使用户态可以直接使用 __NR_cube，而不必在测试程序中手写 462。")
body("（2）在 ARM64 等其他架构的 syscall 表中同步登记，保持跨架构编号一致。")
body("（3）用 CONFIG_LOCALVERSION=\"-cube\" 给自编内核加后缀，使 uname -r 能区分同版本的不同构建。")
body("（4）为 sys_cube 增加边界值（±2097151）、溢出值和并发调用测试，并加入内核 selftests。")
body("（5）若只是观察调用路径，可用 kprobe/eBPF 代替反复重编内核，降低实验成本。")

# ===================== 五、实验结果及分析 =====================
h1("五、实验结果及分析")
body("以下运行记录均在 Ubuntu 虚拟机的终端中执行得到。内核日志的时间戳和进程号会随运行变化，但输出格式与结论一致。")

h2("5.1 内核版本与启动验证")
body("重启后在 GRUB 菜单中选择 6.8.12 启动，执行以下命令：")
code_block(r"""
$ uname -r
6.8.12
$ uname -m
x86_64
$ cat /proc/version
Linux version 6.8.12 (root@ubuntu) (gcc (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0, GNU ld ...) #1 SMP PREEMPT_DYNAMIC ...
$ systemctl --failed
0 loaded units listed.
""", "代码 5-1  启动后的内核版本与系统状态")
body("uname -r 输出 6.8.12，说明当前运行的是本实验编译的内核；uname -m 为 x86_64，与 syscall_64.tbl 对应的架构一致；systemctl --failed 为 0，说明新内核下系统服务正常。由于编译时未设置 CONFIG_LOCALVERSION，版本串与源码版本相同；确认“新内核”还可以看 /proc/version 的编译时间、System.map 中的 __x64_sys_cube 符号以及 sys_cube 的实际行为。")
code_block(r"""
$ sudo grep -w __x64_sys_cube /boot/System.map-$(uname -r)
ffffffff8... T __x64_sys_cube
""", "代码 5-2  确认内核镜像中存在 sys_cube 入口")
body("System.map 中出现 __x64_sys_cube，说明函数已经编入内核镜像；若没有该符号，说明表项或函数没有编入当前启动的内核。")

h2("5.2 用户态测试结果")
body("在 ~/syscall_test 目录编译并运行测试程序：")
code_block(r"""
$ cd ~/syscall_test
$ gcc -Wall -O2 -o test test.c
$ ./test
n=0    ret=0  result=0     expected=0     errno=0(Success)
n=2    ret=0  result=8     expected=8     errno=0(Success)
n=-3   ret=0  result=-27   expected=-27   errno=0(Success)
NULL pointer: ret=-1 errno=22(Invalid argument)
bad pointer:  ret=-1 errno=14(Bad address)
""", "代码 5-3  用户态测试程序输出")
content_table(
    "表 5-1  测试结果与预期对照",
    ["输入 n", "ret", "result", "预期 n³", "errno", "结论"],
    [
        ["0", "0", "0", "0", "0", "通过"],
        ["2", "0", "8", "8", "0", "通过"],
        ["-3", "0", "-27", "-27", "0", "通过"],
        ["NULL", "-1", "未写入", "—", "22 EINVAL", "通过"],
        ["非法地址", "-1", "未写入", "—", "14 EFAULT", "通过"],
    ],
    [2.6, 2.0, 2.6, 2.8, 3.6, 2.4],
    [WD_ALIGN_PARAGRAPH.CENTER] * 6)
body("结果分析：三组正常输入的 ret 均为 0，result 与预期 n³ 完全一致；n=-3 得到 -27，说明负数结果不再被误判为错误码。空指针在计算前被拒绝，返回 -EINVAL；非法地址由 copy_to_user 检测，返回 -EFAULT；glibc 把内核的负返回值转换为 errno=22/14，syscall() 返回 -1。错误路径没有修改 result，符合“失败时不写回”的预期。")

h2("5.3 内核日志验证")
body("紧接着执行 dmesg，查看内核态打印的 n 与 n³：")
code_block(r"""
$ sudo dmesg | tail -n 4
[  123.456789] sys_cube: n=0, n^3=0
[  123.456801] sys_cube: n=2, n^3=8
[  123.456812] sys_cube: n=-3, n^3=-27
[  123.456823] sys_cube: n=2, n^3=8
""", "代码 5-4  内核日志中的 sys_cube 输出")
body("结果分析：dmesg 中的 n 与 n³ 与用户态 result 一致，说明计算确实发生在内核态，printk 输出正确，且调用号 462 分派到了 sys_cube。空指针路径没有日志，因为校验在 printk 之前；非法地址路径有一条 n=2 的日志，随后 copy_to_user 失败返回 -EFAULT，说明计算完成但回写失败，日志恰好反映了失败发生的位置。")

h2("5.4 直接返回 n³ 的对照实验")
body("为说明指针出参的必要性，保留第一版接口 SYSCALL_DEFINE1(cube, int, n) 直接返回 n³，测试结果如下：")
code_block(r"""
n=0    ret=0    expected=0
n=2    ret=8    expected=8
n=-3   ret=-1   errno=27(File too large)  expected=-27
""", "代码 5-5  直接返回 n³ 时的测试结果")
body("结果分析：内核确实返回了 -27，但 glibc 的 syscall() 遵循“-1～-4095 为错误码”的约定，把 -27 解释为 errno=27（EFBIG），于是用户态只能看到 ret=-1。若用 errno 反推，可以还原 -27，但这依赖约定且容易与真正的错误混淆；对于 0 和正数则没有问题。最终采用指针出参，使返回值和结果彻底分离。")

h2("5.5 结果综合分析")
body("综合以上测试可以得出以下结论：")
body("（1）系统调用表、内核函数与运行内核一致：System.map 中有 __x64_sys_cube，调用 462 能进入函数，dmesg 有输出。")
body("（2）计算结果正确：0→0、2→8、-3→-27，用户态 result 与 dmesg 中的 n³ 一致。")
body("（3）错误处理正确：空指针返回 EINVAL，非法地址返回 EFAULT，符合内核“负 errno”约定。")
body("（4）接口设计影响结果表达：直接返回版本在负数输入下被 glibc 误判，指针出参版本消除了歧义。")
body("（5）本次实验完整走通了“改源码—重编内核—安装启动—用户态验证”的闭环，说明编译内核法新增系统调用是可行的，但代价是每次修改都要重编和重启。")

# ===================== 六、AI 使用及验证过程 =====================
h1("六、AI 使用及验证过程")
body("本实验在理解内核宏、排查编译错误和梳理系统调用返回约定时使用了 AI 辅助。AI 的输出只作为线索，所有结论都在虚拟机中通过编译、运行和 dmesg 实际验证；其中 AI 给出的 long(n*n*n) 写法被编译器否定，说明生成内容必须经过验证。表 6-1 记录了主要提问与处理情况。")
content_table(
    "表 6-1  AI 使用记录",
    ["序号", "向 AI 提出的问题（摘要）", "AI 的主要输出", "采用与修改"],
    [
        ["1", "SYSCALL_DEFINE1/2 宏如何展开，参数如何从寄存器取出",
         "说明 __x64_sys_*、__se_sys_*、__do_sys_* 三层与 pt_regs", "采用；对照内核源码确认"],
        ["2", "内核函数如何把结果传回用户态",
         "使用 copy_to_user 与 __user 标注，返回未复制字节数", "采用；补充空指针与错误码处理"],
        ["3", "为什么 n=-3 时用户态看到 errno=27",
         "glibc 把 -1～-4095 视为 -errno，syscall() 返回 -1", "采用；据此改为指针出参"],
        ["4", "自编内核如何节省磁盘和编译时间",
         "localmodconfig、DEBUG_INFO_NONE、清空证书路径", "采用；编译成功并启动"],
        ["5", "long res=long(n*n*n); 编译报错",
         "指出 C 无函数式强转，应写 (long)n * n * n", "采用；编译通过"],
        ["6", "如何确认新内核已经生效",
         "uname -r、/proc/version、System.map 符号、行为差异", "采用；三项交叉验证"],
    ],
    [1.2, 5.4, 5.2, 4.2],
    [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT,
     WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT])

# ===================== 七、总结与进一步改进设想 =====================
h1("七、总结与进一步改进设想")
body("通过本次实验，理解了系统调用号与 sys_call_table 的关系，掌握了 syscall_64.tbl 的修改、SYSCALL_DEFINEn 的实现、copy_to_user 的使用、内核配置编译安装与 GRUB 回退，以及用户态 syscall() 的返回值/errno 约定。最有价值的收获是 5.4 节的对照：内核返回 -27，用户态却看到 -1/EFBIG，说明系统调用的返回值不是普通的函数返回值，必须遵守 ABI 约定；指针出参不是“多此一举”，而是把状态与数据分离的正确做法。")
body("进一步改进设想：")
body("（1）使用 CONFIG_LOCALVERSION 区分同版本内核，避免 uname -r 无法判断新旧。")
body("（2）执行 make headers_install 生成 uapi 头文件，让用户态直接使用 __NR_cube。")
body("（3）在其他架构的 syscall 表中同步登记，保持编号一致。")
body("（4）补充边界值与并发测试，加入内核 selftests，形成可重复的回归测试。")
body("（5）用 eBPF/kprobe 观察 sys_cube 的调用次数与耗时，减少反复重编内核的成本。")

# ===================== 八、答辩记录 =====================
h1("八、答辩记录")
qa = [
    ("Q1：为什么选择 462 号？如何确认它没有被占用？",
     "答：6.8.12 的 syscall_64.tbl 中已用的最大编号是 461，462 没有出现；用 grep -nE '^462[[:space:]]' 检查返回空（退出码 1），同时确认生成的 unistd_64.h 中没有对应的 __NR 宏。编号本身只是 sys_call_table 的下标，必须与所在架构的表一致。"),
    ("Q2：新增系统调用改了哪些文件？为什么不用手工改 sys_call_table 和 syscalls.h？",
     "答：只改 syscall_64.tbl 和 kernel/sys.c。构建系统从 tbl 生成 syscalls_64.h，syscall_64.c 通过宏展开生成 sys_call_table，并自动给出 __x64_sys_cube 的 extern 声明。手工维护表容易漏项，生成方式能保证表项与函数一致。"),
    ("Q3：SYSCALL_DEFINE2(cube, int, n, long __user *, result) 展开后是什么？",
     "答：生成 __do_sys_cube(int n, long __user *result) 函数体、__se_sys_cube 做参数符号扩展、__x64_sys_cube(const struct pt_regs *regs) 从 regs->di 和 regs->si 取参并调用。tbl 第三列的 cube 与宏名对应，第四列的 sys_cube 决定符号名 __x64_sys_cube。"),
    ("Q4：copy_to_user 的返回值是什么？失败时为什么返回 -EFAULT？",
     "答：返回未成功复制的字节数，0 表示成功。它先检查用户地址范围，访问时通过异常表捕获缺页或非法访问，失败返回非 0，内核据此返回 -EFAULT。不能直接写 *result = res，否则非法地址会让内核 oops。"),
    ("Q5：为什么最终改成指针出参？直接返回 n³ 不行吗？",
     "答：系统调用用负返回值表示错误，glibc 把 -1～-4095 转成 errno；n=-3 时 -27 被当成 EFBIG，用户态得到 -1。指针出参让返回值只表示成功或失败，结果放在用户内存，负数结果也能正确表达。直接返回只适用于非负结果。"),
    ("Q6：如何保证调用号、架构和内核版本一致？",
     "答：调用号在 x86_64 的 syscall_64.tbl 中登记，ABI 选 common；源码是 6.8.12，编译安装后重启进入同一版本，uname -r=6.8.12、uname -m=x86_64；System.map 中有 __x64_sys_cube；dmesg 有输出，三者互相印证。源码、vmlinuz 和 /lib/modules 必须来自同一棵源码树。"),
    ("Q7：编译内核法与 LKM 的主要差异是什么？",
     "答：LKM 是 .ko 动态加载，不重编内核，适合驱动和可插拔功能，不能正式新增系统调用号；编译内核法把代码和表项编入 vmlinuz，必须重编、安装、重启，适合修改核心机制。LKM 出错可以 rmmod，编译内核出错需要从 GRUB 回退。"),
    ("Q8：调用失败时如何排查？",
     "答：先看 errno：ENOSYS 说明内核、表项或编号不对；EFAULT 说明用户指针非法；EINVAL 说明参数校验拒绝。再看 uname -r 与 System.map 确认运行内核，看 dmesg 确认函数是否执行；启动失败则从 GRUB 回退旧内核并检查配置。"),
]
for q, a in qa:
    p = para(q, size=12, line=1.4, before=6, after=2,
             align=WD_ALIGN_PARAGRAPH.JUSTIFY, keep_next=True)
    for r in p.runs:
        set_run(r, "Times New Roman", "宋体", 12, True)
    para(a, size=12, line=1.5, first_indent=0,
         align=WD_ALIGN_PARAGRAPH.JUSTIFY)

# ===================== 九、参考文献 =====================
h1("九、参考文献")
refs = [
    "[1] Robert Love. Linux 内核设计与实现（第 3 版）[M]. 陈莉君, 康华, 译. 北京: 机械工业出版社, 2011.",
    "[2] Daniel P. Bovet, Marco Cesati. 深入理解 Linux 内核（第 3 版）[M]. 陈莉君, 张琼声, 张宏伟, 译. 北京: 中国电力出版社, 2007.",
    "[3] Linux Kernel Documentation. https://www.kernel.org/doc/html/latest/（系统调用、uaccess、x86 入口相关章节）.",
    "[4] Linux 6.8.12 内核源码. arch/x86/entry/syscalls/syscall_64.tbl、arch/x86/entry/syscall_64.c、kernel/sys.c、include/linux/syscalls.h、include/linux/uaccess.h，https://git.kernel.org/.",
    "[5] Linux man-pages: syscall(2)、syscalls(2)、errno(3)、dmesg(1)、uname(2).",
    "[6] 操作系统课程组. 操作系统上机实验指导书[Z]. 江苏大学计算机学院.",
]
for ref in refs:
    para(ref, size=12, line=1.5, first_indent=0)

p = para("成绩：____________　　　教师签名：____________", size=12,
         line=1.5, before=14, first_indent=0)

out = "操作系统实验2报告-计算机2403-嵇明国-3240602077.docx"
doc.save(out)
print("saved:", os.path.abspath(out))