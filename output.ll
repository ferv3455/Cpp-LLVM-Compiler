; ModuleID = ""
target triple = ""
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

declare i32 @"scanf"(i8* %".1", ...)

declare i32 @"strlen"(i8* %".1")

declare i32 @"strcmp"(i8* %".1", i8* %".2")

declare i8* @"strcat"(i8* %".1", i8* %".2")

declare i8* @"strcpy"(i8* %".1", i8* %".2")

declare i32 @"strnlen"(i8* %".1", i32 %".2")

declare i32 @"strncmp"(i8* %".1", i8* %".2", i32 %".3")

declare i8* @"strncat"(i8* %".1", i8* %".2", i32 %".3")

declare i8* @"strncpy"(i8* %".1", i8* %".2", i32 %".3")

@"pattern" = global [256 x i8] undef
@"text" = global [1024 x i8] undef
@"pi" = global [256 x i32] undef
define void @"pi_cal"(i32 %".1")
{
.3:
  %"len_p" = alloca i32
  store i32 %".1", i32* %"len_p"
  %".5" = getelementptr [256 x i32], [256 x i32]* @"pi", i32 0, i32 1
  store i32 0, i32* %".5"
  %"k" = alloca i32
  store i32 0, i32* %"k"
  %"q" = alloca i32
  store i32 2, i32* %"q"
  br label %".9"
.9:
  %".13" = load i32, i32* %"q"
  %".14" = load i32, i32* %"len_p"
  %".15" = icmp sle i32 %".13", %".14"
  br i1 %".15", label %".10", label %".11"
.10:
  br label %".17"
.11:
  ret void
.17:
  %".21" = load i32, i32* %"k"
  %".22" = icmp sgt i32 %".21", 0
  %".23" = load i32, i32* %"k"
  %".24" = add i32 %".23", 1
  %".25" = load i32, i32* %"len_p"
  %".26" = icmp slt i32 %".24", %".25"
  %".27" = and i1 %".22", %".26"
  %".28" = load i32, i32* %"k"
  %".29" = add i32 %".28", 1
  %".30" = getelementptr [256 x i8], [256 x i8]* @"pattern", i32 0, i32 %".29"
  %".31" = load i8, i8* %".30"
  %".32" = load i32, i32* %"q"
  %".33" = getelementptr [256 x i8], [256 x i8]* @"pattern", i32 0, i32 %".32"
  %".34" = load i8, i8* %".33"
  %".35" = icmp ne i8 %".31", %".34"
  %".36" = and i1 %".27", %".35"
  br i1 %".36", label %".18", label %".19"
.18:
  %".38" = load i32, i32* %"k"
  %".39" = getelementptr [256 x i32], [256 x i32]* @"pi", i32 0, i32 %".38"
  %".40" = load i32, i32* %".39"
  store i32 %".40", i32* %"k"
  br label %".17"
.19:
  %".46" = load i32, i32* %"k"
  %".47" = add i32 %".46", 1
  %".48" = load i32, i32* %"len_p"
  %".49" = icmp slt i32 %".47", %".48"
  %".50" = load i32, i32* %"k"
  %".51" = add i32 %".50", 1
  %".52" = getelementptr [256 x i8], [256 x i8]* @"pattern", i32 0, i32 %".51"
  %".53" = load i8, i8* %".52"
  %".54" = load i32, i32* %"q"
  %".55" = getelementptr [256 x i8], [256 x i8]* @"pattern", i32 0, i32 %".54"
  %".56" = load i8, i8* %".55"
  %".57" = icmp eq i8 %".53", %".56"
  %".58" = and i1 %".49", %".57"
  br i1 %".58", label %".43", label %".44"
.43:
  %".60" = load i32, i32* %"k"
  %".61" = add i32 %".60", 1
  store i32 %".61", i32* %"k"
  br label %".45"
.44:
  br label %".45"
.45:
  %".65" = load i32, i32* %"k"
  %".66" = load i32, i32* %"q"
  %".67" = getelementptr [256 x i32], [256 x i32]* @"pi", i32 0, i32 %".66"
  store i32 %".65", i32* %".67"
  %".69" = load i32, i32* %"q"
  %".70" = add i32 %".69", 1
  store i32 %".70", i32* %"q"
  br label %".9"
}

