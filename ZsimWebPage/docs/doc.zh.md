# ZSim开始手册

## 下载并启动

从[发布页面](https://github.com/ZZZSimulator/ZSim/releases/latest)下载最新打包源码或使用 `git clone` 指令直接下载最新源码

### 安装UV（如未安装）

在任意终端中执行：

```bash
# 如果你已安装了python或安装了pip，则可以使用pip安装：
pip install uv
```

如果你没有python：

```bash
# macOS/Linux：
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```bash
# Windows11 24H2及以上：
winget install --id=astral-sh.uv -e
```

```bash
# 旧版Windows：
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

或参考官方安装指南：[https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/)

### 安装ZZZ模拟器

在项目目录中执行：

```bash
uv sync
uv pip install .  # 这里有个 '.' 代表相对路径
```

## 运行说明

在任意终端中执行（部分操作系统需要重启终端）：

```bash
zsim run
```

若你不想安装此工具，或者上一步没成功，可直接运行：

```bash
uv run ./zsim/run.py run
```

```bash
# 或使用：
uv run zsim run
```

---

## 如何开始模拟

1. 在**角色编辑**页面下拉菜单中选择角色（角色的初始站位顺序和游戏逻辑相同）
2. 依次展开每位角色的配置列表，修改角色的配装
3. 完成修改后，点击页面最下方的 **提交并保存角色配置** 按钮保存配置
4. 在左侧标签栏中点击 **模拟器** 按钮，切换到模拟器页面
5. 填写模拟时长（单位：帧），并通过 **APL选择按钮** 选择当前队伍的APL，然后点击 **保存APL选择** 按钮保存
6. 点击 **开始模拟** 按钮启动模拟
7. 在 **"数据分析"** 页面中，点击 **开启数据分析** 按钮，自动分析模拟数据，分析完成后可展开查看结果

---

## FAQ

1. 本项目目前还处于测试与开发阶段，如果您碰到了程序报错，请向开发者团队提供**复现方式**以及**报错日志**；
2. 本项目前端界面仅为临时使用，未来我们会对用户界面进行重新开发；
