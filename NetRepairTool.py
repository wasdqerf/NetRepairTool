# -*- coding: utf-8 -*-
"""
Windows 11 网络故障恢复工具 - 中英双语 + 可配置测试目标
"""
import sys
import os
import re
import json
import base64
import ctypes
import subprocess
import threading
import datetime
import ipaddress
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog


# ============ 常量 ============
TEST_PORT = 443
CONFIG_DIR = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "NetRepairTool")
PROFILE_FILE = os.path.join(CONFIG_DIR, "profiles.json")
SETTINGS_FILE = os.path.join(CONFIG_DIR, "settings.json")

# 测试目标预设（翻译键, 主机名）
TEST_PRESETS = [
    ("preset_jd",     "www.jd.com"),
    ("preset_ms",     "www.microsoft.com"),
    ("preset_google", "www.google.com"),
    ("preset_baidu",  "www.baidu.com"),
]
DEFAULT_HOST = "www.jd.com"


# ============ 翻译表 ============
LANG = "zh"
SETTINGS = {"lang": "zh", "test_host": DEFAULT_HOST}

MESSAGES = {
    "zh": {
        "app_title": "Windows 11 网络故障恢复工具",
        "admin_ok": "✅ 管理员权限已就绪",
        "admin_no": "⚠️ 当前不是管理员权限（修复/重置/改IP不可用）",
        "btn_diagnose": "🔍  诊断网络",
        "btn_repair": "🔧  修复网络",
        "btn_reset": "🔄  重置网络",
        "btn_driver": "📋  检查驱动",
        "status_ready": "就绪",
        "tab_adapters": "  🖧 网卡状态  ",
        "tab_config": "  ⚙️ 网络配置  ",
        "tab_log": "  📄 详细日志  ",
        "adapter_hint": "点击上方【诊断网络】按钮，即可查看本机所有网卡状态、IP、DNS 等信息。",
        "clear_log": "清空日志",
        "welcome": "欢迎使用 Windows 11 网络故障恢复工具",
        "test_target_label": "测试目标：",
        "test_target": "连通性测试目标：{host}:{port}",
        "config_hint": "切换网络环境请用【网络配置】标签页。",
        "lang_btn_zh": "中文",
        "lang_btn_en": "English",
        "preset_jd": "京东",
        "preset_ms": "微软",
        "preset_google": "谷歌",
        "preset_baidu": "百度",
        "preset_custom": "自定义",
        "custom_host_hint": "（输入域名，如 www.qq.com）",
        # 配置页
        "config_adapter_label": "应用到网卡：",
        "config_refresh": "🔄 刷新网卡",
        "ip_group_title": "  IP 地址 ",
        "ip_mode_label": "获取方式：",
        "ip_dhcp": "自动获取（DHCP）",
        "ip_static": "手动设置（静态 IP）",
        "ip_label": "IP 地址：",
        "ip_hint": "例：10.173.200.123",
        "mask_label": "子网掩码：",
        "mask_hint": "例：255.255.0.0 或直接填 16",
        "gw_label": "默认网关：",
        "gw_hint": "例：10.173.11.254",
        "dns_group_title": "  DNS 服务器 ",
        "dns_mode_label": "获取方式：",
        "dns_dhcp": "自动获取",
        "dns_static": "手动指定",
        "dns1_label": "首选 DNS：",
        "dns1_hint": "例：10.30.6.66",
        "dns2_label": "备用 DNS：",
        "dns2_hint": "选填，可留空",
        "btn_apply_current": "💾  应用当前设置",
        "btn_save_profile": "📁  另存为配置",
        "profiles_list_title": "已保存的配置（点击按钮一键切换）：",
        "no_profiles": "（还没有保存的配置。填写上面的信息后，点【另存为配置】即可保存。）",
        "btn_apply_profile": "▶  应用",
        "btn_delete": "✕ 删除",
        "icon_home": "🏠",
        "icon_work": "🏢",
        "icon_mixed": "🔀",
        "msg_save_profile_title": "保存配置",
        "msg_save_profile_ask": "给这个配置起个名字（比如：公司、家里）：",
        "msg_ok_title": "成功",
        "msg_saved": "配置【{name}】已保存",
        "msg_save_fail": "保存配置文件失败",
        "msg_del_title": "删除配置",
        "msg_del_ask": "确定要删除配置【{name}】吗？",
        "msg_warn_title": "提示",
        "msg_pick_adapter": "请先选择要应用的网卡",
        "msg_format_err": "格式错误",
        "msg_ip_invalid": "IP 地址格式不正确",
        "msg_mask_empty": "子网掩码不能为空",
        "msg_gw_invalid": "默认网关格式不正确",
        "msg_dns_empty": "至少填一个 DNS 服务器",
        "msg_dns1_invalid": "首选 DNS 格式不正确",
        "msg_dns2_invalid": "备用 DNS 格式不正确",
        "msg_confirm_title": "确认",
        "msg_confirm_apply": "将网卡【{alias}】设置为：\n\n  IP：{ip}\n  子网掩码：{mask}\n  默认网关：{gw}\n  DNS：{dns}\n\n继续吗？",
        "msg_confirm_switch": "将网卡【{alias}】一键切换为【{name}】：\n\n  IP：{ip}\n  默认网关：{gw}\n  DNS：{dns}\n\n继续吗？",
        "auto": "自动获取",
        "auto_paren": "（自动）",
        "none_paren": "（无）",
        "msg_reset_title": "确认重置网络",
        "msg_reset_ask": "网络重置将修改 Winsock 和 TCP/IP 协议栈。\n完成后需要重启电脑才能完全生效。\n\n确定要继续吗？",
        "msg_need_admin_title": "需要管理员权限",
        "msg_need_admin_text": "此功能需要管理员权限。\n请关闭窗口，右键脚本 → 以管理员身份运行。",
        "lbl_ipv4": "IPv4 地址",
        "lbl_gw": "默认网关",
        "lbl_dns": "DNS 服务器",
        "lbl_speed": "连接速率",
        "lbl_mac": "MAC 地址",
        "lbl_drv_ver": "驱动版本",
        "lbl_drv_vendor": "驱动厂商",
        "no_adapters": "未检测到网卡信息（请尝试以管理员身份运行）",
        "adapters_count": "共检测到 {total} 张网卡，其中 {up} 张已连接",
        "virtual_mark": "[虚拟]",
        "unknown_adapter": "未知网卡",
        "st_up": "已连接", "st_disc": "未连接", "st_dis": "已禁用",
        "st_np": "未检测到（缺驱动）", "st_lower": "底层未就绪", "st_unknown": "未知状态",
        "tip_up": "正在正常使用中", "tip_disc": "未插网线或未连 WiFi",
        "tip_dis": "在设备管理器中禁用了", "tip_np": "驱动可能缺失或损坏",
        "tip_lower": "物理层异常",
        "diag_start": "开始网络诊断",
        "diag_reading": "读取网卡 / IP / DNS…",
        "diag_testing": "连通性测试 {host}…",
        "diag_adapters": "【网卡】共 {n} 张",
        "diag_conn": "【连通性测试：{host}:{port}】",
        "diag_icmp_ok": "  ICMP (ping)：✅ 通过",
        "diag_icmp_fail": "  ICMP (ping)：❌ 失败",
        "diag_tcp_ok": "  TCP  443  ：✅ 通过",
        "diag_tcp_fail": "  TCP  443  ：❌ 失败",
        "diag_conclusion": "【诊断结论】",
        "diag_ok": "  ✅ 网络连接正常，可以访问外网（{host} 可达）。",
        "diag_warn": "  ⚠️ 能 ping 通但 443 端口不通，可能是防火墙、代理或 VPN 拦截。",
        "diag_bad": "  ❌ 网络不通，建议点击【修复网络】，仍不行再【重置网络】。",
        "repair_start": "开始网络修复（不需重启）",
        "repair_step_1": "释放 IP 地址",
        "repair_step_2": "更新 IP 地址",
        "repair_step_3": "刷新 DNS 缓存",
        "repair_step_4": "重新注册 DNS",
        "step_running": "正在执行：{name}",
        "step_ok": "  ✅ 完成",
        "step_fail": "  ❌ 失败",
        "repair_done": "修复完成：{ok}/{total} 步成功",
        "reset_start": "开始网络重置（需重启生效）",
        "reset_step_1": "重置 Winsock",
        "reset_step_2": "重置 TCP/IP 协议栈",
        "reset_step_3": "重置 IPv4 接口",
        "reset_step_4": "重置 IPv6 接口",
        "reset_done": "重置完成：{ok}/{total} 步成功",
        "reset_restart": "⚠️ 请重启电脑，重置才能完全生效。",
        "drv_start": "网卡驱动检查",
        "drv_count": "共 {n} 张网卡",
        "drv_issues": "【发现的问题】",
        "drv_issue_np": "❌ {name}：未检测到硬件，驱动可能缺失或损坏",
        "drv_issue_dis": "⚠️ {name}：已被禁用，如需使用请在设备管理器启用",
        "drv_issue_disc": "⚠️ {name}：物理连接异常（未插网线或未连 WiFi）",
        "drv_issue_old": "⚠️ {name}：驱动日期 {date}（约 {years:.1f} 年前），建议去电脑品牌官网更新",
        "drv_ok": "✅ 未发现明显的驱动问题。",
        "apply_title_ip_dhcp_dns_dhcp": "IP 自动 + DNS 自动",
        "apply_title_ip_dhcp_dns_static": "IP 自动 + DNS 手动",
        "apply_title_ip_static_dns_dhcp": "IP 手动 + DNS 自动",
        "apply_title_ip_static_dns_static": "IP 手动 + DNS 手动",
        "apply_setting": "设置网卡【{alias}】：{desc}",
        "apply_ok": "✅ 设置已生效。",
        "apply_fail": "❌ 设置失败，可能是 IP 冲突或网卡被占用。",
        "apply_busy": "正在设置网卡【{alias}】…",
        "apply_busy_switch": "正在切换到【{name}】…",
        "busy_title": "提示",
        "busy_msg": "正在执行上一个任务，请稍候…",
        "elevate_title": "需要管理员权限",
        "elevate_ask": "本工具需要管理员权限才能修复/重置网络、修改 IP。\n\n是否立即以管理员身份重新启动？",
        "elevate_fail_title": "提权失败",
        "elevate_fail_text": "无法获取管理员权限，\n你仍可以使用【诊断网络】功能。",
    },
    "en": {
        "app_title": "Windows 11 Network Repair Tool",
        "admin_ok": "✅ Running as Administrator",
        "admin_no": "⚠️ Not running as Administrator (repair / reset / IP change disabled)",
        "btn_diagnose": "🔍  Diagnose",
        "btn_repair": "🔧  Repair",
        "btn_reset": "🔄  Reset",
        "btn_driver": "📋  Driver",
        "status_ready": "Ready",
        "tab_adapters": "  🖧 Adapters  ",
        "tab_config": "  ⚙️ Config  ",
        "tab_log": "  📄 Log  ",
        "adapter_hint": "Click 'Diagnose' above to view all network adapters, IP, DNS, etc.",
        "clear_log": "Clear Log",
        "welcome": "Welcome to Windows 11 Network Repair Tool",
        "test_target_label": "Test target: ",
        "test_target": "Connectivity test target: {host}:{port}",
        "config_hint": "Use the 'Config' tab to switch network environments.",
        "lang_btn_zh": "中文",
        "lang_btn_en": "English",
        "preset_jd": "JD.com",
        "preset_ms": "Microsoft",
        "preset_google": "Google",
        "preset_baidu": "Baidu",
        "preset_custom": "Custom",
        "custom_host_hint": "(enter domain, e.g. www.qq.com)",
        "config_adapter_label": "Apply to adapter: ",
        "config_refresh": "🔄 Refresh",
        "ip_group_title": "  IP Address ",
        "ip_mode_label": "Mode: ",
        "ip_dhcp": "Automatic (DHCP)",
        "ip_static": "Manual (Static IP)",
        "ip_label": "IP Address: ",
        "ip_hint": "e.g. 10.173.200.123",
        "mask_label": "Subnet Mask: ",
        "mask_hint": "e.g. 255.255.0.0 or 16",
        "gw_label": "Default Gateway: ",
        "gw_hint": "e.g. 10.173.11.254",
        "dns_group_title": "  DNS Servers ",
        "dns_mode_label": "Mode: ",
        "dns_dhcp": "Automatic",
        "dns_static": "Manual",
        "dns1_label": "Primary DNS: ",
        "dns1_hint": "e.g. 10.30.6.66",
        "dns2_label": "Secondary DNS: ",
        "dns2_hint": "Optional",
        "btn_apply_current": "💾  Apply Current",
        "btn_save_profile": "📁  Save as Profile",
        "profiles_list_title": "Saved profiles (click Apply for one-click switch):",
        "no_profiles": "(No profiles saved yet. Fill in above and click 'Save as Profile'.)",
        "btn_apply_profile": "▶  Apply",
        "btn_delete": "✕ Delete",
        "icon_home": "🏠",
        "icon_work": "🏢",
        "icon_mixed": "🔀",
        "msg_save_profile_title": "Save Profile",
        "msg_save_profile_ask": "Name this profile (e.g. Office, Home):",
        "msg_ok_title": "Success",
        "msg_saved": "Profile [{name}] saved",
        "msg_save_fail": "Failed to save profile",
        "msg_del_title": "Delete Profile",
        "msg_del_ask": "Delete profile [{name}]?",
        "msg_warn_title": "Notice",
        "msg_pick_adapter": "Please select an adapter first",
        "msg_format_err": "Invalid Format",
        "msg_ip_invalid": "Invalid IP address",
        "msg_mask_empty": "Subnet mask cannot be empty",
        "msg_gw_invalid": "Invalid default gateway",
        "msg_dns_empty": "At least one DNS server is required",
        "msg_dns1_invalid": "Invalid primary DNS",
        "msg_dns2_invalid": "Invalid secondary DNS",
        "msg_confirm_title": "Confirm",
        "msg_confirm_apply": "Set adapter [{alias}] to:\n\n  IP: {ip}\n  Mask: {mask}\n  Gateway: {gw}\n  DNS: {dns}\n\nContinue?",
        "msg_confirm_switch": "Switch adapter [{alias}] to profile [{name}]:\n\n  IP: {ip}\n  Gateway: {gw}\n  DNS: {dns}\n\nContinue?",
        "auto": "Automatic",
        "auto_paren": "(auto)",
        "none_paren": "(none)",
        "msg_reset_title": "Confirm Network Reset",
        "msg_reset_ask": "Network reset will modify Winsock and TCP/IP stack.\nA reboot is required for the changes to take effect.\n\nContinue?",
        "msg_need_admin_title": "Administrator Required",
        "msg_need_admin_text": "This feature requires Administrator privileges.\nPlease close and relaunch as Administrator.",
        "lbl_ipv4": "IPv4 Address",
        "lbl_gw": "Default Gateway",
        "lbl_dns": "DNS Servers",
        "lbl_speed": "Link Speed",
        "lbl_mac": "MAC Address",
        "lbl_drv_ver": "Driver Version",
        "lbl_drv_vendor": "Driver Vendor",
        "no_adapters": "No adapters detected (try running as Administrator)",
        "adapters_count": "{total} adapters found, {up} connected",
        "virtual_mark": "[Virtual]",
        "unknown_adapter": "Unknown adapter",
        "st_up": "Connected", "st_disc": "Disconnected", "st_dis": "Disabled",
        "st_np": "Not Present (driver missing)", "st_lower": "Lower layer down",
        "st_unknown": "Unknown",
        "tip_up": "Working normally", "tip_disc": "No cable or WiFi",
        "tip_dis": "Disabled in Device Manager", "tip_np": "Driver may be missing or corrupted",
        "tip_lower": "Physical layer error",
        "diag_start": "Starting network diagnosis",
        "diag_reading": "Reading adapters / IP / DNS…",
        "diag_testing": "Testing connectivity to {host}…",
        "diag_adapters": "[Adapters] {n} found",
        "diag_conn": "[Connectivity test: {host}:{port}]",
        "diag_icmp_ok": "  ICMP (ping): ✅ OK",
        "diag_icmp_fail": "  ICMP (ping): ❌ Failed",
        "diag_tcp_ok": "  TCP  443  : ✅ OK",
        "diag_tcp_fail": "  TCP  443  : ❌ Failed",
        "diag_conclusion": "[Conclusion]",
        "diag_ok": "  ✅ Network is working fine ({host} reachable).",
        "diag_warn": "  ⚠️ Ping OK but TCP 443 blocked. Firewall / proxy / VPN may be involved.",
        "diag_bad": "  ❌ Network is down. Try [Repair], then [Reset] if needed.",
        "repair_start": "Starting network repair (no reboot needed)",
        "repair_step_1": "Release IP",
        "repair_step_2": "Renew IP",
        "repair_step_3": "Flush DNS",
        "repair_step_4": "Register DNS",
        "step_running": "Running: {name}",
        "step_ok": "  ✅ Done",
        "step_fail": "  ❌ Failed",
        "repair_done": "Repair finished: {ok}/{total} steps OK",
        "reset_start": "Starting network reset (reboot required)",
        "reset_step_1": "Reset Winsock",
        "reset_step_2": "Reset TCP/IP stack",
        "reset_step_3": "Reset IPv4 interface",
        "reset_step_4": "Reset IPv6 interface",
        "reset_done": "Reset finished: {ok}/{total} steps OK",
        "reset_restart": "⚠️ Please reboot to fully apply the changes.",
        "drv_start": "Network driver check",
        "drv_count": "{n} adapters total",
        "drv_issues": "[Issues found]",
        "drv_issue_np": "❌ {name}: hardware not present, driver may be missing",
        "drv_issue_dis": "⚠️ {name}: disabled, enable it in Device Manager if needed",
        "drv_issue_disc": "⚠️ {name}: physical link down (no cable / no WiFi)",
        "drv_issue_old": "⚠️ {name}: driver dated {date} (~{years:.1f} years old), consider updating",
        "drv_ok": "✅ No obvious driver issues found.",
        "apply_title_ip_dhcp_dns_dhcp": "IP Auto + DNS Auto",
        "apply_title_ip_dhcp_dns_static": "IP Auto + DNS Manual",
        "apply_title_ip_static_dns_dhcp": "IP Manual + DNS Auto",
        "apply_title_ip_static_dns_static": "IP Manual + DNS Manual",
        "apply_setting": "Configuring adapter [{alias}]: {desc}",
        "apply_ok": "✅ Settings applied.",
        "apply_fail": "❌ Failed. Possibly IP conflict or adapter in use.",
        "apply_busy": "Configuring adapter [{alias}]…",
        "apply_busy_switch": "Switching to [{name}]…",
        "busy_title": "Notice",
        "busy_msg": "Another task is running, please wait…",
        "elevate_title": "Administrator Required",
        "elevate_ask": "This tool requires Administrator privileges.\n\nRelaunch as Administrator now?",
        "elevate_fail_title": "Elevation Failed",
        "elevate_fail_text": "Failed to gain Administrator privileges.\nYou can still use [Diagnose].",
    }
}


