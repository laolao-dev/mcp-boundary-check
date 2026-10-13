# T01_TEST_SPEC｜Controlled Server Tool Authorization
DESIGN STAGE；目标工作日2026-10-14，实际编写2026-10-13 JST。
T01_RUNTIME_TEST=NOT_RUN。没有Server脚本/CLI/扫描器，本文件只定义可执行契约。

## 核心技术假设与责任组件
H-T01：对自有MCP Server的直接调用，能够在明确主体/工具policy与Server内计数下，确定性区分“低权限被拒”与“低权限进入受保护handler”。
必须把检查放在Server收到tools/call之后、调用handler之前。CLI/runner不得替Server预先拒绝reader请求；tools/list过滤也不是授权证据。
第一切片为stdio自有fixture；目标协议2026-07-28。HTTP、OAuth、第三方Server、真实Host/LLM不在该切片。OS进程隔离保护实验数据，不声称阻止拥有同一OS用户权限的人改启动配置。

## A/B 身份与可信来源
- A正常授权用户writer-fixture：可读可写。
- B未授权用户reader-fixture：可读、不可调用受保护write。
- 身份在可信测试runner启动各独立Server时以最小环境MBC_FIXTURE_ROLE=writer/reader固定；Server必须启动后冻结该值。
- 不存在真实token；请求arguments/_meta/clientInfo里的user/role/name不改身份。此映射为实验fixture身份，不是MCP规范认证、OAuth token或真实多租户身份。
- 每case新Server进程，角色由case manifest（runner可信输入）选定，攻击输入只能写MCP请求。未知启动角色拒绝启动；不得从完整用户env继承凭据。

## C/D 工具与策略
C=fixture.read_note，inputSchema为空object，additionalProperties=false。返回虚拟note值，reader/writer均允许；handler读取1次，mutation0。
D=fixture.write_note，arguments.value为固定长度1–64的合成string，其余字段禁止；只有writer允许，note在内存从BASE变为WRITTEN。
对象固定note-1，不测试跨租户ownership（T08）；工具description/annotation不参与角色授予。策略文件只包含role→tool set及缺省DENY，无动态角色输入。

## 输入格式
数据文件evidence/T01_SAMPLE_INPUTS.json提供机器可读样例。外层含schema_version、protocol_version、role_source、policy和cases。
每case字段：case_id、launch_role、request（真实JSON-RPC结构）、initial_state、timeout_ms。launch_role属于runner manifest，不上wire。
MCP请求：jsonrpc=2.0；整数id唯一；method=tools/call；params.name/arguments/_meta。_meta含io.modelcontextprotocol/protocolVersion=2026-07-28及clientCapabilities={}；clientInfo可选（本样例加入名称/version用于诊断）。
不使用旧initialize握手。未来实现还需最小schema/metadata校验；如果target不支持版本，应BLOCKED，不静默回退。

## E/F 正反测试与调用流程
6个case，每case内存note重置BASE：
1. P_READ_READER：reader合法读取，ALLOW、read handler1、写副作用0。
2. P_READ_WRITER：writer合法读取，同上。
3. P_WRITE_WRITER：writer合法写，ALLOW、write handler1、写副作用1，note=WRITTEN。
4. N_WRITE_READER：reader直接写，DENY、write handler0、写副作用0，note=BASE。
5. N_CLIENTINFO_SPOOF：reader声明clientInfo.name=writer-fixture仍提交合法write参数；可信主体仍reader，DENY、handler0。
6. N_ARGUMENT_ROLE：reader写参数额外role=writer，schema拒绝、handler0；这个case只能证明非法参数拒绝，不能代替case4的权限测试。

请求顺序：可信runner创建临时工作目录并启动Server→发送一条case请求→读取按id对应MCP响应→收集Server stderr JSONL事件与终态→独立判定→关闭stdin/等待退出→下一case。
MCP错误表达：case4/5为tools/call result.isError=true，content包含固定非敏感FORBIDDEN；case6为JSON-RPC -32602。case1/2/3为isError=false。这些具体错误约定属于fixture契约，stdio没有HTTP403。
Server不能直接把expected_result复制为observed。expected文件仅runner持有，不传给Server。Server记录实际授权/handler/副作用轨迹，runner交叉核响应和终态。

## G 明确日志结构
每行evidence_type=OBSERVED_RUNTIME仅可在真正执行后生成；当前样例不用此值。
event字段：run_id、case_id、sequence、request_id、component、event_type、principal、role_source、tool、policy_sha256、request_sha256、decision、reason_code、handler_count、side_effect_count、note_hash_before/after。
顺序：request_received → schema_checked → principal_resolved → authorization_decided → handler_entered（只允许时）→ state_snapshot → response_sent。
Server stdout只含MCP消息，stderr是受控fixture telemetry，不把普通第三方stderr自动当可信证据。配对request_id、可读终态及事件；允许调用的进入事件恰好1次，无额外无id写调用。
Report每case有expected、observed、status、evidence_refs；未运行observed=null/status=NOT_RUN。不记录机器真实env、token或完整私密路径。

## H 自动判定与失败分类
安全行为PASS需要：正向3case全部成功且计数正确；case4/5拒绝、handler/副作用0；case6正确拒绝；note终态、响应、日志互相一致。
明确安全FAIL：reader case4/5出现ALLOW/成功返回、write handler>0或状态改变；拒绝文字不抵销已发生副作用。
测试协议失败/正常case失败/日志不完整：BLOCKED，reason=HARNESS_OR_EVIDENCE_INCOMPLETE；不能判安全PASS。所有未执行case NOT_RUN。
测试器的检测有效性未来可用一个显式local vulnerable fixture模式作负控：同样case4进入handler1/副作用1，独立oracle必须FAIL。该负控同样尚未实现，不作为今天成功发现。
退出码草案：0=安全模式全部适用PASS；1=至少一个有证据安全FAIL；2=BLOCKED/NOT_RUN/输入或观察不足。未运行的expected结构不是TEST_PASS。

## 隔离、资源与回滚
未来拟用已存在CPython3.12.14标准库，无安装、无LLM、无网络、无真实文件访问工具；仅进程stdio。进程只执行自写固定fixture绝对路径，shell=false，不接收任意启动命令。隔离不是恶意第三方二进制沙箱，不运行第三方包。
临时根位于本轮项目work/t01-run-<id>；不得设为ABL/用户home。保留证据仅写本轮输出路径。每case10秒，6case上限60秒；整个小运行上限120秒，失败最多一次诊断重试；禁止扩张benchmark。
回滚：关闭本轮启动的已记录pid；确认临时根resolved absolute仍在本轮work范围，再由用户授权流程/正常工具删除仅临时fixture数据；证据保留。今天未创建进程或临时fixture，实际回滚NOT_RUN。

## 验证力与更便宜办法
现在的表格/JSON审查比编写代码更便宜，已能检查role区分、case对照和预期判据；不能证明实现中的授权时序。
未来实现通过仅证明该fixture、该版本、该policy和观察范围内能得到可区分结果；不能证明第三方Server有漏洞、Host抗注入、MCP全规范符合或市场需求成立。
若安全fixture也失败，先定位runner/协议/日志/策略；若故意缺授权fixture未被判FAIL，检测假设被否证，停止扩张。需要Server真正运行的G5本轮NOT_RUN，所以工程Gate不能报告READY。
