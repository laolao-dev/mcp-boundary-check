# ENGINEERING_GATE_PROTOCOL_V2
日期：2026-10-13 JST。范围：MCP Boundary Check自有T01最小stdio fixture。
本文件替代未来实验的单体Gate逻辑；旧ENGINEERING_GATE_REVIEW.md及历史验收保留，不改成已通过。
GATE_A_STATUS=BLOCKED（A5具体fixture源码/启动清单尚未存在）
GATE_A_DESIGN_REVIEW=PASS（方案级静态预检）
GATE_B_STATUS=NOT_RUN
RUNTIME_TEST=NOT_RUN
本轮协议设计不授予代码编写/运行许可。本轮无fixture实施。

## 循环阻塞审计
旧条件G5要求“真实受控运行可复现”，又规定十项通过才能写/运行代码。形成：无运行证据→不许实现/运行→拿不到证据。
修正方法不是把G5改成文档PASS，而是将其全部移到Gate B；Gate A不能以Gate B任何运行结果为前提。
已有独立目录、版本、policy、输入/预期、无付费/无外部目标等静态证据继续使用，不重新初始化/重复侦察。

## 两个Gate与独立授权的状态机
1. DESIGN_ONLY：编写模型/spec与纯数据，运行证据保持NOT_RUN。
2. 经单独明确授权，允许准备自写fixture/runner源码和启动清单；此准备授权不自动允许启动进程。可以由用户在同一明确授权中授予“仅Gate A全部PASS后启动”的条件许可。
3. STATIC_PREFLIGHT：对拟执行源码/清单完成Gate A，全部PASS才进入AWAIT_EXPERIMENT_AUTHORIZATION。源代码缺失为BLOCKED，不需要运行证据来解锁。
4. 授权实验必须点名仅T01自有stdio、7个case、0JPY、无网络、限120秒、无ABL改动和限定目录；授权payload绑定reviewed源码/解释器/输入/policy哈希。条件授权可覆盖第2步，但通过A之前不得运行。
5. 运行前复核当前hash/paths仍与授权绑定相同。变化→失效、回Gate A静审；未经确认不能换成第三方Server/HTTP/模型。
6. EXPERIMENT：只执行获准最小fixture，收集OBSERVED_RUNTIME证据。完成后独立评估Gate B。
7. B PASS也只允许形成受控技术结论；扩大测试/真实目标/发布/付费仍须另行Gate与授权。市场Gate独立NOT_RUN。
本轮停在第1步；A5缺源码，不是等待B通过。没有自动运行、自动授权或所谓批准日志。

## Gate A：安全预检（全部是静态可判断条件）
|ID|必要条件|当前状态|现有证据/剩余证据|
|---|---|---|---|
|A1|独立新目录、原档案及ABL不可写入实验|PASS|本轮目录；evidence/PRIOR_BASELINE.json；evidence/FINAL_VERIFICATION.json保护范围|
|A2|仅自有T01 stdio，两工具、合成身份/数据，禁止网络/真实秘密/OS破坏|PASS|上轮T01_TEST_SPEC.md；evidence/FIXTURE_EXPERIMENT_PLAN.json|
|A3|明确现有运行时与许可，零安装/零付费|PASS|上轮DEPENDENCY_REVIEW.json；本轮runtime文件存在/PSF许可hash复核|
|A4|正对照、越权反例、检测有效性负控、确定性oracle和证据格式|PASS|上轮6case及本轮第7case设计；计划验证见STATIC_REVIEW.json；不表示测试通过|
|A5|拟执行fixture/runner源码已静审；固定绝对启动路径、shell=false、hash绑定、最小env、无网络/任意命令接口|BLOCKED|目前无该源码/launch manifest。仅文档不能证明实现控制；需独立准备授权后生成并逐项静审，不需提前运行|
|A6|总预算/资源终止/回滚与残留检查明确|PASS|本协议；7case各10秒、总120秒、最多一次授权范围内诊断重试；固定临时根、已记录pid|
|A7|协议版本/消息结构/可信角色与stderr观察责任分开|PASS|上轮spec，REFERENCES_T11_T20.md；元数据不作身份、Server内授权、输出resultType待实现静审核对|
Gate A证据含源码文本审查、imports/API清单、敏感操作inventory、静态路径解析及manifest SHA-256。不得以启动fixture来“证明A”。源码/命令尚无时A5 BLOCKED；无额度/范围时相应条件FAIL/BLOCKED。
Gate A全部PASS ≠ 已授权运行。授权记录单独保存为EXPERIMENT_AUTHORIZATION（目前不存在）。

