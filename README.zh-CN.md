# Practical AI Systems（实用 AI 系统）

[English](README.md) | **简体中文**

<p align="center">
  <strong>构建小型 AI 系统，测试它们会在哪些地方出错。</strong><br />
  30 个离线优先项目，包含可运行代码、测试、合成评估和坦诚说明的局限性。
</p>

> **项目范围：**这是一个学习实验室，不是生产工具包，也不是排行榜。系统使用小型合成样例，便于观察行为；这些分数不能证明真实场景中的表现。

## 从这里开始

**按目标选择：**

- **第一个 AI 项目：**[文档问答](systems/doc_qa/README.md)——检索证据、引用答案，并在证据不足时拒绝作答。
- **实用 Python：**[发票字段抽取](systems/invoice_extract/README.md)——提取字段并校验金额。
- **团队评估：**[语音代理评估](systems/voice_eval/README.md)——分别衡量任务成功率、不安全操作和延迟。

## 60 秒运行一个系统

需要 Python 3.10 及以上版本和终端。基线无需 API 密钥、模型下载或第三方 Python 包。

```bash
git clone https://github.com/shivamnegi92/practical-ai-systems.git
cd practical-ai-systems
python3 -m systems.doc_qa.app "How much does Pro cost?"
```

你应该会得到带有来源引用的答案。试着询问示例文档中没有的信息，系统应该拒绝作答。每个系统的说明都包含对应命令、评估、测试和局限性。

```bash
python3 -m systems.doc_qa.evaluate
python3 -m unittest systems.doc_qa.test_doc_qa -v
```

更喜欢点击而不是终端？请[在在线图库中探索全部 30 个浏览器演示](https://shivamnegi92.github.io/practical-ai-systems/)。每个系统还提供零依赖 Web 应用；安装 Node 20 及以上版本后，可运行 `make serve SYSTEM=doc_qa` 在本地启动。

## 你可以在这里学到什么

- **构建基线：**词法检索、信息抽取、路由、缓存和文档处理。
- **评估行为：**添加合成测试用例，衡量任务相关结果并检查失败。
- **设计防护措施：**限制工具权限，对副作用要求审批，并测试对抗性输入。
- **运行系统：**跟踪成本和延迟、模拟发布，并检查执行轨迹。

## 浏览 30 个可运行系统

[系统索引](README.md#browse-the-30-runnable-systems)按难度递增，涵盖初级、中级和高级项目。索引由每个系统的 `system.json` 清单生成。打开项目指南，然后运行测试和评估器。每项结果都链接到合成测试用例并注明样例规模；这是教学辅助材料，不是基准测试。

## 探索精选工具箱

[精选工具箱](README.md#explore-the-curated-toolbox)按能力整理了 6 个领域的 20 个项目。每个条目都链接到其规范来源，并标注审核状态。

## 如何使用本项目

- **学习者：**从快速入门开始，运行测试和评估；修改一个合成用例，观察系统如何变化。
- **讲师：**将系统作为实验，让学习者复现基线、添加边界案例，并解释结果和局限性。
- **专业团队：**把这些内容视为设计模式，而不是生产服务。在用于真实工作流前，审查隐私、授权、依赖项和评估缺口。

## 贡献

欢迎提交任何规模的贡献，从修复 README 错字到新增完整系统均可。你可以直接提出想法或发起 Pull Request；**所有改动都需要维护者批准后才会合并**。Pull Request 是提案，不代表一定会被接受。

```bash
make check                                   # 运行 CI 中的全部检查
make new SYSTEM=my_system                    # 使用 Python、Web 应用、测试和 npm 锁文件创建新系统
make test SYSTEM=doc_qa                      # 测试一个系统
make eval SYSTEM=doc_qa                      # 重新生成该系统的 eval/results.json
make serve SYSTEM=doc_qa                     # 在 http://localhost:4173 启动 Web 应用
```

- **5 分钟：**修复 README，或[报告失败案例](https://github.com/shivamnegi92/practical-ai-systems/issues/new?template=failing-case.yml)。
- **30 分钟：**添加能使系统出错的评估用例，或改进 Web 应用。
- **几小时：**按照[新增系统指南](docs/ADDING_A_SYSTEM.md)提议一个新系统。欢迎先讨论范围，再开始实现。

请阅读[贡献指南](CONTRIBUTING.md)和[行为准则](CODE_OF_CONDUCT.md)。

## 相关资源

- [学习路径](catalog/paths.md)：通过工具和项目循序渐进地学习。
- [精选工具箱](catalog/README.md)：按能力分类并经过审核的外部项目。
- [实践指南](recipes/)：常见工作流的原创指南。
- [评估手册](benchmarks/README.md)：设计有代表性的测试并解读结果。
- [语音代理评估语料与 TRG](https://github.com/shivamnegi92/voice-agent-eval-corpus)：专注实时语音代理评估的配套语料库、报告规范与验证工具。
- [更新日志](CHANGELOG.md)：近期项目更新。

## 许可

原创内容采用 [CC0 1.0](LICENSE) 发布。链接指向的项目保留各自的许可和使用条款。
