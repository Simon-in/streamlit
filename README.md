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

### 📊 数据分析
- **数据概况** - 表结构分析和数据分布建议
- **SQL格式化** - 美化SQL代码，提高可读性
- **语法检查** - 检查SQL语法错误并提供修复建议

## 🛠️ 技术架构

项目采用模块化设计，目录结构如下：

```
sql_generator/           # 核心包
├── core/                # 核心功能模块
│   ├── sql_generator.py # SQL生成器
│   ├── sql_formatter.py # SQL格式化工具
│   └── advanced_sql.py  # 高级SQL功能
├── ui/                  # 用户界面模块
│   ├── main_app.py      # 主应用UI
│   └── streamlit_example.py # Streamlit示例组件
├── templates/           # SQL模板模块
│   ├── sql_patterns.py  # 常用SQL模式
│   └── sql_example.xlsx # 示例Excel模板
├── utils/               # 工具模块
│   ├── file_utils.py    # 文件处理工具
│   ├── ui_utils.py      # UI辅助工具
│   ├── history_manager.py # 历史记录管理
│   └── security.py      # 安全工具
├── config/              # 配置模块
│   └── constants.py     # 配置常量
└── assets/              # 静态资源
    ├── create.png       # 创建表示例图
    ├── select.png       # 查询示例图
    ├── insert.png       # 插入示例图
    └── ... 

scripts/                 # 辅助脚本目录
├── quick_setup.py       # 一键环境配置工具
├── check_env.py         # 环境检查脚本
├── check_encoding.py    # 编码检查工具
├── demo_features.py     # 功能演示脚本
└── demo_history.json    # 演示历史记录

tests/                   # 测试目录
├── test_sql_formatter.py # SQL格式化测试
├── test_history_manager.py # 历史管理测试
└── sample_sql.sql       # 测试用SQL样例
```
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
├── app.py                  # 主应用入口点
├── setup.py                # 安装脚本
├── pyproject.toml          # Python项目配置
├── MANIFEST.in             # 包含非Python文件的清单
├── start.bat               # Windows启动脚本
├── start.sh                # Linux/Mac启动脚本
├── run_with_encoding.bat   # Windows编码兼容启动脚本
├── sql_generator/          # 核心包
│   ├── core/               # 核心功能模块
│   │   ├── sql_generator.py # 基础SQL生成器
│   │   ├── advanced_sql.py  # 高级SQL功能
│   │   └── sql_formatter.py # SQL格式化工具
│   ├── ui/                 # 用户界面模块 
│   │   ├── main_app.py     # 主应用UI逻辑
│   │   └── streamlit_example.py # Streamlit示例组件
│   ├── utils/              # 工具模块
│   │   ├── file_utils.py   # 文件处理工具
│   │   ├── ui_utils.py     # UI辅助工具
│   │   ├── history_manager.py # 历史记录管理
│   │   └── security.py     # 安全验证模块
│   ├── templates/          # 模板模块
│   │   ├── sql_patterns.py # SQL模板系统
│   │   └── sql_example.xlsx # 样例配置文件
│   ├── config/             # 配置模块
│   │   └── constants.py    # 配置常量
│   └── assets/             # 静态资源
│       ├── create.png
│       ├── select.png
│       ├── merge.png
│       └── ...
├── scripts/                # 辅助脚本和工具
│   ├── quick_setup.py      # 一键环境配置脚本
│   ├── check_env.py        # 环境检查工具
│   ├── check_encoding.py   # 编码检查工具
│   ├── demo_features.py    # 功能演示脚本
│   └── demo_history.json   # 演示用的历史记录
├── tests/                  # 测试目录
│   ├── test_history_manager.py # 历史管理测试
│   ├── test_sql_formatter.py # SQL格式化测试
│   └── sample_sql.sql      # 测试用SQL样例
├── requirements.txt        # 项目依赖
└── README.md               # 项目说明
```

## 🛠️ 技术架构

### 核心组件
- **主应用** (`app.py`) - Streamlit应用主入口，导入并运行主UI组件
- **主UI** (`main_app.py`) - 处理页面路由和用户交互
- **配置管理** (`constants.py`) - 集中管理应用配置项和常量
- **工具模块** (`file_utils.py`, `ui_utils.py`) - 提供通用功能和辅助函数
- **SQL生成器** (`sql_generator.py`) - 核心业务逻辑，负责各种SQL语句生成
- **高级SQL** (`advanced_sql.py`) - 高级SQL功能，如索引、存储过程等
- **安全模块** (`security.py`) - 文件验证和SQL注入防护
- **历史记录** (`history_manager.py`) - 操作历史记录管理

### 设计模式
- **单一职责原则** - 每个模块负责特定功能
- **开放封闭原则** - 易于扩展新功能
- **依赖注入** - 模块间低耦合设计
- **装饰器模式** - 性能监控和缓存功能

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Streamlit 1.12.0

### 安装步骤

#### 🚀 一键安装（最简单）

1. **克隆项目**
```bash
git clone <repository-url>
cd streamlit-main
```

2. **一键配置**
```bash
python scripts/quick_setup.py
```
*此脚本会自动安装依赖、创建启动脚本*

3. **启动应用（Windows）**
```
start.bat
```
或
```
run_with_encoding.bat  # 解决中文编码问题
```

3. **启动应用（Linux/Mac）**
```bash
chmod +x start.sh
./start.sh
```

#### 🛠️ 手动安装

1. **克隆项目**
```bash
git clone <repository-url>
cd streamlit-main
```

2. **配置pip镜像源（可选，推荐）**
```bash
# 手动配置清华镜像源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/
pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **运行应用**
```bash
streamlit run app.py
```

