# CPP-LLVM 编译器

## 基本概述

在 LLVM 架构中，编译运行 C++程序涉及到两步：

- 使用 `clang` 编译 C++代码生成**LLVM IR(intermediate representation)**，也即 LLVM bitcode；
- 使用 `llc` 直接运行 LLVM IR 代码（其中包含了生成可执行文件的步骤）。

我们要实现的是第一步。

## 环境搭建

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

## 词法分析

### 预先准备

目前准备使用 flex + yacc 工具来实现词法分析、语法分析，使用以下的指令安装：`sudo apt install flex bison`。

在根目录下使用以下命令运行当前的词法分析（借助脚本 test.sh）：

```shell
chmod +x test.sh
./test.sh lexer helloworld
```

上述的 test.sh 脚本接受两个参数：

- **执行模式**：可以是 lexer（词法分析部分）、parser（语法分析部分）等
- **测试文件**：上述的 `test` 表示 `/example` 目录下的 `test.cpp` 文件

### 代码结构

**只需要关注两个目录**：`/src` 和 `/example`：

- `/example`（**实例代码**）：可以将自己要使用的示例代码加入该文件夹中，向上面的 `test.sh` 脚本传入第二个参数即可指定文件。
- `/src`（**源代码**）：**所有要修改的代码都位于这里**。
    - `main.c`：主程序入口，**暂时不需要修改**；
    - `lexer.l`：lex 程序，用以生成**词法分析器**代码；
    - `parser.y`：yacc 程序，用以生成**语法分析器**代码；
    - `token.h`：**额外的token**定义头文件（只有在无法区分token时添加）。

### 当前进度与任务

- **主要目标：修改 `lexer.l` 程序，必要时需要在 `parser.y` 中添加 token 的类型定义，使得由此生成的词法分析器能够正常满足需求。**
- 目前实现的内容：在`lexer.l`中已经添加了基本的token正则表达式匹配和对应的处理方式（**这里使用正则表达式匹配token**），在`parser.y`中定义了基本的token类型（**token类型需要定义在这里**）。
- 建议先阅读课件 29-34 页或教材 3.5 节。
- 当前任务：添加更多的token类型（在`parser.y`中）和对应的匹配（在`lexer.l`中），尽可能支持C++的所有关键字、数据类型等。关键字列表可参考：https://en.cppreference.com/w/cpp/keyword 。
