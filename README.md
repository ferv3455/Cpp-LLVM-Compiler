# CPP-LLVM 编译器

## 基本概述

在 LLVM 架构中，编译运行 C++程序涉及到两步：

- 使用 `clang` 编译 C++代码生成**LLVM IR(intermediate representation)**，也即 LLVM bitcode；
- 使用 `llc` 直接运行 LLVM IR 代码（其中包含了生成可执行文件的步骤）。

我们要实现的是第一步。

## 词法分析

### 原始方法（废弃）

> 不再使用这里的 flex + yacc 方式完成词法分析。

#### 预先准备

使用 flex + yacc 工具来实现词法分析、语法分析，使用以下的指令安装：`sudo apt install flex bison`。

在根目录下使用以下命令运行当前的词法分析（借助脚本 test.sh）：

```shell
chmod +x test.sh
./test.sh lexer helloworld
```

上述的 test.sh 脚本接受两个参数：

- **执行模式**：可以是 lexer（词法分析部分）、parser（语法分析部分）等
- **测试文件**：上述的 `test` 表示 `/example` 目录下的 `test.cpp` 文件

#### 代码结构

**只需要关注两个目录**：`/src` 和 `/example`：

- `/example`（**实例代码**）：可以将自己要使用的示例代码加入该文件夹中，向上面的 `test.sh` 脚本传入第二个参数即可指定文件。
- `/src`（**源代码**）：**所有要修改的代码都位于这里**。
    - `main.c`：主程序入口，**暂时不需要修改**；
    - `lexer.l`：lex 程序，用以生成**词法分析器**代码；
    - `parser.y`：yacc 程序，用以生成**语法分析器**代码；
    - `token.h`：**额外的 token **定义头文件（只有在无法区分 token 时添加）。

### 当前方法

#### 代码结构（废弃）

> 代码结构已更新，见语法分析部分。

**只需要关注两个目录**：`/python` 和 `/example`：

- `example/`（实例代码）：可将要使用的示例代码加入该文件夹中；
- `python/`（源代码）：
    - `main.py`：主程序入口，暂时不需要修改；
    - `lexrules.py`：**全部的词法分析转换规则都在这里定义，理论上只需要修改这一文件**；
    - `lexer/`：词法分析器模块的源代码。

#### 运行方式

在根目录下运行 `python ./python/main.py ./example/helloworld.cpp -l` 即可。`-l` 标记表示词法分析（lexical analysis）。

#### 当前进度与任务

- **主要目标：修改 `lexrules.py`，在 rules 中添加更多的 token，使得由此生成的词法分析器能够正常满足需求。**
- 目前已经添加了基本的符号、变量符、字面常量等，剩下的部分主要为关键字（keywords）。

#### 语法规则

- `RULES` 列表中的表项均为元组，元组内容为 `(token_name, NFA, [ignore])`，其中最后一项 `ignore` 可选：
    - `token_name` 为字符串，表示 **token 类型名**；
    - `NFA` 为**匹配格式的自动机**，创建方式见下；
    - `ignore` 可选，默认为 `False`。如果为 `True`，则词法分析器**不会在 token 流中输出该项**。
- `RULES` 中的匹配规则**存在先后顺序**，长度相同时优先匹配靠前的；
- 自动机的创建方式：
    - `r('abc')` 创建用于**匹配文本**"abc"的 NFA；
    - `n('abc')` 创建的 NFA **匹配字符集的补集**：如果输入是"a"或"b"或"c"则**拒绝**，否则**接受**。可用 `n()` 表示正则表达式中的 `.`；
    - 以上是所有的原子自动机，其他的自动机可由此组合而成。
    - **或**（or）：加法，如 `r('a') + r('b')` 匹配"a"或"b"；
    - **连接**（concat）：乘法，如 `r('a') * r('b')` 匹配"ab"；
    - **星闭包**（star）：`r('a').star()` 匹配多个"a"（注意：使用 `n().star()` 时，需要加一个结尾，如 `r().star() * r('b')`，否则会全文匹配）；
    - **加号闭包**（plus）：`r('a').plus()` 匹配至少一个"a"；
    - **可选**（optional）：`r('a').optional()` 匹配一个或零个"a"；
    - **多个或**：可用 `r.alt` 函数。它接受一个可迭代对象作为参数，或是将多个自动机作为参数：
        - `r.alt(r(x) for x in string.digits)` 匹配所有的一位数字（参数为生成器）；
        - `r.alt(r('&&'), r('||'))` 匹配逻辑运算符（参数列表为单个的自动机）。
    - **多个连接**：可用 `r.concat` 函数，参数同上。
- 自动机的重复使用：如果先创建了一个自动机，将它保存在一个变量中（如：`DIGIT = r.alt(r(x) for x in string.digits)`），后续需要多次使用该自动机时，必须将该自动机深层复制（deepcopy），避免状态的重复利用：`c(DIGIT)`。
- 如果需要调试自己写的 NFA 是否能够正确匹配，可以在 `/python/debug.py` 代码中指定输入串 `text`，定义自动机，调用自动机的 `.simulate(text)` 方法得到（从头）匹配的长度，输出结果。