## Gate B：首次受控运行验收（本轮全部NOT_RUN）
|ID|运行条件|当前状态|需要的实际证据|
|---|---|---|---|
|B1|指定源码与解释器通过stdio真实交换消息|NOT_RUN|启动manifest/hash、stdout消息、pid/run_id、时间|
|B2|合法读/写正向3case可用，计数与状态正确|NOT_RUN|实际MCP结果+Server handler telemetry+终态|
|B3|reader越权与clientInfo伪称不进write handler、无副作用|NOT_RUN|两case实际请求/拒绝/handler0/state BASE|
|B4|非法role参数schema拒绝，与权限测试分开|NOT_RUN|JSON-RPC -32602响应/handler0|
|B5|故意只对T01关闭授权的负控被oracle判FAIL|NOT_RUN|第7case真实ALLOW/handler1/side_effect1和独立判定FAIL；预期“fixture失败”是检测器正确区分，不是漏洞发现|
|B6|证据非expected抄录且跨观察点一致|NOT_RUN|Server不接expected文件，request-id/事件顺序/response/state相互校验，原始文件hash|
|B7|在预算内结束，无网络/真实改动，进程退出/原档案ABL未变|NOT_RUN|运行计时、已记录pid退出、源码静态限制与实际运行观察、前后hash。无网络若无OS强制限制证据只作本fixture范围结论，不宣称恶意软件沙箱|
只有B1–B7均有充分真实证据并PASS，Gate B才PASS。
安全fixture越权为FAIL；正常路径/消息/日志失效为BLOCKED；负控未被判FAIL为检测能力FAIL。没有运行时NOT_RUN；缺日志不能补造PASS。
负控case的目标状态FAIL与Gate B5验收PASS是两层状态，报告必须分开，不把预期/目标的FAIL直接计成本工具失败。

## 首次实验的最小范围
沿用上一轮6case，追加1个故意vulnerable的N_WRITE_READER负控，共7case。每case独立自写fixture进程，固定启动角色；只变内存note BASE→WRITTEN。负控允许Server漏授权一次以验证oracle，不接真实文件、客户或公网。
解释器用已存在CPython3.12.14标准库；不安装MCP SDK、不复制ABL、不调用模型、无HTTP listener。未知角色/任意command/env/URL输入必须拒绝。shell=false；最小env允许工作所需OS项但不全量继承用户凭据。
原始stderr仅作为自有fixture telemetry；若后续任意第三方stdio Server，不能自动信stderr计数，需要重新设计观察层与授权。
2026-07-28 response.result.resultType="complete"属于实现前静审清单；旧样例仅输入，无运行结果。预期JSON observed=null不能变成observed evidence。
7case×10秒；总运行120秒（含关闭与收尾），输出上限每case64KiB、整个run512KiB，这是本实验政策，不是MCP规范硬限。达到预算停止，不扩大benchmark。

## 回滚与失效条件
所有source/run目录限定本轮项目内部work/t01-experiment/<run-id>（现在未创建）；resolved absolute根必须在允许目录，避免递归删除home/ABL。实验只能结束本轮已记录pid，不按名称杀进程。close stdin、等退出、必要时结束记录pid；保留stdout/stderr/manifest，清理只针对核验过的临时根。
Gate A、授权和Gate B的版本、输入、source hash不一致；网络/外部目标/真实秘密出现；超时/预算突破；证据泄漏→STOP。恢复只处理本轮生成文件，不覆盖旧档案。明确剩余副作用/未退出进程，不能“回滚成功”口头替代观察。
本轮回滚未运行，运行残留检查NOT_RUN。

## 可直接审阅的后续授权文本（不是已授予权限）
“允许仅在MCP Boundary Check独立目录准备T01自写stdio fixture/runner及启动manifest；先完成Gate A全部静态检查。仅A全部PASS且源码/输入hash固定后，允许启动7case（6安全case+1纯内存负控），总120秒、0JPY、无网络/第三方/真实Token/真实破坏，ABL只读，保存原始证据；任何不符停止，不扩大产品范围。”
用户可只授权准备源码而不运行；此时Gate A通过后仍等待单独运行授权。不能把本协议或用户当前“仅模型设计”指令当作该授权。

## 验证结论与商业边界
本轮能证明：文档逻辑不再要求B先于A；20条模型静态完整、去重；原有数据保留。
不能证明：fixture已安全、T01实际通过、全协议兼容、真实Server有漏洞、模型抗注入、市场成立。
当前唯一最小下一步是审阅/单独授权这个受控准备与条件执行范围，不是再用文档填B PASS，也不是建设大规模CLI。
