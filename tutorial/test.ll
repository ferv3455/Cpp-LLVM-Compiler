; ModuleID = "test"
target triple = ""
target datalayout = ""

@"msg" = internal constant [14 x i8] c"Hello world!\0a\00"
declare i32 @"printf"(i8* %".1", ...)

define i32 @"main"(i32 %".1", i8** %".2")
{
.4:
  br label %".5"
.5:
  %".9" = phi  i32 [0, %".4"], [%".14", %".6"]
  %".10" = icmp slt i32 %".9", %".1"
  br i1 %".10", label %".6", label %".7"
.6:
  %".12" = bitcast [14 x i8]* @"msg" to i8*
  %".13" = call i32 (i8*, ...) @"printf"(i8* %".12")
  %".14" = add i32 %".9", 1
  br label %".5"
.7:
  ret i32 0
}