define void @"knuth_morris_pratt"()
{
.2:
  %".3" = bitcast [256 x i8]* @"pattern" to i8*
  %".4" = call i32 @"strlen"(i8* %".3")
  %".5" = sub i32 %".4", 1
  %"len_p" = alloca i32
  store i32 %".5", i32* %"len_p"
  %".7" = bitcast [1024 x i8]* @"text" to i8*
  %".8" = call i32 @"strlen"(i8* %".7")
  %".9" = sub i32 %".8", 1
  %"len_t" = alloca i32
  store i32 %".9", i32* %"len_t"
  %".11" = load i32, i32* %"len_p"
  call void @"pi_cal"(i32 %".11")
  %"q" = alloca i32
  store i32 0, i32* %"q"
  %"i" = alloca i32
  store i32 1, i32* %"i"
  br label %".15"
.15:
  %".19" = load i32, i32* %"i"
  %".20" = load i32, i32* %"len_t"
  %".21" = icmp sle i32 %".19", %".20"
  br i1 %".21", label %".16", label %".17"
.16:
  br label %".23"
.17:
  ret void
.23:
  %".27" = load i32, i32* %"q"
  %".28" = icmp sgt i32 %".27", 0
  %".29" = load i32, i32* %"q"
  %".30" = add i32 %".29", 1
  %".31" = getelementptr [256 x i8], [256 x i8]* @"pattern", i32 0, i32 %".30"
  %".32" = load i8, i8* %".31"
  %".33" = load i32, i32* %"i"
  %".34" = getelementptr [1024 x i8], [1024 x i8]* @"text", i32 0, i32 %".33"
  %".35" = load i8, i8* %".34"
  %".36" = icmp ne i8 %".32", %".35"
  %".37" = and i1 %".28", %".36"
  br i1 %".37", label %".24", label %".25"
.24:
  %".39" = load i32, i32* %"q"
  %".40" = getelementptr [256 x i32], [256 x i32]* @"pi", i32 0, i32 %".39"
  %".41" = load i32, i32* %".40"
  store i32 %".41", i32* %"q"
  br label %".23"
.25:
  %".47" = load i32, i32* %"q"
  %".48" = add i32 %".47", 1
  %".49" = getelementptr [256 x i8], [256 x i8]* @"pattern", i32 0, i32 %".48"
  %".50" = load i8, i8* %".49"
  %".51" = load i32, i32* %"i"
  %".52" = getelementptr [1024 x i8], [1024 x i8]* @"text", i32 0, i32 %".51"
  %".53" = load i8, i8* %".52"
  %".54" = icmp eq i8 %".50", %".53"
  br i1 %".54", label %".44", label %".45"
.44:
  %".56" = load i32, i32* %"q"
  %".57" = add i32 %".56", 1
  store i32 %".57", i32* %"q"
  br label %".46"
.45:
  br label %".46"
.46:
  %".64" = load i32, i32* %"q"
  %".65" = load i32, i32* %"len_p"
  %".66" = icmp eq i32 %".64", %".65"
  br i1 %".66", label %".61", label %".62"
.61:
  %".68" = load i32, i32* %"i"
  %".69" = load i32, i32* %"len_p"
  %".70" = sub i32 %".68", %".69"
  %".71" = bitcast [14 x i8]* @"140234532208544" to i8*
  %".72" = call i32 (i8*, ...) @"printf"(i8* %".71", i32 %".70")
  %".73" = load i32, i32* %"q"
  %".74" = getelementptr [256 x i32], [256 x i32]* @"pi", i32 0, i32 %".73"
  %".75" = load i32, i32* %".74"
  store i32 %".75", i32* %"q"
  br label %".63"
.62:
  br label %".63"
.63:
  %".79" = load i32, i32* %"i"
  %".80" = add i32 %".79", 1
  store i32 %".80", i32* %"i"
  br label %".15"
}

@"140234532208544" = internal constant [14 x i8] c"Shift at %d.\0a\00"
define i32 @"main"()
{
.2:
  %".3" = getelementptr [1024 x i8], [1024 x i8]* @"text", i32 0, i32 0
  store i8 32, i8* %".3"
  %".5" = getelementptr [256 x i8], [256 x i8]* @"pattern", i32 0, i32 0
  store i8 32, i8* %".5"
  %".7" = getelementptr [1024 x i8], [1024 x i8]* @"text", i32 0, i32 1
  %".8" = bitcast [3 x i8]* @"140234532260880" to i8*
  %".9" = call i32 (i8*, ...) @"scanf"(i8* %".8", i8* %".7")
  %".10" = getelementptr [256 x i8], [256 x i8]* @"pattern", i32 0, i32 1
  %".11" = bitcast [3 x i8]* @"140234532282224" to i8*
  %".12" = call i32 (i8*, ...) @"scanf"(i8* %".11", i8* %".10")
  call void @"knuth_morris_pratt"()
  ret i32 0
}

@"140234532260880" = internal constant [3 x i8] c"%s\00"
@"140234532282224" = internal constant [3 x i8] c"%s\00"
