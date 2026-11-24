# -*- coding: utf-8 -*-
"""生成实验2报告的两张流程图。"""
import matplotlib
matplotlib.use("Agg")                       # 无界面后端，直接输出 PNG
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]  # 中文字体
plt.rcParams["axes.unicode_minus"] = False  # 负号正常显示

NAVY = "#1F3864"                             # 主色：深蓝
FILL = "#D9E2F3"                             # 方框填充：浅蓝
TEXT = "#1F3864"


def box(ax, x, y, w, h, text, fill=FILL, fontsize=11, bold=False):
    """在归一化坐标 (x,y) 处画一个圆角框并写入文字。"""
    p = FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                       boxstyle="round,pad=0.012,rounding_size=0.02",
                       linewidth=1.4, edgecolor=NAVY, facecolor=fill)
    ax.add_patch(p)
    ax.text(x, y, text, ha="center", va="center", fontsize=fontsize,
            color=TEXT, fontweight="bold" if bold else "normal", linespacing=1.45)


def arrow(ax, p1, p2, style="-|>", ls="-"):
    """画一条带箭头的连线。"""
    a = FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=14,
                        linewidth=1.4, color=NAVY, linestyle=ls,
                        shrinkA=2, shrinkB=2)
    ax.add_patch(a)


# ---------------- 图 4-1 新增系统调用的整体流程 ----------------
fig, ax = plt.subplots(figsize=(10, 6.2), dpi=220)
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

w, h = 0.265, 0.175
xs = [0.17, 0.5, 0.83]
y1, y2, y3 = 0.80, 0.50, 0.20

box(ax, xs[0], y1, w, h, "1. 准备 linux-6.8.12 源码\n（kernel.org / TUNA 镜像）")
box(ax, xs[1], y1, w, h, "2. 生成省空间配置\nolddefconfig + localmodconfig")
box(ax, xs[2], y1, w, h, "3. 修改 syscall_64.tbl\n462 common cube sys_cube")
box(ax, xs[2], y2, w, h, "4. 实现内核函数\nSYSCALL_DEFINE2(cube, …)")
box(ax, xs[1], y2, w, h, "5. 编译内核\nmake -j2")
box(ax, xs[0], y2, w, h, "6. 安装内核与模块\nmodules_install / install")
box(ax, xs[0], y3, w, h, "7. 重启进入新内核\nupdate-grub → reboot")
box(ax, xs[1], y3, w, h, "8. 运行用户态测试\n./test 验证 0、2、-3")
box(ax, xs[2], y3, w, h, "9. 查看内核日志\ndmesg 核对 n 与 n³")

arrow(ax, (xs[0] + w / 2, y1), (xs[1] - w / 2, y1))
arrow(ax, (xs[1] + w / 2, y1), (xs[2] - w / 2, y1))
arrow(ax, (xs[2], y1 - h / 2), (xs[2], y2 + h / 2))
arrow(ax, (xs[2] - w / 2, y2), (xs[1] + w / 2, y2))
arrow(ax, (xs[1] - w / 2, y2), (xs[0] + w / 2, y2))
arrow(ax, (xs[0], y2 - h / 2), (xs[0], y3 + h / 2))
arrow(ax, (xs[0] + w / 2, y3), (xs[1] - w / 2, y3))
arrow(ax, (xs[1] + w / 2, y3), (xs[2] - w / 2, y3))

ax.text(0.5, 0.955, "新增系统调用（编译内核法）的完整流程",
        ha="center", va="center", fontsize=13, color=NAVY, fontweight="bold")
ax.text(0.5, 0.045, "源码与实现 → 编译与安装 → 启动与验证",
        ha="center", va="center", fontsize=10.5, color="#595959")
fig.tight_layout(pad=0.2)
fig.savefig("报告插图/flow_build.png", bbox_inches="tight", facecolor="white")
plt.close(fig)

# ---------------- 图 4-2 用户态到内核态的调用路径 ----------------
fig, ax = plt.subplots(figsize=(10, 6.8), dpi=220)
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

# 两个泳道背景
ax.add_patch(FancyBboxPatch((0.09, 0.665), 0.86, 0.285,
                            boxstyle="round,pad=0.008,rounding_size=0.02",
                            linewidth=1.0, edgecolor="#B4C6E7", facecolor="#EEF3FA"))
ax.add_patch(FancyBboxPatch((0.09, 0.045), 0.86, 0.575,
                            boxstyle="round,pad=0.008,rounding_size=0.02",
                            linewidth=1.0, edgecolor="#D0D0D0", facecolor="#F7F7F7"))
ax.text(0.115, 0.925, "用户态", ha="left", va="center", fontsize=11,
        color="#2F5597", fontweight="bold")
ax.text(0.115, 0.595, "内核态", ha="left", va="center", fontsize=11,
        color="#404040", fontweight="bold")

w, h = 0.255, 0.165
x1, x2, x3 = 0.19, 0.5, 0.81
yu, ym, yl = 0.795, 0.475, 0.165

box(ax, x1, yu, w, h, "用户程序 test.c\nsyscall(462, n, &result)")
box(ax, x2, yu, w, h, "glibc syscall()\nrax=462, rdi=n, rsi=&result")
box(ax, x3, yu, w, h, "执行 syscall 指令\nCPU 切换到 ring 0")

box(ax, x3, ym, w, h, "entry_SYSCALL_64\n保存现场到 pt_regs", fill="#E8E8E8")
box(ax, x2, ym, w, h, "do_syscall_64(regs, 462)\n按调用号查表", fill="#E8E8E8")
box(ax, x1, ym, w, h, "sys_call_table[462]\n→ __x64_sys_cube", fill="#E8E8E8")

box(ax, x1, yl, w, h, "SYSCALL_DEFINE2(cube, …)\n从 regs 取出 rdi / rsi", fill="#E8E8E8")
box(ax, x2, yl, w, h, "cube(n, result)\n校验 + 计算 n³ + printk", fill="#E8E8E8")
box(ax, x3, yl, w, h, "copy_to_user 写回结果\n返回 0 或 -errno", fill="#E8E8E8")

arrow(ax, (x1 + w / 2, yu), (x2 - w / 2, yu))
arrow(ax, (x2 + w / 2, yu), (x3 - w / 2, yu))
arrow(ax, (x3, yu - h / 2), (x3, ym + h / 2))
arrow(ax, (x3 - w / 2, ym), (x2 + w / 2, ym))
arrow(ax, (x2 - w / 2, ym), (x1 + w / 2, ym))
arrow(ax, (x1, ym - h / 2), (x1, yl + h / 2))
arrow(ax, (x1 + w / 2, yl), (x2 - w / 2, yl))
arrow(ax, (x2 + w / 2, yl), (x3 - w / 2, yl))

ax.text(0.5, 0.985, "用户态 syscall() 到内核 sys_cube 的调用路径",
        ha="center", va="center", fontsize=13, color=NAVY, fontweight="bold")
ax.text(0.5, 0.012, "返回：rax = 0（成功）或 -errno；glibc 把 -1～-4095 转为 errno，syscall() 返回 -1",
        ha="center", va="center", fontsize=10, color="#595959")
fig.tight_layout(pad=0.2)
fig.savefig("报告插图/flow_path.png", bbox_inches="tight", facecolor="white")
plt.close(fig)

print("figures done")