# models/README_weights.md

模型权重存放说明

- 若权重文件较小 (< 100MB)：可以放入仓库的 models/ 目录并提交。
- 若权重大于仓库推荐大小（或超过 GitHub 单文件限制），请使用下列选项之一：
  - Git LFS：跟踪大型二进制文件（需要在本地安装 git-lfs 并在仓库中开启）。
  - Releases：把权重文件放在 GitHub Releases 附件并在 README 中放下载链接。
  - 外部对象存储（S3、阿里云 OSS 等）：在 README 中提供下载与校验（sha256）信息。

放置约定
- 本示例约定：把模型文件放在 models/<model_name>/ 下，运行时通过 --model-path 指定到该目录。

示例：
- models/so101-real/
    - config.json
    - pytorch_model.bin
    - tokenizer.json

安全与许可
- 请确保你拥有发布或存储该权重的权限，遵守模型许可证。