## 语法分析

### 代码结构

- `drafts/`（草稿）：尝试过的其他实现方法；
- `examples/`（实例代码）：可将要使用的示例代码加入该文件夹中；
- **`src/`（源代码）**：
    - `mycompiler/`：编译器框架的源代码，包含词法分析、语法分析；
    - **`rules/`：词法分析、语法分析规则。理论上只需要修改其中的规则；**
    - `main.py`：主程序入口，暂时不需要修改；
    - `debug.py`：用于调试。
- `tmp/`（临时文件）：用于缓存生成的词法分析器和语法分析器；
- `tutorial/`：配置 LLVM 环境所用的示例代码，暂时用不到。

### 运行方式

在根目录下运行 `python ./python/main.py ./example/test.cpp -p -u` 即可。**`-p` 标记表示解析（parsing），`-u` 标记表示更新所有的规则**，不加该标记会载入缓存的规则，而不是新修改的规则。

**请在根目录下运行，否则会找不到缓存文件的路径。**

### 当前进度与任务

- **文法部分：**
    - **修改 `src/rules/grammar.py`，完善文法，使得由此生成的解析器能够正常满足需求。**
    - 目前可以**支持 LR(1)文法**（参考课件），现在 `grammar.py` 中的文法为课件 Chapter 4' P44 的文法。
    - 设计文法需要考虑到**运算符优先级**、**文法本身是否是 LR(1)** 等问题。
- 框架部分：
    - 目前已实现 LR(1)分析，会进行进一步测试。

### 文法规则

可参考已提供的 `grammar.py`。`GRAMMAR` 为字典，其中包含以下的记录：

- `"non-terminals"`：所有的非终结符，可任意命名；
- `"terminals"`：所有的终结符，**需要与 lexrules 中 token 的名称一致**。如果需要细分 lexrules 中的一类 token，则可以使用 `:: ` 符号，在符号右侧写**具体的符号内容**。如加号：`arithmetic-op::+`；
- `"start"`：文法的推导起点（S）；
- `"derivations"`：所有产生式的列表。每条产生式用二元元组表示，分别用一个字符串表示左边和右边。右边的各符号之间用空格隔开。

## 代码生成

### 环境搭建

- **安装 python 的 `llvmlite` 库**：`pip install llvmlite`。可以使用虚拟环境 virtualenv。
- **正确配置 LLVM 环境**（见文末附录）。
- 测试：进入 `tutorial/` 目录，使用 `python codegen.py` 运行脚本，生成 LLVM IR 代码 `test.ll`。使用指令 `lli test.ll` 即可运行程序。**该程序是读取命令行参数的个数 `argc`，随后输出 `argc` 行 Hello world!**

### 源代码编译步骤

- 在**根目录下**运行 `python ./src/main.py ./examples/test.cpp`（**首次运行**需要添加 `-u` 标记，更新暂存的文法），即可得到编译结果 `output.ll`。
- 使用 `lli output.ll` 即可运行程序。

### 当前进展

当前支持的功能如下：

- include：cstdio 加载 printf、scanf，cstring 加载 strlen
- 变量类型：char、bool、int、void、一维数组
- 基本的函数定义，return 返回
- if 语句
- while、for、do while，暂时未实现 break、continue
- 简单变量定义（如 `int b, c = 8;`）
- 运算符：各种赋值运算、逻辑与或非、按位与或非、带符号整数的大小比较、左移右移、带符号整数的加减乘除模、自增自减、正负号、变量取地址、函数调用、取数组元素
- 字面量：整数、字符串、字符、true、false

### 后续任务

- 目前已经可以编译通过 sort.cpp、palindrome.cpp、kmp_pair.cpp 三个测试用例，这些用例已根据已实现的功能略微修改。
- 看看还需要实现哪些重要功能，如 cstdlib 库、break 等。

## 附录：LLVM 环境搭建

> Adapted from https://clang.llvm.org/get_started.html .

### On Unix-like Systems

If you would like to check out and build Clang, the current procedure is as follows:

