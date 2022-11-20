# CPP-LLVM 编译器

## 基本概述

在 LLVM 架构中，编译运行 C++程序涉及到两步：

- 使用 `clang` 编译 C++代码生成**LLVM IR(intermediate representation)**，也即 LLVM bitcode；
- 使用 `llc` 直接运行 LLVM IR 代码（其中包含了生成可执行文件的步骤）。

我们要实现的是第一步。

## 环境搭建

> 已在Linux系统上完成了安装，以下是Linux上安装的完整步骤。未测试过Windows，尽可能使用Linux。

### On Unix-like Systems

> Adapted from https://clang.llvm.org/get_started.html .

If you would like to check out and build Clang, the current procedure is as follows:

1.  Get the required tools. (**Generally, `sudo apt install cmake` is enough.** Tested on WSL2 Ubuntu 20.08.) If there are errors in the following steps, refer to these requirements.
    - See [Getting Started with the LLVM System - Requirements](https://llvm.org/docs/GettingStarted.html#requirements) .
    - Note also that Python is needed for running the test suite. Get it at: [https://www.python.org/downloads/](https://www.python.org/downloads/)
    - Standard build process uses CMake. Get it at: [https://cmake.org/download/](https://cmake.org/download/)
2.  **Check out the LLVM project**:
    - Change directory to where you want the llvm directory placed.
    - **The command `git clone https://github.com/llvm/llvm-project.git` is very slow. It can be made faster by creating a shallow clone. Shallow clone saves storage and speeds up the checkout time. This is done by using the command:`git clone --depth=1 https://github.com/llvm/llvm-project.git`**
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
4.  **Add `llvm/build/bin` to your path**: add this new line to the end of file`~/.bashrc`: `export PATH="/path/to/llvm/build/bin:$PATH"`, and then restart shell: `source ~/.bashrc`.
5.  **Try it out**:
    - clang++ --version
    - clang++ --help
    - clang++ file.cpp -fsyntax-only (check for correctness)
    - clang++ file.cpp -S -emit-llvm -o - (print out unoptimized llvm code)
    - clang++ file.cpp -S -emit-llvm -o - -O3
    - clang++ file.cpp -S -O3 -o - (output native machine code)

### IDE 配置

可以使用Visual Studio Code，在扩展中搜索**LLVM插件**（LLVM | LLVM IR syntax hightlight | Ingvar Stepanyan），实现代码高亮和提示。

### 测试实验环境

创建文件 `helloworld.cpp`（可以在`/example`目录下找到）：

```cpp
#include <cstdio>  
  
int main()  
{  
    printf("Hello world!\n");  
    return 0;  
}
```

使用命令 `clang++ -emit-llvm -S helloworld.cpp -o helloworld.ll` 可以得到 LLVM IR 语言的代码文件 `helloworld.ll`。这一步也可使用shell脚本`./compile.sh helloworld.cpp`（可能需要`chmod +x ./compile.sh`）：

```llvm
; ModuleID = 'helloworld.cpp'
source_filename = "helloworld.cpp"
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

此时使用指令 `lli helloworld.ll` 可以运行 LLVM IR 代码，输出 Hello world!

尝试自己写 LLVM IR 代码，实现 hello world，得到`helloworld2.ll`：

```llvm
@.str = internal constant [14 x i8] c"Hello world!\0A\00"

declare i32 @printf(ptr, ...)

define i32 @main(i32 %argc, ptr %argv) nounwind {
entry:
    %tmp1 = getelementptr [14 x i8], ptr @.str, i32 0, i32 0
    %tmp2 = call i32 (ptr, ...) @printf( ptr %tmp1 ) nounwind
    ret i32 0
}
```

此时使用指令 `lli helloworld2.ll` 同样可以运行该 LLVM IR 代码，输出 Hello world!

**最终的实验任务就是读取这样的 `helloworld.cpp`，生成上述 `helloworld.ll`。**
