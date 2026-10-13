# T11–T20官方条款与适用性核查

访问2026-10-13 JST；新模型接口基线2026-07-28。上一轮T01–T10与S01–S12引用保留，来源快照与许可证据不重复研究。N01–N07均本轮实际打开并定位章节；不是完整协议符合性审核。

|ID|官方链接|具体条款|适用性|
|---|---|---|---|
|N01|[官方规范](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http)|Security & Endpoint; Standard Request Headers; Server Validation; Schema Extension; Value Encoding|T11–T13；仅HTTP，无OAuth前提|
|N02|[官方规范](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)|Output Schema / Structured Content; Security Considerations|T14/T20；Server MUST与client SHOULD分开|
|N03|[官方规范](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization)|Scope Selection Strategy; Step-Up Authorization Flow|T18；HTTP OAuth，scope ceiling为本项目policy|
|N04|[官方规范](https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation)|Form Elicitation; URL Mode; sensitive input restrictions|T17；MRTR机制；不打开URL|
|N05|[官方规范](https://modelcontextprotocol.io/specification/2026-07-28/server/resources)|Security Considerations|T19；file URI roots路径约束|
|N06|[官方规范](https://modelcontextprotocol.io/specification/2026-07-28/basic)|Result Responses; Error Responses|T16；响应id关联，异常error例外|
|N07|[官方规范](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/security-considerations)|Authorization Code Protection|T15；PKCE支持/S256|

所有复现方法是本项目设计，官方出处支持被测不变量，不能证明本项目复现成功。T11非法已提供Origin与缺Origin分开；T12新镜像头只按2026验；T13stdio可忽略该扩展；T14客户端验证是SHOULD；T15不等同issuer保护；T17form凭据采集不允许、URL交互不在MCP client收凭据；T18用户scope ceiling需事先声明；T19虚拟路径不证明OS/symlink约束；T20虚拟时钟不证明真实性能。