def t(key, **kwargs):
    s = MESSAGES.get(LANG, MESSAGES["zh"]).get(key, key)
    if kwargs:
        try:
            return s.format(**kwargs)
        except Exception:
            return s
    return s


# ============ 设置读写 ============
def load_settings():
    global LANG
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                LANG = data.get("lang", "zh")
                if LANG not in ("zh", "en"):
                    LANG = "zh"
                SETTINGS["lang"] = LANG
                SETTINGS["test_host"] = data.get("test_host", DEFAULT_HOST) or DEFAULT_HOST
    except Exception:
        pass


def save_settings():
    try:
        os.makedirs(CONFIG_DIR, exist_ok=True)
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump({"lang": LANG, "test_host": SETTINGS.get("test_host", DEFAULT_HOST)},
                      f, ensure_ascii=False, indent=2)
    except Exception:
        pass


# ============ 配置管理 ============
def load_profiles():
    try:
        if os.path.exists(PROFILE_FILE):
            with open(PROFILE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for name, prof in data.items():
                    if "ip_mode" not in prof and "dns_mode" not in prof:
                        old = prof.get("mode", "dhcp")
                        prof["ip_mode"] = old
                        prof["dns_mode"] = old
                return data
    except Exception:
        pass
    return {}


def save_profiles(profiles):
    try:
        os.makedirs(CONFIG_DIR, exist_ok=True)
        with open(PROFILE_FILE, "w", encoding="utf-8") as f:
            json.dump(profiles, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False


def is_valid_ipv4(s):
    if not s:
        return False
    parts = s.split(".")
    if len(parts) != 4:
        return False
    for p in parts:
        if not p.isdigit() or not (0 <= int(p) <= 255):
            return False
    return True


def mask_to_prefix(mask):
    mask = (mask or "").strip()
    if not mask:
        return 24
    try:
        if mask.isdigit():
            v = int(mask)
            if 0 <= v <= 32:
                return v
    except Exception:
        pass
    try:
        return ipaddress.IPv4Network(f"0.0.0.0/{mask}", strict=False).prefixlen
    except Exception:
        return 24


def ps_quote(s):
    if s is None:
        return "''"
    return "'" + str(s).replace("'", "''") + "'"


# ============ 管理员权限 ============
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False


def run_as_admin():
    script = os.path.abspath(sys.argv[0])
    params = " ".join([f'"{a}"' for a in sys.argv[1:]])
    try:
        ret = ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, f'"{script}" {params}', None, 1
        )
        return int(ret) > 32
    except Exception:
        return False


# ============ 命令执行 ============
CREATE_NO_WINDOW = 0x08000000


def run_cmd(cmd, timeout=120, encoding="gbk"):
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True,
            encoding=encoding, errors="replace", timeout=timeout,
            creationflags=CREATE_NO_WINDOW,
        )
        out = (result.stdout or "") + (result.stderr or "")
        return result.returncode == 0, out.strip()
    except subprocess.TimeoutExpired:
        return False, f"Timeout ({timeout}s)"
    except Exception as e:
        return False, f"Error: {e}"


