# 官方条款核验与依赖边界

目标工作日2026-10-14；实际访问日期2026-10-13 JST。官网当前正式版本仍为2026-07-28。旧稿引用保留，本轮只核与T01–T10有关条款，不重新侦察市场。

|ID|来源|版本|已核条款|
|---|---|---|---|
|S01|[MCP Versioning](https://modelcontextprotocol.io/docs/2026-07-28/learn/versioning)|2026-07-28 Current|Revisions; Negotiation|
|S02|[MCP Base Protocol](https://modelcontextprotocol.io/specification/2026-07-28/basic)|2026-07-28|Statelessness; _meta / Per-request protocol fields|
|S03|[MCP Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)|2026-07-28|User Interaction Model; Capabilities; Tool; Security Considerations|
|S04|[MCP Authorization](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization)|2026-07-28|Resource Parameter Implementation; Token Handling; Authorization Response Validation|
|S05|[MCP Security Best Practices](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices)|2026-07-28|Token Passthrough; Confused Deputy Problem; SSRF; State Handle Hijacking; Mix-Up Attacks; Local MCP Server Compromise|
|S06|[MCP stdio](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio)|2026-07-28|Request Metadata; Receiving Messages; Shutdown|
|S07|[MCP Streamable HTTP](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http)|2026-07-28|Security & Endpoint; Standard Request Headers; Server Validation|
|S08|[Legacy MCP Security Best Practices](https://modelcontextprotocol.io/docs/2025-11-25/tutorials/security/security_best_practices)|2025-11-25|Session Hijacking|
|S09|[OWASP GenAI LLM Top 10 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/)|2026; published 2026-08-03|LLM01 Prompt Injection; LLM02 Sensitive Information Disclosure; LLM03 Excessive Agency (PDF reviewed in prior task)|
|S10|[Python History and License](https://docs.python.org/3/license.html)|web currently 3.15.0; local runtime 3.12.14 separately verified|PSF License Version 2; incorporated software notices|
|S11|[RFC8707](https://www.rfc-editor.org/info/rfc8707/)|RFC8707; 2020-02|Resource indicators / resource audience binding|
|S12|[RFC9207](https://www.rfc-editor.org/info/rfc9207/)|RFC9207; 2022-03|§2.4 client issuer validation|

## 适用性校正
- stdio为进程通道；HTTP OAuth凭据要求不直接套用到stdio。clientInfo自报信息不作身份。
- 2026逐请求必须含protocolVersion/clientCapabilities；clientInfo为可选，旧Tools页面示例上方对元数据的笼统描述以Base Protocol字段表为准。
- State Handle是应用对象标识；旧2025 Session Hijacking是另一层，不套session假设到2026。
- issuer矩阵：广告支持iss却缺失→拒绝；present mismatch→拒绝；匹配→可继续；未广告且缺失→规范允许继续。测试需保留分支，不能一刀切。
- 最新版实际授权/传输集成尚未运行；官网规范确定不等于所选SDK已兼容。
- S09本轮仅刷新官方发布入口；详细风险编号来自上一任务已核PDF，不冒充本轮完整重读。
- Authorization/security猜测URL返回Internal Error，未计有效来源；使用已成功核验的Authorization正文与Security Best Practices对应章节，未重试无效URL。

## 最小工程依赖与许可证
拟议T01离线核心及stdio自有fixture只用现有CPython 3.12.14标准库（json/subprocess/hashlib/pathlib/time）；不引入MCP SDK、LLM、浏览器、容器或HTTP OAuth服务。该选择仍是待实施方案，不是已实现组件。
本机已用绝对路径实际执行--version，输出Python 3.12.14：
<LOCAL_PATH>
本机LICENSE.txt实际读取，主许可PSF License v2，另有历史/第三方组件条款；不重分发Python二进制，本轮不安装任何软件。模块可用性见evidence/DEPENDENCY_REVIEW.json，仅runtime预检，不是T01安全测试。

|组件|采用/复用|许可证核查|剩余风险|
|---|---|---|---|
|现有CPython 3.12.14|仅未来执行标准库，非打包发布|本机LICENSE.txt + S10；hash见依赖证据|无法据runtime版本宣称MCP符合性；未来分发需再次核NOTICE|
|MCP SDK|首个方案不使用|NOT_RUN（没有所选包）|若改为SDK须锁定版本、兼容性和许可后重开G7|
|ABL代码|复制0、修改0；仅架构参考|现有LICENSE头Apache-2.0已核|未来复制必须逐文件归属/NOTICE核查；今日不借旧测试|
|项目自身未来代码|未编写|开源LICENSE尚未选定|发布Gate未通过，不影响无外部分发的自有测试设计|

不把G7的“当前最小无第三方包方案已核”泛化为所有未来依赖/开源发布许可证已完成。
