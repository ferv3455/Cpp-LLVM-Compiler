; ModuleID = ""
target triple = ""
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

declare i32 @"scanf"(i8* %".1", ...)

define i32 @"main"()
{
.2:
  %"m" = alloca i32
  %".3" = bitcast [3 x i8]* @"140070818012416" to i8*
  %".4" = call i32 (i8*, ...) @"scanf"(i8* %".3", i32* %"m")
  %"i" = alloca i32
  store i32 0, i32* %"i"
  br label %".6"
.6:
  %".10" = icmp ne i8 1, 0
  br i1 %".10", label %".7", label %".8"
.7:
  %".12" = load i32, i32* %"i"
  %".13" = bitcast [4 x i8]* @"140070818019936" to i8*
  %".14" = call i32 (i8*, ...) @"printf"(i8* %".13", i32 %".12")
  %"j" = alloca i32
  store i32 0, i32* %"j"
  br label %".16"
.8:
  ret i32 0
.16:
  %".21" = load i32, i32* %"j"
  %".22" = load i32, i32* %"i"
  %".23" = icmp sle i32 %".21", %".22"
  br i1 %".23", label %".17", label %".19"
.17:
  %".25" = load i32, i32* %"j"
  %".26" = bitcast [7 x i8]* @"140070818031600" to i8*
  %".27" = call i32 (i8*, ...) @"printf"(i8* %".26", i32 %".25")
  %".31" = load i32, i32* %"j"
  %".32" = load i32, i32* %"i"
  %".33" = sdiv i32 %".32", 2
  %".34" = icmp sge i32 %".31", %".33"
  br i1 %".34", label %".28", label %".29"
.18:
  %".39" = load i32, i32* %"j"
  %".40" = add i32 %".39", 1
  store i32 %".40", i32* %"j"
  br label %".16"
.19:
  %".46" = load i32, i32* %"i"
  %".47" = load i32, i32* %"m"
  %".48" = icmp sge i32 %".46", %".47"
  br i1 %".48", label %".43", label %".44"
.28:
  br label %".19"
.29:
  br label %".30"
.30:
  br label %".18"
.43:
  br label %".8"
.44:
  br label %".45"
.45:
  %".52" = load i32, i32* %"i"
  %".53" = add i32 %".52", 1
  store i32 %".53", i32* %"i"
  br label %".6"
}

@"140070818012416" = internal constant [3 x i8] c"%d\00"
@"140070818019936" = internal constant [4 x i8] c"%d\0a\00"
@"140070818031600" = internal constant [7 x i8] c"   %d\0a\00"
