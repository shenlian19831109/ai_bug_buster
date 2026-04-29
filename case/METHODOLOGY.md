# AI 诊断方法论

## 核心流程

```
问题 → 收集信息 → 分类 → 诊断 → 修复 → 验证
```

## 第一步：收集信息

```bash
# 查看错误日志
tail -100 logs/error.log

# 检查环境变量
env | grep -i "api\|key"

# 验证配置文件
ls -la config/

# 查看相关代码
grep -r "error_keyword" src/
```

## 第二步：问题分类

根据错误信息进行分类：

```
错误类型 → 可能的原因 → 优先级
401 Unauthorized → 认证失败 → 高
  ├─ 签名错误
  ├─ 密钥配置错误
  ├─ 使用了错误的 ID
  └─ Header 格式错误

400 Bad Request → 参数错误 → 中
  ├─ 缺少必需参数
  ├─ 参数格式错误
  └─ 参数值不匹配

500 Internal Error → 服务器错误 → 低
  ├─ 代码逻辑错误
  ├─ 资源不足
  └─ 外部服务故障
```

## 第三步：深度诊断

### 分层诊断法

```
第 1 层：基础配置
├─ 环境变量是否存在
├─ 配置文件是否正确
└─ 依赖是否安装

第 2 层：代码实现
├─ 逻辑是否正确
├─ 参数是否完整
└─ 错误处理是否完善

第 3 层：外部 API
├─ 请求格式是否正确
├─ 认证信息是否正确
└─ 响应是否符合预期

第 4 层：集成流程
├─ 业务流程是否正确
├─ 状态转移是否正确
└─ 错误恢复是否完善
```

### 诊断工具

```bash
# 日志分析
grep "ERROR\|WARN" logs/*.log | head -50

# 代码审查
git diff HEAD~1 src/payment.ts

# API 测试
curl -X POST https://api.example.com/pay \
  -H "Authorization: Bearer token" \
  -d '{"amount": 100}'

# 配置验证
echo $WECHAT_MERCHANT_ID
echo $WECHAT_API_V3_KEY
```

## 第四步：优先级排序

```
优先级 1（立即修复）
├─ 阻塞主流程的问题
├─ 安全相关的问题
└─ 数据损坏的问题

优先级 2（尽快修复）
├─ 影响用户体验的问题
├─ 性能问题
└─ 部分功能不可用

优先级 3（后续优化）
├─ 代码质量问题
├─ 文档不完整
└─ 非关键功能缺陷
```

## 第五步：分阶段修复

```
修复 1：最直接的问题
- 添加缺失的参数
- 修复明显的错误
- 验证修复是否有效

修复 2：架构问题
- 选择正确的模式
- 调整代码结构
- 重新验证

修复 3：完善和优化
- 添加错误处理
- 改进日志记录
- 添加单元测试
```

## 第六步：充分验证

```
单元测试
├─ 关键逻辑测试
├─ 边界情况测试
└─ 错误处理测试

集成测试
├─ 端到端流程测试
├─ 外部 API 集成测试
└─ 错误恢复测试

日志验证
├─ 检查初始化日志
├─ 检查执行日志
└─ 检查错误日志
```

## 常见模式

### 模式 1：ID 混淆

**特征：** 多个相似的 ID，使用了错误的 ID

**诊断：**
1. 列出所有相关的 ID
2. 理解每个 ID 的用途
3. 检查代码中使用的 ID

**解决：** 使用清晰的变量名，添加注释说明用途

### 模式 2：缺少必需参数

**特征：** API 返回"必填"或"缺少"错误

**诊断：**
1. 查看 API 文档
2. 列出所有必需参数
3. 检查代码中是否包含

**解决：** 添加参数验证，改进错误消息

### 模式 3：模式选择错误

**特征：** 使用了错误的 API 端点或模式

**诊断：**
1. 理解不同模式的用途
2. 确定当前使用场景
3. 选择正确的模式

**解决：** 添加注释说明选择原因，添加验证检查

## 最佳实践

### 1. 错误消息

```typescript
// ❌ 不好
throw new Error('Error');

// ✅ 好
throw new Error('WECHAT_APPID is not configured. Please set environment variable.');
```

### 2. 日志记录

```typescript
// ✅ 有用的日志
console.log('[Payment] Order created:', { orderId, amount });
console.log('[Payment] Auth header:', authHeader);
console.log('[Payment] API response:', response);
```

### 3. 代码注释

```typescript
// ✅ 解释"为什么"
// 使用 H5 模式而不是 Native 模式，因为这是网页支付
const url = '/v3/pay/transactions/h5';
```

### 4. 测试覆盖

```typescript
// ✅ 关键逻辑必须有测试
- 签名生成
- 参数验证
- 错误处理
- 状态转移
```

## 工具和命令

```bash
# 查看日志
tail -f logs/app.log

# 搜索关键字
grep -r "payment" src/

# 查看 git 历史
git log --oneline -10

# 运行测试
npm run test

# 检查类型
npm run type-check

# 代码格式
npm run format
```

---

**方法论版本：** 1.0  
**最后更新：** 2026-04-29
