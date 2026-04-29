# 案例：支付 API 签名错误诊断

## 问题概述

支付集成返回 401 签名错误，导致支付流程失败。

## 错误现象

```
HTTP 500 Error
API Response: 401 SIGN_ERROR
Message: 签名错误，请检查后再试
```

## 诊断过程

### 第一步：信息收集
- 检查服务器日志
- 验证环境变量配置
- 查看证书文件是否存在

### 第二步：根本原因分析
发现 Authorization header 中的 `serial_no` 字段使用了错误的值：
- ❌ 使用了平台公钥 ID
- ✅ 应该使用商户证书序列号

### 第三步：分阶段修复

**修复 1：添加缺失的 HTTP Header**
```typescript
headers: {
  'Accept': 'application/json',  // 微信 API 要求
  'Authorization': authHeader,
}
```

**修复 2：改用正确的支付模式**
```typescript
// 从 Native 模式改为 H5 模式（网页支付）
const url = '/v3/pay/transactions/h5';
```

**修复 3：添加正确的应用 ID**
```typescript
const body = JSON.stringify({
  appid: process.env.WECHAT_APPID,  // 必需字段
  mchid: process.env.WECHAT_MERCHANT_ID,
  // ...
});
```

## 关键发现

| 问题 | 原因 | 解决方案 |
|------|------|--------|
| 签名错误 | serial_no 使用错误的 ID | 使用正确的证书序列号 |
| 缺少 Header | API 要求 | 添加 Accept header |
| appid 不匹配 | 支付模式选择错误 | 改用 H5 模式 |

## 修复结果

✅ 支付流程正常工作  
✅ 单元测试全部通过  
✅ 生产就绪

## AI 工作方法

```
收集信息 → 分类问题 → 深度诊断 → 优先级排序 → 分阶段修复 → 充分验证
```

### 关键技能
1. **日志分析** - 从日志中提取关键信息
2. **代码审查** - 识别代码中的问题
3. **API 理解** - 理解第三方 API 的设计意图
4. **系统化诊断** - 分层逐步排除法

## 学到的经验

1. **不同的 ID 用途不同**
   - 商户证书序列号：用于签名
   - 平台公钥 ID：用于验证回调
   - 应用 ID：用于支付模式

2. **支付模式的选择**
   - Native 模式：公众号/小程序
   - H5 模式：网页
   - APP 模式：移动应用

3. **API 集成的最佳实践**
   - 完整的参数验证
   - 清晰的错误消息
   - 详细的日志记录
   - 充分的单元测试

## 相关文件

- `server/wechat-pay.ts` - 支付核心实现
- `server/wechat-pay.test.ts` - 单元测试
- `server/routers/payment.ts` - 支付 API 路由

---

**修复状态：** ✅ 完成  
**修复时间：** 2026-04-29