def run_ps(ps_code, timeout=120):
    prefix = ("[Console]::OutputEncoding=[System.Text.Encoding]::UTF8; "
              "$OutputEncoding=[System.Text.Encoding]::UTF8; ")
    full = prefix + ps_code
    encoded = base64.b64encode(full.encode("utf-16-le")).decode("ascii")
    cmd = f"powershell -NoProfile -NonInteractive -EncodedCommand {encoded}"
    return run_cmd(cmd, timeout=timeout, encoding="utf-8")


# ============ 可滚动容器 ============
class ScrollableFrame(tk.Frame):
    def __init__(self, parent, bg="#1e1e2e", **kwargs):
        super().__init__(parent, bg=bg, **kwargs)
        self.canvas = tk.Canvas(self, bg=bg, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical",
                                      command=self.canvas.yview)
        self.inner = tk.Frame(self.canvas, bg=bg)
        self._win = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.inner.bind("<Configure>",
                        lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>",
                         lambda e: self.canvas.itemconfig(self._win, width=e.width))
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.bind_all("<MouseWheel>", self._wheel)

    def _wheel(self, event):
        try:
            self.canvas.yview_scroll(int(-event.delta / 120), "units")
        except Exception:
            pass


# ============ 主应用 ============
class NetRepairApp:
    def __init__(self, root):
        self.root = root
        self._busy = False
        self._adapter_cache = []
        self.profiles = load_profiles()
        self._build_all()

    def _build_all(self):
        self.root.title(t("app_title"))
        self.root.geometry("1000x810")
        self.root.minsize(920, 700)
        self.root.configure(bg="#f5f5f5")
        for w in self.root.winfo_children():
            w.destroy()
        self._build_ui()

    def _build_ui(self):
        # 顶部：权限 + 语言
        top = tk.Frame(self.root, bg="#1e1e2e", height=42)
        top.pack(fill="x")
        txt = t("admin_ok") if is_admin() else t("admin_no")
        col = "#4caf50" if is_admin() else "#ffb300"
        tk.Label(top, text=txt, bg="#1e1e2e", fg=col,
                 font=("微软雅黑", 11, "bold")).pack(side="left", padx=15, pady=9)

        lang_frame = tk.Frame(top, bg="#1e1e2e")
        lang_frame.pack(side="right", padx=12)
        cur = LANG
        for code, label_key in [("zh", "lang_btn_zh"), ("en", "lang_btn_en")]:
            tk.Button(
                lang_frame, text=t(label_key),
                command=lambda c=code: self._switch_lang(c),
                bg="#3b8ed0" if cur == code else "#333",
                fg="white", activebackground="#3b8ed0",
                activeforeground="white", relief="flat",
                font=("微软雅黑", 10), cursor="hand2",
                padx=10, pady=3, bd=0,
            ).pack(side="left", padx=2)

        # 按钮区
        bf = tk.Frame(self.root, bg="#f5f5f5")
        bf.pack(fill="x", padx=12, pady=(12, 6))
        btns = [
            (t("btn_diagnose"), "#3b8ed0", self.on_diagnose),
            (t("btn_repair"), "#1f6aa5", self.on_repair),
            (t("btn_reset"), "#c44536", self.on_reset),
            (t("btn_driver"), "#2b7a4b", self.on_driver),
        ]
        for text, color, cmd in btns:
            tk.Button(
                bf, text=text, command=cmd,
                bg=color, fg="white", activebackground=color,
                activeforeground="white", font=("微软雅黑", 12, "bold"),
                relief="flat", cursor="hand2", width=14, height=2, bd=0,
            ).pack(side="left", padx=6)

        # 测试目标行
        target_row = tk.Frame(self.root, bg="#f5f5f5")
        target_row.pack(fill="x", padx=18, pady=(2, 6))
        tk.Label(target_row, text=t("test_target_label"), bg="#f5f5f5",
                 fg="#333", font=("微软雅黑", 10)).pack(side="left")

        self.target_combo_var = tk.StringVar()
        self.target_combo = ttk.Combobox(
            target_row, textvariable=self.target_combo_var,
            state="readonly", width=12, font=("微软雅黑", 10)
        )
        self.target_combo.pack(side="left", padx=6)
        self.target_combo.bind("<<ComboboxSelected>>", self._on_target_changed)

        self.custom_host_var = tk.StringVar()
        self.custom_host_entry = tk.Entry(
            target_row, textvariable=self.custom_host_var,
            width=32, font=("Consolas", 10)
        )
        self.custom_host_entry.pack(side="left", padx=6)
        self.custom_host_entry.bind("<FocusOut>", lambda e: self._save_target_setting())
        self.custom_host_entry.bind("<Return>", lambda e: self._save_target_setting())

        self.target_hint = tk.Label(target_row, text=t("custom_host_hint"),
                                    bg="#f5f5f5", fg="#888",
                                    font=("微软雅黑", 9))
        self.target_hint.pack(side="left", padx=6)

        # 状态 + 进度
        self.status_var = tk.StringVar(value=t("status_ready"))
        tk.Label(self.root, textvariable=self.status_var, anchor="w",
                 bg="#f5f5f5", fg="#333",
                 font=("微软雅黑", 10)).pack(fill="x", padx=18)
        self.progress = ttk.Progressbar(self.root, mode="determinate")
        self.progress.pack(fill="x", padx=16, pady=(4, 10))

        style = ttk.Style()
        try:
            style.theme_use("default")
        except Exception:
            pass

        self.nb = ttk.Notebook(self.root)
        self.nb.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        # Tab1
        tab1 = tk.Frame(self.nb, bg="#1e1e2e")
        self.nb.add(tab1, text=t("tab_adapters"))
        self.adapter_box = ScrollableFrame(tab1)
        self.adapter_box.pack(fill="both", expand=True)
        tk.Label(self.adapter_box.inner, text=t("adapter_hint"),
                 bg="#1e1e2e", fg="#888",
                 font=("微软雅黑", 11)).pack(pady=30)

        # Tab2
        tab2 = tk.Frame(self.nb, bg="#f5f5f5")
        self.nb.add(tab2, text=t("tab_config"))
        self._build_config_tab(tab2)

        # Tab3
        tab3 = tk.Frame(self.nb, bg="#1e1e1e")
        self.nb.add(tab3, text=t("tab_log"))
        self.log = scrolledtext.ScrolledText(
            tab3, wrap="word", font=("Consolas", 10),
            bg="#1e1e1e", fg="#e0e0e0", insertbackground="white",
            relief="flat", bd=0,
        )
        self.log.pack(fill="both", expand=True, padx=6, pady=6)
        for tag, c in [("info", "#82aaff"), ("success", "#7bd88f"),
                       ("warn", "#ffb86c"), ("error", "#ff6e6e"),
                       ("head", "#c792ea")]:
            self.log.tag_config(tag, foreground=c)
        self.log.tag_config("head", font=("Consolas", 11, "bold"))

        # 底部
        bottom = tk.Frame(self.root, bg="#f5f5f5")
        bottom.pack(fill="x", padx=16, pady=(0, 10))
        tk.Button(bottom, text=t("clear_log"), command=self.clear_log,
                  font=("微软雅黑", 10), width=12,
                  relief="flat", bg="#e0e0e0", cursor="hand2"
                  ).pack(side="right")

        self.write(t("welcome") + "\n", "head")
        self.write(t("test_target", host=self._get_current_host(), port=TEST_PORT) + "\n", "info")
        self.write(t("config_hint") + "\n\n", "info")

        # 初始化目标选择器
        self._init_target_selector()
        self.root.after(500, self._refresh_adapter_combo)

    # ---------- 测试目标 ----------
    def _init_target_selector(self):
        display_names = [t(k) for k, _ in TEST_PRESETS] + [t("preset_custom")]
        self.target_combo["values"] = display_names

        saved_host = SETTINGS.get("test_host", DEFAULT_HOST)
        matched = False
        for i, (_, host) in enumerate(TEST_PRESETS):
            if host == saved_host:
                self.target_combo_var.set(display_names[i])
                matched = True
                break
        if not matched:
            self.target_combo_var.set(t("preset_custom"))
        self.custom_host_var.set(saved_host)
        self._update_custom_state()

    def _on_target_changed(self, event=None):
        display = self.target_combo_var.get()
        if display != t("preset_custom"):
            for k, host in TEST_PRESETS:
                if t(k) == display:
                    self.custom_host_var.set(host)
                    break
        self._update_custom_state()
        self._save_target_setting()

    def _update_custom_state(self):
        if self.target_combo_var.get() == t("preset_custom"):
            self.custom_host_entry.configure(state="normal", bg="white")
        else:
            self.custom_host_entry.configure(state="readonly", bg="#f0f0f0")

    def _get_current_host(self):
        h = self.custom_host_var.get().strip()
        return h or DEFAULT_HOST

    def _save_target_setting(self):
        SETTINGS["test_host"] = self._get_current_host()
        save_settings()

    def _switch_lang(self, code):
        global LANG
        if code == LANG:
            return
        LANG = code
        SETTINGS["lang"] = code
        save_settings()
        snapshot = self._snapshot_form()
        self._build_all()
        self._restore_form(snapshot)

    def _snapshot_form(self):
        try:
            return {
                "adapter": self.config_adapter_var.get(),
                "ip_mode": self.ip_mode_var.get(),
                "dns_mode": self.dns_mode_var.get(),
                "ip": self.ip_var.get(),
                "mask": self.mask_var.get(),
                "gateway": self.gateway_var.get(),
                "dns1": self.dns1_var.get(),
                "dns2": self.dns2_var.get(),
            }
        except Exception:
            return {}

    def _restore_form(self, snap):
        if not snap:
            return
        try:
            if snap.get("adapter") and snap["adapter"] in self.config_adapter_combo["values"]:
                self.config_adapter_var.set(snap["adapter"])
            if snap.get("ip_mode"):
                self.ip_mode_var.set(snap["ip_mode"])
            if snap.get("dns_mode"):
                self.dns_mode_var.set(snap["dns_mode"])
            self.ip_var.set(snap.get("ip", ""))
            self.mask_var.set(snap.get("mask", ""))
            self.gateway_var.set(snap.get("gateway", ""))
            self.dns1_var.set(snap.get("dns1", ""))
            self.dns2_var.set(snap.get("dns2", ""))
            self._toggle_mode()
        except Exception:
            pass

    # ============ 网络配置标签页 ============
    def _build_config_tab(self, parent):
        row1 = tk.Frame(parent, bg="#f5f5f5")
        row1.pack(fill="x", padx=18, pady=(14, 6))
        tk.Label(row1, text=t("config_adapter_label"), bg="#f5f5f5",
                 font=("微软雅黑", 11)).pack(side="left")
        self.config_adapter_var = tk.StringVar()
        self.config_adapter_combo = ttk.Combobox(
            row1, textvariable=self.config_adapter_var,
            state="readonly", width=32, font=("微软雅黑", 10)
        )
        self.config_adapter_combo.pack(side="left", padx=6)
        tk.Button(row1, text=t("config_refresh"), command=self._refresh_adapter_combo,
                  font=("微软雅黑", 10), relief="flat", bg="#e0e0e0",
                  cursor="hand2").pack(side="left", padx=6)

        ip_group = tk.LabelFrame(parent, text=t("ip_group_title"),
                                 bg="#f5f5f5", font=("微软雅黑", 10, "bold"),
                                 fg="#2b5f9f", padx=14, pady=8)
        ip_group.pack(fill="x", padx=18, pady=(6, 4))

        ip_mode_row = tk.Frame(ip_group, bg="#f5f5f5")
        ip_mode_row.pack(fill="x")
        tk.Label(ip_mode_row, text=t("ip_mode_label"), bg="#f5f5f5",
                 font=("微软雅黑", 10), width=12, anchor="e").pack(side="left")
        self.ip_mode_var = tk.StringVar(value="dhcp")
        tk.Radiobutton(ip_mode_row, text=t("ip_dhcp"),
                       variable=self.ip_mode_var, value="dhcp",
                       bg="#f5f5f5", font=("微软雅黑", 10),
                       command=self._toggle_mode).pack(side="left", padx=(0, 10))
        tk.Radiobutton(ip_mode_row, text=t("ip_static"),
                       variable=self.ip_mode_var, value="static",
                       bg="#f5f5f5", font=("微软雅黑", 10),
                       command=self._toggle_mode).pack(side="left")

        self.ip_var = tk.StringVar()
        self.mask_var = tk.StringVar(value="255.255.0.0")
        self.gateway_var = tk.StringVar()

        self._ip_widgets = []
        self._add_form_row(ip_group, t("ip_label"), self.ip_var,
                           t("ip_hint"), self._ip_widgets)
        self._add_form_row(ip_group, t("mask_label"), self.mask_var,
                           t("mask_hint"), self._ip_widgets)
        self._add_form_row(ip_group, t("gw_label"), self.gateway_var,
                           t("gw_hint"), self._ip_widgets)

        dns_group = tk.LabelFrame(parent, text=t("dns_group_title"),
                                  bg="#f5f5f5", font=("微软雅黑", 10, "bold"),
                                  fg="#2b5f9f", padx=14, pady=8)
        dns_group.pack(fill="x", padx=18, pady=(4, 6))

        dns_mode_row = tk.Frame(dns_group, bg="#f5f5f5")
        dns_mode_row.pack(fill="x")
        tk.Label(dns_mode_row, text=t("dns_mode_label"), bg="#f5f5f5",
                 font=("微软雅黑", 10), width=12, anchor="e").pack(side="left")
        self.dns_mode_var = tk.StringVar(value="dhcp")
        tk.Radiobutton(dns_mode_row, text=t("dns_dhcp"),
                       variable=self.dns_mode_var, value="dhcp",
                       bg="#f5f5f5", font=("微软雅黑", 10),
                       command=self._toggle_mode).pack(side="left", padx=(0, 10))
        tk.Radiobutton(dns_mode_row, text=t("dns_static"),
                       variable=self.dns_mode_var, value="static",
                       bg="#f5f5f5", font=("微软雅黑", 10),
                       command=self._toggle_mode).pack(side="left")

        self.dns1_var = tk.StringVar()
        self.dns2_var = tk.StringVar()

        self._dns_widgets = []
        self._add_form_row(dns_group, t("dns1_label"), self.dns1_var,
                           t("dns1_hint"), self._dns_widgets)
        self._add_form_row(dns_group, t("dns2_label"), self.dns2_var,
                           t("dns2_hint"), self._dns_widgets)

        row3 = tk.Frame(parent, bg="#f5f5f5")
        row3.pack(fill="x", padx=18, pady=(6, 6))
        tk.Button(row3, text=t("btn_apply_current"), command=self._on_apply_current,
                  bg="#1f6aa5", fg="white", activebackground="#1f6aa5",
                  activeforeground="white", font=("微软雅黑", 11, "bold"),
                  relief="flat", cursor="hand2", width=18, height=2, bd=0,
                  ).pack(side="left", padx=(0, 8))
        tk.Button(row3, text=t("btn_save_profile"), command=self._on_save_profile,
                  bg="#2b7a4b", fg="white", activebackground="#2b7a4b",
                  activeforeground="white", font=("微软雅黑", 11, "bold"),
                  relief="flat", cursor="hand2", width=18, height=2, bd=0,
                  ).pack(side="left", padx=8)

        tk.Label(parent, text=t("profiles_list_title"),
                 bg="#f5f5f5", fg="#333",
                 font=("微软雅黑", 11, "bold")
                 ).pack(anchor="w", padx=18, pady=(12, 4))

        self.profile_frame = tk.Frame(parent, bg="#f5f5f5")
        self.profile_frame.pack(fill="both", expand=True, padx=18, pady=(0, 14))

        self._toggle_mode()
        self._render_profile_list()

    def _add_form_row(self, parent, label, var, hint, widget_list):
        row = tk.Frame(parent, bg="#f5f5f5")
        row.pack(fill="x", pady=3)
        tk.Label(row, text=label, bg="#f5f5f5",
                 font=("微软雅黑", 10), width=12, anchor="e"
                 ).pack(side="left", padx=(0, 8))
        e = tk.Entry(row, textvariable=var, width=26, font=("Consolas", 11))
        e.pack(side="left")
        tk.Label(row, text=hint, bg="#f5f5f5", fg="#888",
                 font=("微软雅黑", 9)).pack(side="left", padx=10)
        widget_list.append(e)

    def _toggle_mode(self):
        ip_state = "normal" if self.ip_mode_var.get() == "static" else "disabled"
        for w in self._ip_widgets:
            try:
                w.configure(state=ip_state)
            except Exception:
                pass
        dns_state = "normal" if self.dns_mode_var.get() == "static" else "disabled"
        for w in self._dns_widgets:
            try:
                w.configure(state=dns_state)
            except Exception:
                pass

    def _refresh_adapter_combo(self):
        def worker():
            adapters = self._get_adapters()
            names = [a.get("Name") for a in adapters if a.get("Name")]
            def apply():
                try:
                    self.config_adapter_combo["values"] = names
                    cur = self.config_adapter_var.get()
                    if cur not in names:
                        picked = ""
                        for a in adapters:
                            if a.get("Status") == "Up":
                                picked = a.get("Name")
                                break
                        if not picked and names:
                            picked = names[0]
                        self.config_adapter_var.set(picked)
                except Exception:
                    pass
            self.root.after(0, apply)
        threading.Thread(target=worker, daemon=True).start()

    def _render_profile_list(self):
        for w in self.profile_frame.winfo_children():
            w.destroy()

        if not self.profiles:
            tk.Label(self.profile_frame, text=t("no_profiles"),
                     bg="#f5f5f5", fg="#888",
                     font=("微软雅黑", 10)).pack(anchor="w", pady=6)
            return

        for name, prof in self.profiles.items():
            row = tk.Frame(self.profile_frame, bg="white",
                           highlightthickness=1, highlightbackground="#ddd")
            row.pack(fill="x", pady=4)

            ip_mode = prof.get("ip_mode", "dhcp")
            dns_mode = prof.get("dns_mode", "dhcp")

            if ip_mode == "dhcp" and dns_mode == "dhcp":
                icon = t("icon_home")
            elif ip_mode == "static" and dns_mode == "static":
                icon = t("icon_work")
            else:
                icon = t("icon_mixed")

            ip_desc = t("auto") if ip_mode == "dhcp" else f"IP {prof.get('ip', '')}"
            if dns_mode == "dhcp":
                dns_desc = "DNS " + t("auto")
            else:
                d = prof.get("dns1", "")
                dns_desc = f"DNS {d}" if d else "DNS"
            desc = f"{ip_desc}  |  {dns_desc}"
            if prof.get("gateway"):
                desc += f"  |  GW {prof.get('gateway')}"

            tk.Label(row, text=icon, bg="white",
                     font=("Arial", 18)).pack(side="left", padx=(12, 6), pady=8)

            info = tk.Frame(row, bg="white")
            info.pack(side="left", fill="x", expand=True, pady=6)
            tk.Label(info, text=name, bg="white", fg="#222",
                     font=("微软雅黑", 12, "bold"), anchor="w"
                     ).pack(anchor="w")
            tk.Label(info, text=desc, bg="white", fg="#666",
                     font=("Consolas", 9), anchor="w"
                     ).pack(anchor="w")

            tk.Button(row, text=t("btn_delete"),
                      command=lambda n=name: self._on_delete_profile(n),
                      bg="#f0f0f0", fg="#c44536", relief="flat",
                      font=("微软雅黑", 9), cursor="hand2",
                      width=10).pack(side="right", padx=8)

            tk.Button(row, text=t("btn_apply_profile"),
                      command=lambda n=name: self._on_apply_profile(n),
                      bg="#1f6aa5", fg="white", activebackground="#1f6aa5",
                      activeforeground="white", relief="flat",
                      font=("微软雅黑", 11, "bold"), cursor="hand2",
                      width=12, height=2, bd=0).pack(side="right", padx=4)

    def _on_save_profile(self):
        name = simpledialog.askstring(t("msg_save_profile_title"),
                                      t("msg_save_profile_ask"),
                                      parent=self.root)
        if not name or not name.strip():
            return
        name = name.strip()

        ip_mode = self.ip_mode_var.get()
        dns_mode = self.dns_mode_var.get()
        profile = {"ip_mode": ip_mode, "dns_mode": dns_mode}

        ip = self.ip_var.get().strip()
        mask = self.mask_var.get().strip()
        gw = self.gateway_var.get().strip()
        d1 = self.dns1_var.get().strip()
        d2 = self.dns2_var.get().strip()

        if ip_mode == "static":
            if not is_valid_ipv4(ip):
                messagebox.showerror(t("msg_format_err"), t("msg_ip_invalid")); return
            if not mask:
                messagebox.showerror(t("msg_format_err"), t("msg_mask_empty")); return
            if gw and not is_valid_ipv4(gw):
                messagebox.showerror(t("msg_format_err"), t("msg_gw_invalid")); return
        if dns_mode == "static":
            if not d1 and not d2:
                messagebox.showerror(t("msg_format_err"), t("msg_dns_empty")); return
            if d1 and not is_valid_ipv4(d1):
                messagebox.showerror(t("msg_format_err"), t("msg_dns1_invalid")); return
            if d2 and not is_valid_ipv4(d2):
                messagebox.showerror(t("msg_format_err"), t("msg_dns2_invalid")); return

        profile.update({"ip": ip, "mask": mask, "gateway": gw,
                        "dns1": d1, "dns2": d2})
        self.profiles[name] = profile
        if save_profiles(self.profiles):
            self._render_profile_list()
            messagebox.showinfo(t("msg_ok_title"), t("msg_saved", name=name))
        else:
            messagebox.showerror(t("msg_format_err"), t("msg_save_fail"))

    def _on_delete_profile(self, name):
        if not messagebox.askyesno(t("msg_del_title"), t("msg_del_ask", name=name)):
            return
        self.profiles.pop(name, None)
        save_profiles(self.profiles)
        self._render_profile_list()

    def _on_apply_current(self):
        if not self.require_admin():
            return
        alias = self.config_adapter_var.get().strip()
        if not alias:
            messagebox.showwarning(t("msg_warn_title"), t("msg_pick_adapter")); return

        ip_mode = self.ip_mode_var.get()
        dns_mode = self.dns_mode_var.get()
        ip = self.ip_var.get().strip()
        mask = self.mask_var.get().strip()
        gw = self.gateway_var.get().strip()
        d1 = self.dns1_var.get().strip()
        d2 = self.dns2_var.get().strip()

        if ip_mode == "static":
            if not is_valid_ipv4(ip):
                messagebox.showerror(t("msg_format_err"), t("msg_ip_invalid")); return
            if not mask:
                messagebox.showerror(t("msg_format_err"), t("msg_mask_empty")); return
            if gw and not is_valid_ipv4(gw):
                messagebox.showerror(t("msg_format_err"), t("msg_gw_invalid")); return
        if dns_mode == "static":
            if not d1 and not d2:
                messagebox.showerror(t("msg_format_err"), t("msg_dns_empty")); return
            if d1 and not is_valid_ipv4(d1):
                messagebox.showerror(t("msg_format_err"), t("msg_dns1_invalid")); return
            if d2 and not is_valid_ipv4(d2):
                messagebox.showerror(t("msg_format_err"), t("msg_dns2_invalid")); return

        ip_str = t("auto") if ip_mode == "dhcp" else ip
        dns_str = t("auto") if dns_mode == "dhcp" else ", ".join([x for x in [d1, d2] if x])
        mask_str = mask if ip_mode == "static" else t("auto_paren")
        gw_str = gw if (ip_mode == "static" and gw) else t("auto_paren")
        msg = t("msg_confirm_apply", alias=alias, ip=ip_str,
                mask=mask_str, gw=gw_str, dns=dns_str)
        if not messagebox.askyesno(t("msg_confirm_title"), msg):
            return

        self.run_async(
            lambda: self._apply_config(alias, ip_mode, dns_mode, ip, mask, gw, d1, d2),
            t("apply_busy", alias=alias)
        )

    def _on_apply_profile(self, name):
        if not self.require_admin():
            return
        prof = self.profiles.get(name)
        if not prof:
            return
        alias = self.config_adapter_var.get().strip()
        if not alias:
            messagebox.showwarning(t("msg_warn_title"), t("msg_pick_adapter")); return

        ip_mode = prof.get("ip_mode", "dhcp")
        dns_mode = prof.get("dns_mode", "dhcp")
        ip = prof.get("ip", "")
        mask = prof.get("mask", "")
        gw = prof.get("gateway", "")
        d1 = prof.get("dns1", "")
        d2 = prof.get("dns2", "")

        ip_str = t("auto") if ip_mode == "dhcp" else ip
        dns_str = t("auto") if dns_mode == "dhcp" else ", ".join([x for x in [d1, d2] if x])
        gw_str = gw if (ip_mode == "static" and gw) else t("auto_paren")
        msg = t("msg_confirm_switch", alias=alias, name=name,
                ip=ip_str, gw=gw_str, dns=dns_str)
        if not messagebox.askyesno(t("msg_confirm_title"), msg):
            return

        self.ip_mode_var.set(ip_mode)
        self.dns_mode_var.set(dns_mode)
        self.ip_var.set(ip)
        self.mask_var.set(mask)
        self.gateway_var.set(gw)
        self.dns1_var.set(d1)
        self.dns2_var.set(d2)
        self._toggle_mode()

        self.run_async(
            lambda: self._apply_config(alias, ip_mode, dns_mode, ip, mask, gw, d1, d2),
            t("apply_busy_switch", name=name)
        )

    def _apply_config(self, alias, ip_mode, dns_mode, ip, mask, gw, d1, d2):
        self.root.after(0, lambda: self.nb.select(2))

        if ip_mode == "dhcp" and dns_mode == "dhcp":
            desc = t("apply_title_ip_dhcp_dns_dhcp")
        elif ip_mode == "dhcp" and dns_mode == "static":
            desc = t("apply_title_ip_dhcp_dns_static")
        elif ip_mode == "static" and dns_mode == "dhcp":
            desc = t("apply_title_ip_static_dns_dhcp")
        else:
            desc = t("apply_title_ip_static_dns_static")

        self.root.after(0, self.write, "=" * 60 + "\n", "head")
        self.root.after(0, self.write, t("apply_setting", alias=alias, desc=desc) + "\n", "head")
        self.root.after(0, self.write, "=" * 60 + "\n", "head")

        q_alias = ps_quote(alias)
        q_ip = ps_quote(ip)
        q_gw = ps_quote(gw) if gw else "$null"
        prefix = mask_to_prefix(mask) if ip_mode == "static" else 24

        dns_list = []
        if d1:
            dns_list.append(ps_quote(d1))
        if d2:
            dns_list.append(ps_quote(d2))
        dns_array = "@(" + ",".join(dns_list) + ")" if dns_list else "@()"

        parts = [f"$ErrorActionPreference = 'SilentlyContinue'\n$alias = {q_alias}\n"]

        if ip_mode == "dhcp":
            parts.append("""
Write-Output "[IP 1/3] Clear old IP and default route ..."
Remove-NetRoute -InterfaceAlias $alias -DestinationPrefix '0.0.0.0/0' -Confirm:$false -ErrorAction SilentlyContinue
Remove-NetIPAddress -InterfaceAlias $alias -AddressFamily IPv4 -Confirm:$false -ErrorAction SilentlyContinue
Start-Sleep -Milliseconds 400
Write-Output "[IP 2/3] Enable DHCP ..."
Set-NetIPInterface -InterfaceAlias $alias -Dhcp Enabled -ErrorAction SilentlyContinue
Write-Output "[IP 3/3] Renew IP ..."
ipconfig /renew $alias | Out-Null
Start-Sleep -Seconds 2
""")
        else:
            parts.append(f"""
Write-Output "[IP 1/3] Disable DHCP ..."
Set-NetIPInterface -InterfaceAlias $alias -Dhcp Disabled -ErrorAction SilentlyContinue
Write-Output "[IP 2/3] Clear old IP and default route ..."
Remove-NetRoute -InterfaceAlias $alias -DestinationPrefix '0.0.0.0/0' -Confirm:$false -ErrorAction SilentlyContinue
Remove-NetIPAddress -InterfaceAlias $alias -AddressFamily IPv4 -Confirm:$false -ErrorAction SilentlyContinue
Start-Sleep -Milliseconds 400
Write-Output "[IP 3/3] Apply static IP / gateway ..."
$args1 = @{{
    InterfaceAlias = $alias
    IPAddress      = {q_ip}
    PrefixLength   = {prefix}
    AddressFamily  = 'IPv4'
}}
if ({q_gw}) {{ $args1['DefaultGateway'] = {q_gw} }}
New-NetIPAddress @args1 | Out-Null
""")

        if dns_mode == "dhcp":
            parts.append("""
Write-Output "[DNS] Reset to automatic DNS ..."
Set-DnsClientServerAddress -InterfaceAlias $alias -ResetServerAddresses -ErrorAction SilentlyContinue
""")
        else:
            parts.append(f"""
Write-Output "[DNS] Apply DNS servers ..."
$dnsList = {dns_array}
if ($dnsList.Count -gt 0) {{
    Set-DnsClientServerAddress -InterfaceAlias $alias -ServerAddresses $dnsList -ErrorAction SilentlyContinue
}}
""")

        parts.append('\nWrite-Output "OK"\n')
        ps = "".join(parts)

        self.root.after(0, self.progress.configure, value=20)
        ok, out = run_ps(ps, timeout=150)
        self.root.after(0, self.progress.configure, value=85)
        if out:
            self.root.after(0, self.write, out + "\n")
        if ok and "OK" in out:
            self.root.after(0, self.write, "\n" + t("apply_ok") + "\n", "success")
        else:
            self.root.after(0, self.write, "\n" + t("apply_fail") + "\n", "error")

        self.root.after(0, self.progress.configure, value=100)
        self.root.after(0, self.write, "=" * 60 + "\n\n", "head")
        self.root.after(0, self._refresh_adapter_combo)

    # ---------- 通用 ----------
    def write(self, text, tag=None):
        self.log.insert("end", text, tag or "")
        self.log.see("end")

    def clear_log(self):
        self.log.delete("1.0", "end")

    def run_async(self, target, busy_text):
        if self._busy:
            messagebox.showinfo(t("busy_title"), t("busy_msg"))
            return
        self._busy = True
        self.status_var.set(busy_text)
        self.progress["value"] = 0

        def wrapper():
            try:
                target()
            except Exception as e:
                self.root.after(0, self.write, f"\n❌ Error: {e}\n", "error")
            finally:
                self._busy = False
                self.root.after(0, lambda: self.status_var.set(t("status_ready")))
                self.root.after(0, lambda: self.progress.configure(value=0))

        threading.Thread(target=wrapper, daemon=True).start()

    def require_admin(self):
        if not is_admin():
            messagebox.showwarning(t("msg_need_admin_title"), t("msg_need_admin_text"))
            return False
        return True

    # ---------- 拿网卡信息 ----------
    def _get_adapters(self):
        ps = r"""
$ErrorActionPreference = 'SilentlyContinue'
$ipMap = @{}
foreach ($ipa in (Get-NetIPAddress -AddressFamily IPv4)) {
    if ($ipa.IPAddress -eq '127.0.0.1') { continue }
    $k = "$($ipa.InterfaceIndex)"
    if ($ipMap.ContainsKey($k)) {
        if ($ipMap[$k] -notlike "*$($ipa.IPAddress)*") {
            $ipMap[$k] = $ipMap[$k] + ', ' + $ipa.IPAddress
        }
    } else { $ipMap[$k] = $ipa.IPAddress }
}
$gwMap = @{}
foreach ($r in (Get-NetRoute -AddressFamily IPv4)) {
    if ($r.DestinationPrefix -ne '0.0.0.0/0') { continue }
    $k = "$($r.InterfaceIndex)"
    if (-not $gwMap.ContainsKey($k)) { $gwMap[$k] = $r.NextHop }
}
$dnsMap = @{}
foreach ($d in (Get-DnsClientServerAddress -AddressFamily IPv4)) {
    if (-not $d.ServerAddresses -or $d.ServerAddresses.Count -eq 0) { continue }
    $k = "$($d.InterfaceIndex)"
    $dnsMap[$k] = ($d.ServerAddresses -join ', ')
}
$result = foreach ($ad in (Get-NetAdapter)) {
    $k = "$($ad.ifIndex)"
    [PSCustomObject]@{
        Name                 = $ad.Name
        Status               = $ad.Status
        LinkSpeed            = $ad.LinkSpeed
        InterfaceDescription = $ad.InterfaceDescription
        DriverVersion        = $ad.DriverVersion
        DriverDate           = $ad.DriverDate
        DriverProvider       = $ad.DriverProvider
        Virtual              = $ad.Virtual
        MacAddress           = $ad.MacAddress
        IPv4                 = if ($ipMap.ContainsKey($k))  { $ipMap[$k] }  else { '' }
        Gateway              = if ($gwMap.ContainsKey($k))  { $gwMap[$k] }  else { '' }
        DNS                  = if ($dnsMap.ContainsKey($k)) { $dnsMap[$k] } else { '' }
    }
}
ConvertTo-Json -InputObject @($result) -Depth 3 -Compress
"""
        ok, out = run_ps(ps, timeout=60)
        if not ok or not out:
            return []
        idx = -1
        for i, ch in enumerate(out):
            if ch in "[{":
                idx = i
                break
        if idx < 0:
            return []
        out = out[idx:]
        try:
            data = json.loads(out)
        except Exception:
            for end in range(len(out), 0, -1):
                try:
                    data = json.loads(out[:end])
                    break
                except Exception:
                    continue
            else:
                return []
        if isinstance(data, dict):
            data = [data]
        return data if isinstance(data, list) else []

    @staticmethod
    def _fmt_date(s):
        if not s:
            return ""
        m = re.search(r"/Date\((\d+)\)/", str(s))
        if m:
            try:
                ts = int(m.group(1)) / 1000
                return datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
            except Exception:
                return ""
        m = re.match(r"(\d{4}-\d{2}-\d{2})", str(s))
        if m:
            return m.group(1)
        return ""

    def _status_cn(self, status):
        return {
            "Up": t("st_up"), "Disconnected": t("st_disc"),
            "Disabled": t("st_dis"), "Not Present": t("st_np"),
            "LowerLayerDown": t("st_lower"),
        }.get(status, t("st_unknown"))

    def _status_color(self, status):
        return {
            "Up": "#4caf50", "Disconnected": "#9e9e9e",
            "Disabled": "#ffb300", "Not Present": "#e53935",
            "LowerLayerDown": "#ffb300",
        }.get(status, "#9e9e9e")

    def _status_tip(self, status):
        return {
            "Up": t("tip_up"), "Disconnected": t("tip_disc"),
            "Disabled": t("tip_dis"), "Not Present": t("tip_np"),
            "LowerLayerDown": t("tip_lower"),
        }.get(status, "")

    def _render_adapter_cards(self, adapters):
        self._adapter_cache = adapters
        for w in self.adapter_box.inner.winfo_children():
            w.destroy()

        if not adapters:
            tk.Label(self.adapter_box.inner, text=t("no_adapters"),
                     bg="#1e1e2e", fg="#ff6e6e",
                     font=("微软雅黑", 11)).pack(pady=30)
            return

        total = len(adapters)
        up_count = sum(1 for a in adapters if a.get("Status") == "Up")
        tk.Label(self.adapter_box.inner,
                 text=t("adapters_count", total=total, up=up_count),
                 bg="#1e1e2e", fg="#c792ea",
                 font=("微软雅黑", 11, "bold")).pack(anchor="w", padx=14, pady=(12, 6))

        for ad in adapters:
            self._render_one_card(ad)

    def _render_one_card(self, ad):
        name = ad.get("Name") or t("unknown_adapter")
        desc = ad.get("InterfaceDescription") or ""
        status = ad.get("Status") or "Unknown"
        speed = ad.get("LinkSpeed") or ""
        drv_ver = ad.get("DriverVersion") or ""
        drv_date = ad.get("DriverDate") or ""
        provider = ad.get("DriverProvider") or ""
        is_virtual = ad.get("Virtual") is True
        ipv4 = ad.get("IPv4") or ""
        gateway = ad.get("Gateway") or ""
        dns = ad.get("DNS") or ""
        mac = ad.get("MacAddress") or ""

        cn_status = self._status_cn(status)
        color = self._status_color(status)
        tip = self._status_tip(status)

        card = tk.Frame(self.adapter_box.inner, bg="#2a2a3e",
                        highlightthickness=2, highlightbackground=color, bd=0)
        card.pack(fill="x", padx=14, pady=6)

        header = tk.Frame(card, bg="#2a2a3e")
        header.pack(fill="x", padx=14, pady=(10, 2))
        tk.Label(header, text="●", fg=color, bg="#2a2a3e",
                 font=("Arial", 22)).pack(side="left")
        tk.Label(header, text=name, fg="white", bg="#2a2a3e",
                 font=("微软雅黑", 13, "bold")).pack(side="left", padx=(4, 8))
        if is_virtual:
            tk.Label(header, text=t("virtual_mark"), fg="#888", bg="#2a2a3e",
                     font=("微软雅黑", 9)).pack(side="left")
        tk.Label(header, text=cn_status, fg=color, bg="#2a2a3e",
                 font=("微软雅黑", 12, "bold")).pack(side="right")
        if tip:
            tk.Label(header, text=tip, fg="#999", bg="#2a2a3e",
                     font=("微软雅黑", 9)).pack(side="right", padx=(0, 8))

        if desc:
            tk.Label(card, text=desc, fg="#b0b0c0", bg="#2a2a3e",
                     font=("微软雅黑", 9), anchor="w",
                     wraplength=880, justify="left"
                     ).pack(anchor="w", padx=18, pady=(0, 4))

        info = tk.Frame(card, bg="#252535")
        info.pack(fill="x", padx=14, pady=(4, 10))

        rows = [
            (t("lbl_ipv4"), ipv4 or "—"),
            (t("lbl_gw"), gateway or "—"),
            (t("lbl_dns"), dns or "—"),
        ]
        if speed:
            rows.append((t("lbl_speed"), speed))
        if mac:
            rows.append((t("lbl_mac"), mac))
        if drv_ver:
            d = self._fmt_date(drv_date)
            rows.append((t("lbl_drv_ver"), drv_ver + (f"  ({d})" if d else "")))
        if provider:
            rows.append((t("lbl_drv_vendor"), provider))

        for label, value in rows:
            row = tk.Frame(info, bg="#252535")
            row.pack(fill="x", padx=10, pady=1)
            tk.Label(row, text=label, fg="#8a8a9a", bg="#252535",
                     font=("微软雅黑", 9), width=12, anchor="w"
                     ).pack(side="left")
            fg = "#e0e0e0"
            if label in (t("lbl_ipv4"), t("lbl_dns"), t("lbl_gw")) and value != "—":
                fg = "#7bd88f"
            tk.Label(row, text=value, fg=fg, bg="#252535",
                     font=("Consolas", 10), anchor="w",
                     wraplength=700, justify="left"
                     ).pack(side="left", fill="x", expand=True)

    # ============ 诊断 ============
    def on_diagnose(self):
        self.run_async(self._do_diagnose, t("diag_reading"))

    def _do_diagnose(self):
        host = self._get_current_host()
        self.root.after(0, self.write, "=" * 60 + "\n", "head")
        self.root.after(0, self.write, t("diag_start") + "\n", "head")
        self.root.after(0, self.write, "=" * 60 + "\n", "head")
        self.root.after(0, lambda: self.nb.select(0))

        self.root.after(0, self.status_var.set, t("diag_reading"))
        self.root.after(0, self.progress.configure, value=20)
        adapters = self._get_adapters()
        self.root.after(0, self._render_adapter_cards, adapters)
        self.root.after(0, self.progress.configure, value=60)

        self.root.after(0, self.write, "\n" + t("diag_adapters", n=len(adapters)) + "\n", "info")
        for a in adapters:
            cn = self._status_cn(a.get("Status", ""))
            self.root.after(0, self.write,
                            f"  · {a.get('Name')}  [{cn}]  "
                            f"IP: {a.get('IPv4') or '—'}  DNS: {a.get('DNS') or '—'}\n")

        self.root.after(0, self.status_var.set, t("diag_testing", host=host))
        self.root.after(0, self.progress.configure, value=75)

        ps = f"""
$r = Test-NetConnection -ComputerName '{host}' -Port {TEST_PORT} -WarningAction SilentlyContinue
Write-Output "PING=$($r.PingSucceeded)"
Write-Output "TCP=$($r.TcpTestSucceeded)"
"""
        _, out = run_ps(ps, timeout=60)
        ping_ok = "PING=True" in out
        tcp_ok = "TCP=True" in out

        self.root.after(0, self.write,
                        "\n" + t("diag_conn", host=host, port=TEST_PORT) + "\n", "info")
        self.root.after(0, self.write,
                        t("diag_icmp_ok" if ping_ok else "diag_icmp_fail") + "\n")
        self.root.after(0, self.write,
                        t("diag_tcp_ok" if tcp_ok else "diag_tcp_fail") + "\n")

        self.root.after(0, self.write, "\n" + t("diag_conclusion") + "\n", "info")
        if tcp_ok:
            self.root.after(0, self.write, t("diag_ok", host=host) + "\n", "success")
        elif ping_ok and not tcp_ok:
            self.root.after(0, self.write, t("diag_warn") + "\n", "warn")
        else:
            self.root.after(0, self.write, t("diag_bad") + "\n", "error")

        self.root.after(0, self.progress.configure, value=100)
        self.root.after(0, self.write, "=" * 60 + "\n\n", "head")

    # ============ 修复 ============
    def on_repair(self):
        if not self.require_admin():
            return
        self.run_async(self._do_repair, t("repair_start"))

    def _do_repair(self):
        self.root.after(0, lambda: self.nb.select(2))
        steps = [
            (t("repair_step_1"), "ipconfig /release"),
            (t("repair_step_2"), "ipconfig /renew"),
            (t("repair_step_3"), "ipconfig /flushdns"),
            (t("repair_step_4"), "ipconfig /registerdns"),
        ]
        self.root.after(0, self.write, "=" * 60 + "\n", "head")
        self.root.after(0, self.write, t("repair_start") + "\n", "head")
        self.root.after(0, self.write, "=" * 60 + "\n", "head")

        total = len(steps)
        ok_count = 0
        for i, (name, cmd) in enumerate(steps, 1):
            self.root.after(0, self.write, f"\n[{i}/{total}] {name} …\n", "info")
            self.root.after(0, lambda v=i / total: self.progress.configure(value=v * 100))
            self.root.after(0, lambda n=name: self.status_var.set(t("step_running", name=n)))
            ok, out = run_cmd(cmd, timeout=150, encoding="gbk")
            if ok:
                ok_count += 1
                self.root.after(0, self.write, t("step_ok") + "\n", "success")
            else:
                self.root.after(0, self.write, t("step_fail") + "\n", "error")
            if out:
                self.root.after(0, self.write, out[:800] + "\n")

        self.root.after(0, self.write, "\n" + t("repair_done", ok=ok_count, total=total) + "\n", "success")
        self.root.after(0, self.write, "=" * 60 + "\n\n", "head")

    # ============ 重置 ============
    def on_reset(self):
        if not self.require_admin():
            return
        if not messagebox.askyesno(t("msg_reset_title"), t("msg_reset_ask")):
            return
        self.run_async(self._do_reset, t("reset_start"))

    def _do_reset(self):
        self.root.after(0, lambda: self.nb.select(2))
        steps = [
            (t("reset_step_1"), "netsh winsock reset"),
            (t("reset_step_2"), "netsh int ip reset"),
            (t("reset_step_3"), "netsh interface ipv4 reset"),
            (t("reset_step_4"), "netsh interface ipv6 reset"),
        ]
        self.root.after(0, self.write, "=" * 60 + "\n", "head")
        self.root.after(0, self.write, t("reset_start") + "\n", "head")
        self.root.after(0, self.write, "=" * 60 + "\n", "head")

        total = len(steps)
        ok_count = 0
        for i, (name, cmd) in enumerate(steps, 1):
            self.root.after(0, self.write, f"\n[{i}/{total}] {name} …\n", "info")
            self.root.after(0, lambda v=i / total: self.progress.configure(value=v * 100))
            self.root.after(0, lambda n=name: self.status_var.set(t("step_running", name=n)))
            ok, out = run_cmd(cmd, timeout=150, encoding="gbk")
            if ok:
                ok_count += 1
                self.root.after(0, self.write, t("step_ok") + "\n", "success")
            else:
                self.root.after(0, self.write, t("step_fail") + "\n", "error")
            if out:
                self.root.after(0, self.write, out[:800] + "\n")

        self.root.after(0, self.write, "\n" + t("reset_done", ok=ok_count, total=total) + "\n", "success")
        self.root.after(0, self.write, t("reset_restart") + "\n", "warn")
        self.root.after(0, self.write, "=" * 60 + "\n\n", "head")

    # ============ 驱动检查 ============
    def on_driver(self):
        self.run_async(self._do_driver, t("drv_start"))

    def _do_driver(self):
        self.root.after(0, lambda: self.nb.select(0))
        adapters = self._get_adapters()
        self.root.after(0, self._render_adapter_cards, adapters)

        self.root.after(0, self.write, "=" * 60 + "\n", "head")
        self.root.after(0, self.write, t("drv_start") + "\n", "head")
        self.root.after(0, self.write, "=" * 60 + "\n", "head")

        issues = []
        for ad in adapters:
            name = ad.get("Name", "?")
            status = ad.get("Status", "")
            drv_date = ad.get("DriverDate", "")
            if status == "Not Present":
                issues.append(t("drv_issue_np", name=name))
            elif status == "Disabled":
                issues.append(t("drv_issue_dis", name=name))
            elif status in ("LowerLayerDown", "Disconnected") and not ad.get("Virtual"):
                issues.append(t("drv_issue_disc", name=name))

            d = self._fmt_date(drv_date)
            if d:
                try:
                    dt = datetime.datetime.strptime(d, "%Y-%m-%d")
                    years = (datetime.datetime.now() - dt).days / 365
                    if years > 3:
                        issues.append(t("drv_issue_old", name=name, date=d, years=years))
                except Exception:
                    pass

        self.root.after(0, self.write, "\n" + t("drv_count", n=len(adapters)) + "\n", "info")
        if issues:
            self.root.after(0, self.write, "\n" + t("drv_issues") + "\n", "warn")
            for x in issues:
                tag = "error" if x.startswith("❌") else "warn"
                self.root.after(0, self.write, "  " + x + "\n", tag)
        else:
            self.root.after(0, self.write, "\n" + t("drv_ok") + "\n", "success")

        self.root.after(0, self.write, "=" * 60 + "\n\n", "head")


# ============ 启动 ============
def main():
    load_settings()

    if not is_admin():
        tmp = tk.Tk()
        tmp.withdraw()
        ans = messagebox.askyesno(t("elevate_title"), t("elevate_ask"))
        tmp.destroy()
        if ans:
            if run_as_admin():
                sys.exit(0)
            else:
                messagebox.showerror(t("elevate_fail_title"), t("elevate_fail_text"))

    root = tk.Tk()
    NetRepairApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()