1.  Get the required tools. (**Generally, `sudo apt install cmake` is enough.** Tested on WSL2 Ubuntu 20.08.) If there are errors in the following steps, refer to these requirements.
    - See [Getting Started with the LLVM System - Requirements](https://llvm.org/docs/GettingStarted.html#requirements) .
    - Note also that Python is needed for running the test suite. Get it at: [https://www.python.org/downloads/](https://www.python.org/downloads/)
    - Standard build process uses CMake. Get it at: [https://cmake.org/download/](https://cmake.org/download/)
2.  **Check out the LLVM project**:
    - Change directory to where you want the llvm directory placed.
    - `git clone https://github.com/llvm/llvm-project.git`
    - **The above command is very slow. It can be made faster by creating a shallow clone. Shallow clone saves storage and speeds up the checkout time. This is done by using the command:**
        - **`git clone --depth=1 https://github.com/llvm/llvm-project.git`** (using this only the latest version of llvm can be built)
        - For normal users looking to just compile, this command works fine. But if someone later becomes a contributor, since they can't push code from a shallow clone, it needs to be converted into a full clone:
            - cd llvm-project
            - git fetch --unshallow
3.  **Build LLVM and Clang**:
    - **`cd llvm-project`**
    - **`mkdir build`** (in-tree build is not supported)
    - **`cd build`**
    - This builds both LLVM and Clang in release mode. Alternatively, if you need a debug build, switch Release to Debug. See [frequently used cmake variables](https://llvm.org/docs/CMake.html#frequently-used-cmake-variables) for more options.
    - **`cmake -DLLVM_ENABLE_PROJECTS=clang -DCMAKE_BUILD_TYPE=Release -G "Unix Makefiles" ../llvm`**
    - **`make -j N`** (N is the number of parallel jobs, e.g. CPU number) (***this step can be REALLY SLOW, slower than you can imagine***)
    - CMake allows you to generate project files for several IDEs: Xcode, Eclipse CDT4, CodeBlocks, Qt-Creator (use the CodeBlocks generator), KDevelop3. For more details see [Building LLVM with CMake](https://llvm.org/docs/CMake.html) page.
4.  **Add `llvm/build/bin` to your path: add this new line to the end of file`~/.bashrc`: `export PATH="/path/to/llvm/build/bin:$PATH"`, and then restart shell: `source ~/.bashrc`.**
5.  **Try it out**:
    - clang++ --version
    - clang++ --help
    - clang++ file.cpp -fsyntax-only (check for correctness)
    - clang++ file.cpp -S -emit-llvm -o - (print out unoptimized llvm code)
    - clang++ file.cpp -S -emit-llvm -o - -O3
    - clang++ file.cpp -S -O3 -o - (output native machine code)

### 测试实验环境

创建文件 `test.cpp`：

```cpp
#include <cstdio>  
  
int main()  
{  
    printf("Hello world!\n");  
    return 0;  
}
```

使用命令 `clang++ -emit-llvm -S test.cpp -o test.ll` 可以得到 LLVM IR 语言的代码文件 `test.ll`（注：**在项目的 `/example` 目录中包含了 `compile.sh` 脚本，执行 `./compile.sh helloworld.cpp` 即可编译得到 `.ll` 文件。可能需要 `chmod +x ./compile.sh` 得到权限**）：

```llvmir
; ModuleID = 'test.cpp'  
source_filename = "test.cpp"  
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"  
target triple = "x86_64-unknown-linux-gnu"  
  
@.str = private unnamed_addr constant [14 x i8] c"Hello world!\0A\00", align 1  
  
; Function Attrs: mustprogress noinline norecurse optnone uwtable  
define dso_local noundef i32 @main() #0 {  
  %1 = alloca i32, align 4  
  store i32 0, ptr %1, align 4  
  %2 = call i32 (ptr, ...) @printf(ptr noundef @.str)  
  ret i32 0  
}  
  
declare i32 @printf(ptr noundef, ...) #1  
  
attributes #0 = { mustprogress noinline norecurse optnone uwtable "frame-pointer"="all" "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }  
attributes #1 = { "frame-pointer"="all" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }  
  
!llvm.module.flags = !{!0, !1, !2, !3, !4}  
!llvm.ident = !{!5}  
  
!0 = !{i32 1, !"wchar_size", i32 4}  
!1 = !{i32 8, !"PIC Level", i32 2}  
!2 = !{i32 7, !"PIE Level", i32 2}  
!3 = !{i32 7, !"uwtable", i32 2}  
!4 = !{i32 7, !"frame-pointer", i32 2}  
!5 = !{!"clang version 16.0.0 (https://github.com/llvm/llvm-project.git 7c5f06a7dc1319ad012e4f7266de5d5780169de6)"}
```

此时使用指令 `lli test.ll` 可以运行 LLVM IR 代码，输出 Hello world!

修改 `test.ll`，尝试自己写 LLVM IR 代码，实现 hello world：

```llvmir
@.str = internal constant [14 x i8] c"Hello world!\0A\00"

declare i32 @printf(ptr, ...)

define i32 @main(i32 %argc, ptr %argv) nounwind {
entry:
    %tmp1 = getelementptr [14 x i8], ptr @.str, i32 0, i32 0
    %tmp2 = call i32 (ptr, ...) @printf( ptr %tmp1 ) nounwind
    ret i32 0
}
```

此时使用指令 `lli test.ll` 同样可以运行该 LLVM IR 代码，输出 Hello world!

**最终的实验任务就是读取 `test.cpp`，生成上述 `test.ll`。**
