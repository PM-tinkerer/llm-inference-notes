# 推理手册 · LLM Inference Field Notes

中文响应式静态课程网站。目录沿用《大模型推理体系》的 8 篇 24 章规划，只有前三章有正文，第 4–24 章仅为待学习页面。

## 在线阅读

[打开公网课程网站](https://pm-tinkerer.github.io/llm-inference-notes/)

已发布到 GitHub Pages，来源为 main 分支根目录；后续提交会自动更新网站。

## 直接阅读

双击 `index.html`，或在项目目录运行：

```sh
python3 -m http.server 8000
```

浏览器打开 `http://localhost:8000`。无需 npm、数据库、账号、API Key 或外部 CDN；正文在 HTML 内，关闭 JavaScript 仍可阅读和翻页。JS 提供目录过滤、手机目录、KV 计算器、调度演示、块地址查询。图表和字体均无需联网（使用系统中文字体）。

## 发布到 GitHub Pages（推荐：从分支发布）

1. 在 GitHub 创建仓库，例如 `llm-inference-notes`。如要公开分享，选择 Public。
2. 上传**本项目文件夹内的全部内容到仓库根目录**，确保 `index.html` 和 `assets/` 在根目录，不能多套一层 `inference-course/`。
3. 进入仓库 **Settings → Pages → Build and deployment**。
4. Source 选 **Deploy from a branch**，分支选 `main`，目录选 `/(root)`，保存。
5. 等待 GitHub 的 Pages 部署完成，在 Pages 设置页点击站点地址。项目站通常为 `https://你的用户名.github.io/仓库名/`。

所有资源和页面链接均使用相对路径，支持 GitHub Pages 仓库子路径。已包含 `.nojekyll`。具体菜单以 GitHub 当前界面为准，参考 [官方发布来源说明](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)。本项目已发布至上述公网地址。

### 可选：GitHub Actions 自动部署

在 Pages 的 Source 选择 **GitHub Actions**。将 `docs/pages-workflow.yml.example` 复制为 `.github/workflows/pages.yml`，提交到 `main`。工作流校验文件后，只把网页及资源复制到 `dist/` 并上传，不包含编辑源和说明文件。

不要同时启用两套发布方式。若使用不同分支名，修改工作流中的 `branches`。此配置需要仓库允许 GitHub Actions 与 Pages，并允许 Pages 环境从该分支部署。

## 项目结构

```text
index.html                 课程主页（已生成，可直接发布）
chapter-01.html … 24.html   三章正文 + 二十一章待学习页
assets/                    CSS、JS、四张技术 SVG、校订 A4 图、原会话 PNG
content/curriculum.json    原对话 24 章标题
content/chapter-01.html     第一章正文片段
content/chapter-02.html     第二章正文片段
content/chapter-03.html     第三章正文片段
scripts/build.py           标准库静态页面生成器
scripts/diagrams.py        SVG 图生成与 A4 校订工具
scripts/check.py           链接、页面、章节状态与数值检查
docs/                      技术校订说明、部署工作流示例
```

## 未来逐章扩展

**仅在你确认学完某章之后补充该章正文。**

1. 新增 `content/chapter-04.html`（以第四章为例）。用 `<section id="唯一英文锚点"><h2>4.1 标题</h2>…</section>` 组织各节，页面内导航会自动生成。
2. 加入该章的图、术语表、公式适用条件、复习问答与资料链接。
3. 导航收录状态和主页进度会根据正文文件自动更新。按需更新 `scripts/build.py` 中的导语、主页编辑说明与首页卡片；如调整课程范围，更新 `content/curriculum.json`。当前检查脚本严格验证“仅前三章有正文”，正式扩展后同步更新检查中的已收录章节范围。
4. 运行：

```sh
python3 scripts/build.py
python3 scripts/check.py
node --check assets/app.js
```

5. 预览桌面和手机，检查新章节与前后翻页，再提交所有更新文件。无需重新搭建项目。

不要只修改生成后的章节页面，否则重新生成会覆盖修改。现有 4–24 章不含课程正文。源文件使用 UTF-8；Python 3.9+ 即可，Node 只用于可选 JS 语法检查。

## 技术口径与配图

正文是对原会话的重编与校订，不是逐字导出。使用常见 Decoder-only、全注意力、自回归流程；滑动窗口、MLA、混合架构与推测解码不直接套用本文全部公式。

- 复用原会话 `original-prefill-decode.png`，保留原样并在正文标注其简化与误读风险。
- 复用工作区已有 `inference-a4.svg`，校订首 Token、缓存位置数、耗时公式和 RoPE 表述。
- 新增 `pipeline.svg`、`batching.svg`、`blocks.svg`、`prefix.svg`，均为可编辑矢量图。
- 交互工具是教学示例，不能代替模型与硬件压测。

详见 [技术校订](docs/technical-notes.md)。本项目未替用户授予新的开源许可证；若公开作为可再分发项目，可按实际权利情况自行添加 LICENSE。原配图的来源记录保留在上述说明中。
