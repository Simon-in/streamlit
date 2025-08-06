# 🔧 Streamlit SQL生成工具

一个强大且安全的SQL语句生成工具，基于Streamlit构建，支持多种SQL操作的批量生成。

## ✨ 功能特性

### 🎯 核心功能
- **CREATE TABLE** - 根据配置文件生成建表语句
- **SELECT** - 支持单表查询和批量多表查询
- **INSERT** - 批量生成插入语句
- **UPDATE** - 简单更新语句生成
- **MERGE** - 数据合并语句生成
- **DELETE** - 删除并重新插入数据
- **TRUNCATE** - 支持简单清空和清空后插入

### 🚀 高级功能
- **视图管理** - CREATE VIEW语句生成和管理
- **索引优化** - 智能索引创建和优化建议
- **存储过程** - 存储过程和函数生成
- **触发器** - 数据库触发器创建
- **约束管理** - 主键、外键、唯一约束等

### 📚 模板中心
- **基础查询** - 常用SELECT、JOIN、聚合查询模板
- **数据操作** - INSERT、UPDATE、UPSERT模板
- **表结构** - 标准表结构模板（用户表、审计表等）
- **性能优化** - 查询分析、索引优化模板
- **数据分析** - 数据质量检查、时间序列分析

### 📊 数据分析
- **文件分析** - Excel文件结构和内容分析
- **数据概况** - 数据质量统计和分布分析
- **SQL格式化** - SQL语句美化和语法检查
- **性能建议** - SQL性能优化建议

### 📚 历史记录
- **操作记录** - 自动保存所有SQL生成历史到JSON文件
- **收藏功能** - 收藏常用SQL语句
- **搜索功能** - 快速搜索历史记录
- **统计分析** - 使用情况统计和分析
- **导出功能** - 支持JSON、CSV格式导出

### 🛡️ 安全特性
- **文件验证** - 严格的文件类型、大小和内容验证
- **SQL注入防护** - 全面的SQL注入攻击检测和防护
- **输入验证** - 表名、列名等输入的安全性验证
- **恶意内容检测** - 防止上传包含恶意代码的文件

### 🚀 性能优化
- **智能缓存** - 文件读取和SQL生成的缓存机制
- **延迟加载** - 组件按需加载，提升响应速度
- **内存监控** - 实时监控内存使用情况
- **Session优化** - 自动清理过期的session数据

### 🎨 用户体验
- **现代化UI** - 美观的用户界面设计
- **响应式布局** - 适配不同屏幕尺寸
- **实时反馈** - 丰富的状态提示和错误信息
- **示例展示** - 配置格式示例图片

## 📁 项目结构

```
streamlit-main/
├── main/
│   ├── main.py              # 主应用入口
│   ├── config.py            # 配置管理
│   ├── utils.py             # 工具函数
│   ├── SQL.py               # 基础SQL生成器
│   ├── advanced_sql.py      # 高级SQL功能
│   ├── sql_templates.py     # SQL模板系统
│   ├── history_manager.py   # 历史记录管理（JSON存储）
│   ├── streamlit_example.py # Streamlit组件示例
│   ├── security.py          # 安全验证模块
│   ├── performance.py       # 性能优化模块
│   ├── static/              # 静态文件
│   │   └── sql_example.xlsx # 样例配置文件
│   └── image/               # 示例图片
│       ├── create.png
│       ├── select.png
│       ├── merge.png
│       └── ...
├── requirements.txt         # 项目依赖
├── README.md               # 项目说明
└── .gitignore             # Git忽略文件
```

## 🛠️ 技术架构

### 核心组件
- **主应用** (`main.py`) - Streamlit应用主入口，处理页面路由和用户交互
- **配置管理** (`config.py`) - 集中管理应用配置项和常量
- **工具模块** (`utils.py`) - 提供通用功能和辅助函数
- **SQL生成器** (`SQL.py`) - 核心业务逻辑，负责各种SQL语句生成
- **安全模块** (`security.py`) - 文件验证和SQL注入防护
- **性能模块** (`performance.py`) - 缓存管理和性能优化