#### 🔧 编码问题解决方案

如果遇到中文编码相关错误，可以：

1. **使用编码兼容脚本**
```
run_with_encoding.bat  # Windows系统
```

2. **运行编码检查工具**
```bash
python scripts/check_encoding.py
```

3. **手动设置环境变量**
```bash
# Windows
set PYTHONIOENCODING=utf-8
# Linux/Mac
export PYTHONIOENCODING=utf-8
```

6. **访问应用**
打开浏览器访问 `http://localhost:8501`

#### 📦 依赖说明

- **主要依赖**:
  - `streamlit==1.12.0`: Web应用框架
  - `pandas==2.2.3`: 数据处理和分析
  - `numpy==1.26.3`: 数学计算支持
  - `altair==4.2.0`: 数据可视化
  - `sqlparse==0.5.1`: SQL解析和格式化
  - `openpyxl==3.1.0`: Excel文件处理
  - `Pillow==10.4.0`: 图像处理
  - `python-magic` & `python-magic-bin`: 文件类型检测（提升安全性）

#### 🔧 镜像源配置

**推荐使用国内镜像源**以提升安装速度：

```bash
# 方法1：手动配置
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/
pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn

# 方法2：临时使用
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ -r requirements.txt
```

**其他镜像源选择：**
- 阿里云：`https://mirrors.aliyun.com/pypi/simple/`
- 豆瓣：`https://pypi.douban.com/simple/`
- 腾讯云：`https://mirrors.cloud.tencent.com/pypi/simple/`

## 📖 使用指南

### 1. 界面导航
应用主界面包含以下几个主要页面：
- **基本SQL生成**: 生成常用SQL语句
- **高级SQL功能**: 索引、存储过程、触发器等高级功能
- **模板中心**: 使用预定义SQL模板
- **历史记录**: 查看和管理之前生成的SQL语句
- **示例演示**: Streamlit组件示例展示

### 2. 文件上传
- 支持Excel (.xlsx, .xls)、CSV (.csv)、文本文件 (.txt)
- 最大文件大小：5MB (可在配置中调整)
- 自动进行文件类型和安全验证

### 3. 配置格式
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
请参考`templates/sql_example.xlsx`中的格式说明。

### 4. SQL生成流程
1. 在左侧导航栏选择操作类型
2. 上传配置文件或手动输入参数
3. 设置必要的参数和选项
4. 点击"生成SQL"按钮
5. 查看和编辑生成的SQL
6. 复制或下载SQL文件
7. 生成历史会自动保存

### 5. 历史记录管理
- 浏览之前生成的所有SQL操作
- 按操作类型和创建时间筛选
- 收藏常用SQL语句
- 搜索历史记录
- 导出为JSON或CSV格式
- 查看使用统计数据

## 🔒 安全特性

### 文件安全
- 文件类型白名单验证
- 文件大小限制
- MIME类型验证
- 上传文件安全检查

### SQL安全
- 表名和字段名验证
- 危险关键词过滤
- 参数化生成防注入
- 安全日志记录

## 🧪 测试与开发

项目包含测试套件以确保核心功能正常工作：

```bash
# 运行单个测试
python tests/test_history_manager.py

# 运行所有测试
pytest tests/
```

### 演示脚本

项目包含功能演示脚本，可以快速了解各模块功能：

```bash
# 演示高级SQL功能
python scripts/demo_features.py
```

### 开发建议

1. **编码问题**: 始终使用UTF-8编码处理文件
2. **依赖版本**: 注意Altair需要使用4.2.0版本与Streamlit 1.12.0兼容
3. **模块化**: 按照现有结构添加新功能，保持模块独立
4. **错误处理**: 添加适当的异常处理和用户友好的错误消息

## 🔧 常见问题排查

### 编码问题
如果遇到类似 `UnicodeEncodeError: 'charmap' codec can't encode characters` 的错误：
- 使用 `run_with_encoding.bat` 启动应用
- 运行 `python scripts/check_encoding.py` 检查编码设置
- 确保所有文件读写都指定了 `encoding='utf-8'`

### 依赖问题
如果遇到模块导入错误：
- 确认使用了兼容版本的库：`streamlit==1.12.0`, `altair==4.2.0`
- 完全按照 `requirements.txt` 安装依赖

### 运行问题
如果应用无法正常启动：
- 检查 Python 版本（推荐 3.8+）
- 检查 Streamlit 安装是否正确
- 尝试使用绝对路径启动：`streamlit run <完整路径>/app.py`

如果您遇到问题或有建议，请：
1. 运行编码或环境检查工具（`check_encoding.py`或`check_env.py`）
2. 检查控制台输出的错误信息
3. 查看项目文档
4. 提交详细的问题报告

---

⭐ 如果这个项目对您有帮助，请给我一个星标！
