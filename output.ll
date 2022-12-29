; ModuleID = ""
target triple = ""
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

declare i32 @"scanf"(i8* %".1", ...)

@"n" = global [10 x i32] undef
@"m" = global i32 6
@"t" = global i32 4
define i32 @"input"([10 x i32]* %".1")
{
.3:
  %"a" = alloca [10 x i32]*
  store [10 x i32]* %".1", [10 x i32]** %"a"
  %".5" = load [10 x i32]*, [10 x i32]** %"a"
  %".6" = getelementptr [10 x i32], [10 x i32]* %".5", i32 0, i32 0
  %".7" = bitcast [3 x i8]* @"139953650544496" to i8*
  %".8" = call i32 (i8*, ...) @"scanf"(i8* %".7", i32* %".6")
  ret i32 6
}

@"139953650544496" = internal constant [3 x i8] c"%d\00"
define i32 @"main"()
{
.2:
  %".3" = load i32, i32* @"t"
  %".4" = bitcast [4 x i8]* @"139953650565072" to i8*
  %".5" = call i32 (i8*, ...) @"printf"(i8* %".4", i32 %".3")
  %"i" = alloca i32
  store i32 0, i32* %"i"
  br label %".7"
.7:
  %".11" = load i32, i32* %"i"
  %".12" = load i32, i32* @"m"
  %".13" = icmp slt i32 %".11", %".12"
  br i1 %".13", label %".8", label %".9"
.8:
  %"j" = alloca i32
  store i32 0, i32* %"j"
  br label %".16"
.9:
  %"i.1" = alloca i32
  store i32 0, i32* %"i.1"
  br label %".41"
.16:
  %".20" = load i32, i32* %"j"
  %".21" = load i32, i32* %"i"
  %".22" = icmp sle i32 %".20", %".21"
  br i1 %".22", label %".17", label %".18"
.17:
  %".24" = load i32, i32* %"i"
  %".25" = getelementptr [10 x i32], [10 x i32]* @"n", i32 0, i32 %".24"
  %".26" = load i32, i32* %".25"
  %".27" = load i32, i32* %"j"
  %".28" = add i32 %".26", %".27"
  %".29" = load i32, i32* %"i"
  %".30" = getelementptr [10 x i32], [10 x i32]* @"n", i32 0, i32 %".29"
  store i32 %".28", i32* %".30"
  %".32" = load i32, i32* %"j"
  %".33" = add i32 %".32", 1
  store i32 %".33", i32* %"j"
  br label %".16"
.18:
  %".36" = load i32, i32* %"i"
  %".37" = add i32 %".36", 1
  store i32 %".37", i32* %"i"
  br label %".7"
.41:
  %".45" = load i32, i32* %"i.1"
  %".46" = load i32, i32* @"m"
  %".47" = icmp slt i32 %".45", %".46"
  br i1 %".47", label %".42", label %".43"
.42:
  %".49" = load i32, i32* %"i.1"
  %".50" = getelementptr [10 x i32], [10 x i32]* @"n", i32 0, i32 %".49"
  %".51" = load i32, i32* %".50"
  %".52" = bitcast [17 x i8]* @"139953650606032" to i8*
  %".53" = call i32 (i8*, ...) @"printf"(i8* %".52", i32 %".51")
  %".54" = load i32, i32* %"i.1"
  %".55" = add i32 %".54", 1
  store i32 %".55", i32* %"i.1"
  br label %".41"
.43:
  ret i32 0
}

@"139953650565072" = internal constant [4 x i8] c"%d\0a\00"
@"139953650606032" = internal constant [17 x i8] c"Hello world %d!\0a\00"
