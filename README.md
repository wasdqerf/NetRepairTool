# NetRepairTool
<img width="1002" height="842" alt="NetRepairTool_VqSRTAHuOq" src="https://github.com/user-attachments/assets/fe973b3a-c376-4b8b-af24-80ab9e60b8c4" />
<img width="1002" height="842" alt="NetRepairTool_eqZLPg91mC" src="https://github.com/user-attachments/assets/0913cb5e-8bdd-42f9-b389-85b4dd421644" />
**Windows 11 网络故障诊断与修复工具 | Windows 11 Network Diagnosis and Repair Tool**

一款免费、开源、免安装的 Windows 网络工具，帮助普通用户快速排查和修复常见网络问题。

A free, open-source, portable Windows network utility that helps users diagnose and fix common network problems quickly.

---

## ✨ 功能特性 / Features

- 🔍 **网络诊断**：一键检测所有网卡状态、IP 地址、网关、DNS，测试外网连通性
- 🔧 **网络修复**：自动释放 IP、更新 IP、刷新 DNS 缓存，无需重启即可恢复
- 🔄 **网络重置**：重置 Winsock、TCP/IP 协议栈，修复顽固性网络故障
- 📋 **网卡驱动检查**：查看驱动版本、日期，提示过旧或异常的驱动
- ⚙️ **IP / DNS 一键切换**：保存多套配置，公司、家里一键切换
- 🌐 **中英双语**：支持中文和英文界面自动切换
- 🎯 **可配置测试目标**：京东 / 微软 / 谷歌 / 百度 / 自定义

- 🔍 **Diagnose**: Check adapters, IP, gateway, DNS, and external connectivity
- 🔧 **Repair**: Release/renew IP, flush DNS — no reboot required
- 🔄 **Reset**: Reset Winsock and TCP/IP stack for stubborn issues
- 📋 **Driver Check**: View driver version/date, flag outdated drivers
- ⚙️ **One-Click IP / DNS Switch**: Save profiles for office/home
- 🌐 **Bilingual UI**: Chinese and English
- 🎯 **Configurable Test Target**: JD, Microsoft, Google, Baidu, or custom

---

## 📥 下载 / Download

前往 [Releases](https://github.com/wasdqerf/NetRepairTool/releases) 页面下载最新的 `NetRepairTool.exe`，双击即可运行（无需安装）。

Go to the [Releases](https://github.com/wasdqerf/NetRepairTool/releases) page and download the latest `NetRepairTool.exe`. Double-click to run — no installation required.

---

## 🚀 使用方法 / Usage

1. 右键 `NetRepairTool.exe` → **以管理员身份运行**（修复、重置、改 IP 都需要管理员权限）
2. 点击 **诊断网络** 查看当前网络状态
3. 根据诊断结果，选择 **修复网络** 或 **重置网络**
4. 切换网络环境时，用 **网络配置** 标签页保存 / 应用配置

1. Right-click `NetRepairTool.exe` → **Run as Administrator**
2. Click **Diagnose** to view current network status
3. Use **Repair** or **Reset** based on the diagnosis
4. Use the **Config** tab to save / apply network profiles

---

## ⚠️ 注意事项 / Notes

- 本工具需要 **管理员权限**，因为它要调用系统命令修改网络配置
- 网络重置操作会修改 Winsock 和 TCP/IP 协议栈，完成后**需要重启电脑**
- 所有操作均在本地执行，**不联网、不上传任何用户数据**

- Requires **Administrator privileges** to run system network commands
- Network reset modifies Winsock and TCP/IP stack — **reboot required**
- All operations are local. **No data is collected or uploaded.**

---

## 🛠️ 从源码运行 / Run from Source

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole --uac-admin --icon="NetRepairTool.ico" --name "NetRepairTool" NetRepairTool.py