### 设计模式
- **单一职责原则** - 每个模块负责特定功能
- **开放封闭原则** - 易于扩展新功能
- **依赖注入** - 模块间低耦合设计
- **装饰器模式** - 性能监控和缓存功能

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Streamlit 1.39.0+

### 安装步骤

#### 🚀 一键安装（最简单）

1. **克隆项目**
```bash
git clone <repository-url>
cd streamlit-main
```

2. **一键配置**
```bash
python quick_setup.py
```
*此脚本会自动配置清华镜像源、安装依赖、创建启动脚本*

3. **启动应用**
- Windows: 双击 `start.bat` 文件
- Linux/Mac: 运行 `./start.sh`
- 或者运行: `streamlit run main/main.py`

#### 🛠️ 手动安装

1. **克隆项目**
```bash
git clone <repository-url>
cd streamlit-main
```

2. **配置pip镜像源（推荐）**
```bash
# 自动配置清华镜像源
python setup_pip_mirror.py

# 或手动配置
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/
```

3. **安装基础依赖**
```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ -r requirements-minimal.txt
```

4. **安装完整依赖（包含可选功能）**
```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ -r requirements.txt
```

5. **运行应用**
```bash
streamlit run main/main.py
```

6. **访问应用**
打开浏览器访问 `http://localhost:8501`

#### 📦 依赖说明

- **基础依赖** (`requirements-minimal.txt`): 仅包含核心功能所需的包
- **完整依赖** (`requirements.txt`): 包含所有功能和开发工具
- **可选依赖**: 
  - `python-magic`: 文件类型检测（可选，提升安全性）
  - `psutil`: 性能监控（可选，提供内存监控）
  - 开发工具: pytest, black, flake8（仅开发时需要）

#### 🔧 镜像源配置

**推荐使用清华镜像源**以提升安装速度：

```bash
# 方法1：使用配置脚本（推荐）
python setup_pip_mirror.py

# 方法2：手动配置
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/

# 方法3：临时使用
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ <package>
```

**其他镜像源选择：**
- 阿里云：`https://mirrors.aliyun.com/pypi/simple/`
- 豆瓣：`https://pypi.douban.com/simple/`
- 腾讯云：`https://mirrors.cloud.tencent.com/pypi/simple/`

## 📖 使用指南

### 1. 文件上传
- 支持Excel (.xlsx, .xls)、CSV (.csv)、文本文件 (.txt)
- 最大文件大小：10MB
- 自动进行安全验证

### 2. 配置格式
每种SQL操作需要特定的Excel工作表格式：

#### CREATE TABLE
工作表名：`create`
| Domain | Table | Column | DataType |
|--------|-------|--------|----------|
| schema | users | id | INT |
| schema | users | name | VARCHAR(100) |

#### SELECT
工作表名：`select`
| Table | Fields |
|-------|--------|
| users | id, name, email |
| orders | order_id, user_id |

#### INSERT
工作表名：`insert`
| Table | Columns | Values |
|-------|---------|--------|
| users | id, name | 1, 'John' |

#### 其他操作
请参考样例文件中的格式说明。

### 3. SQL生成
- 选择对应的SQL操作类型
- 上传配置文件或手动输入参数
- 点击生成按钮
- 查看生成的SQL语句
- 下载SQL文件

## 🔒 安全特性

### 文件安全
- 文件类型白名单验证
- 文件大小限制
- 恶意内容检测
- MIME类型验证

### SQL安全
- SQL注入攻击检测
- 危险关键词过滤
- 输入参数验证
- 安全日志记录

## 🎯 性能优化

### 缓存策略
- Excel文件读取缓存
- SQL语句生成缓存
- 静态资源缓存

### 内存管理
- 自动清理过期数据
- 大文件分片处理
- 内存使用监控

### 用户体验
- 延迟加载组件
- 操作进度提示
- 错误友好提示

如果您遇到问题或有建议，请：
1. 查看文档和FAQ
2. 搜索已有的Issues
3. 创建新的Issue描述问题
4. 联系维护团队

---

⭐ 如果这个项目对您有帮助，请给我一个星标！
