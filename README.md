SO101 模型适配子系统 — 占位可运行示例

目的
- 在仓库中提供一个最小可运行的 Python 子系统示例，便于在虚拟机中创建 Python 环境并验证运行流程。
- 该示例使用占位模型实现（反转输入字符串并返回 JSON 格式），你可以用真实 SO101 模型替换占位逻辑。

包含的文件
- run_so101.py — 主程序入口（可从文件或 stdin 读取输入，输出 JSON 行）。
- requirements.txt — 建议依赖（默认 CPU 版本）。
- setup_venv.sh — 在 Linux 虚拟机上创建并激活虚拟环境的脚本。
- run.sh — 示例运行脚本。
- models/README_weights.md — 权重存放与 LFS / Release 建议说明。
- tests/test_basic.py — 一个基本的 smoke test（使用 pytest）。
- .gitignore — 忽略虚拟环境、缓存等。

快速开始（在 Debian/Ubuntu 或类 Unix 系统）
1. 克隆仓库并切到 so101-setup 分支（你现在可以在仓库查看该分支）：

   git clone https://github.com/Kyl123456789/kyl111.git
   cd kyl111
   git checkout so101-setup

2. 使用脚本创建虚拟环境并安装依赖：

   bash setup_venv.sh

   脚本默认创建 .venv 并安装 requirements.txt。如果你希望手动执行：

   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install -U pip
   pip install -r requirements.txt

3. 运行占位示例：

   echo "Hello SO101" > examples_input.txt
   python run_so101.py --input examples_input.txt --output out.jsonl
   cat out.jsonl

   你应该看到 JSON 格式的输出，包含反转后的字符串作为 "output" 字段。

4. 运行 smoke tests：

   pip install pytest
   pytest -q

如何替换为真实 SO101 模型
- 在 run_so101.py 中替换 load_model 与 predict 两个函数的实现：
  - load_model: 从磁盘（或 huggingface hub）加载模型与分词器
  - predict: 执行 tokenizer -> model -> decode 的推理流程
- 把模型权重放入仓库的 models/ 目录或外部路径，并在运行时通过 --model-path 指定。

权重存储建议
- 如果权重大于几百 MB，不建议直接提交到仓库的主分支。
- 建议使用 Git LFS（对于大文件）或把权重放到 Release、对象存储（如 S3）并在 models/README_weights.md 中提供下载说明。

需要 GPU 支持？
- 若需�� GPU，请在虚拟环境中安装与 CUDA 匹配的 torch 包（参见 PyTorch 官方安装页），并在 requirements.txt 中移除或改为相应的 CUDA 轮子安装命令。

若需我把真实模型权重与调用逻辑集成，请提供源码或上游仓库链接，我会把它合并并调整依赖。
