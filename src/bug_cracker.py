import sys
import re
import json

def analyze_error(error_log):
    """
    分析错误日志并尝试分类维度。
    """
    dimensions = {
        "A": {"name": "局部逻辑错误", "score": 0, "indicators": [r"IndexError", r"KeyError", r"TypeError", r"AttributeError", r"ZeroDivisionError"]},
        "B": {"name": "上下文/状态污染", "score": 0, "indicators": [r"Deadlock", r"Race condition", r"Global variable", r"State mismatch", r"Cache"]},
        "C": {"name": "上游数据/外部依赖", "score": 0, "indicators": [r"ConnectionError", r"Timeout", r"404 Not Found", r"500 Internal Server Error", r"JSONDecodeError"]},
        "D": {"name": "AI 模型盲区", "score": 0, "indicators": [r"Reflection", r"Metaprogramming", r"Async callback", r"Memory leak"]}
    }
    
    for dim, info in dimensions.items():
        for indicator in info["indicators"]:
            if re.search(indicator, error_log, re.IGNORECASE):
                info["score"] += 1
                
    # 排序得分最高的维度
    sorted_dims = sorted(dimensions.items(), key=lambda x: x[1]["score"], reverse=True)
    return sorted_dims

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 bug_cracker.py <error_log_file>")
        sys.exit(1)
        
    log_file = sys.argv[1]
    try:
        with open(log_file, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
        
    results = analyze_error(content)
    
    print("--- Bug 顽固性诊断报告 ---")
    print(f"分析日志长度: {len(content)} 字符")
    print("\n建议关注维度:")
    for dim_id, info in results:
        if info["score"] > 0:
            print(f"- [{dim_id}] {info['name']} (匹配项: {info['score']})")
    
    if results[0][1]["score"] == 0:
        print("- 无法自动识别明显特征，建议从 [B] 状态污染或 [D] 模型盲区入手手动排查。")
        
    print("\n--- 结束报告 ---")

if __name__ == "__main__":
    main()
