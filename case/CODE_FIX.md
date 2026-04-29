# 代码修复示例

## 修复前（有问题）

```typescript
// ❌ 错误 1：使用了错误的 ID
const WRONG_ID = process.env.PLATFORM_PUBLIC_KEY_ID;

// ❌ 错误 2：使用了错误的支付模式
const url = '/v3/pay/transactions/native';

// ❌ 错误 3：缺少 appid
const body = JSON.stringify({
  mchid: process.env.MERCHANT_ID,
  description,
  out_trade_no: orderId,
  // ...
});

// ❌ 错误 4：缺少必需的 header
const headers = {
  'Content-Type': 'application/json',
  'Authorization': authHeader,
};
```

## 修复后（正确）

```typescript
// ✅ 正确 1：使用正确的证书序列号
const CERT_SERIAL = process.env.WECHAT_CERT_SERIAL;

// ✅ 正确 2：使用 H5 支付模式（网页支付）
const url = '/v3/pay/transactions/h5';

// ✅ 正确 3：添加 appid 字段
const body = JSON.stringify({
  appid: process.env.WECHAT_APPID,
  mchid: process.env.MERCHANT_ID,
  description,
  out_trade_no: orderId,
  scene_info: {
    h5_info: {
      type: 'Wap',
    },
  },
});

// ✅ 正确 4：添加必需的 header
const headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',  // ← 添加此行
  'Authorization': authHeader,
};
```

## 关键修改

### 1. Authorization Header 中的 serial_no

```typescript
// ❌ 错误
serial_no="${PLATFORM_PUBLIC_KEY_ID}"

// ✅ 正确
serial_no="${WECHAT_CERT_SERIAL}"
```

### 2. 支付模式选择

```typescript
// ❌ 错误 - Native 模式（扫码支付）
const url = '/v3/pay/transactions/native';

// ✅ 正确 - H5 模式（网页支付）
const url = '/v3/pay/transactions/h5';
```

### 3. 请求体结构

```typescript
// ❌ 错误
{
  mchid: "...",
  description: "...",
}

// ✅ 正确
{
  appid: "...",
  mchid: "...",
  description: "...",
  scene_info: {
    h5_info: {
      type: "Wap"
    }
  }
}
```

## 环境变量

```bash
# 必需的环境变量
WECHAT_MERCHANT_ID=your_merchant_id
WECHAT_API_V3_KEY=your_api_v3_key
WECHAT_APPID=your_app_id
WECHAT_CERT_SERIAL=your_cert_serial
```

## 测试

```bash
# 运行单元测试
npm run test -- payment.test.ts

# 预期结果
✓ Authorization header 格式正确
✓ 证书序列号正确
✓ 环境变量验证通过
✓ 请求体格式正确
```

---

**修复完成：** ✅  
**测试状态：** ✅ 全部通过
