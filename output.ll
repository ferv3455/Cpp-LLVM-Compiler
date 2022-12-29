; ModuleID = ""
target triple = ""
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

declare i32 @"scanf"(i8* %".1", ...)

declare i32 @"sscanf"(i8* %".1", i8* %".2", ...)

declare i32 @"sprintf"(i8* %".1", i8* %".2", ...)

@"input_number" = global [100 x i32] undef
@"count" = global i32 0
define i32 @"main"()
{
.2:
  %"temp_number" = alloca i32
  store i32 0, i32* %"temp_number"
  %".4" = bitcast [3 x i8]* @"140711695054160" to i8*
  %".5" = call i32 (i8*, ...) @"scanf"(i8* %".4", i32* @"count")
  %"i" = alloca i32
  store i32 0, i32* %"i"
  br label %".7"
.7:
  %".12" = load i32, i32* %"i"
  %".13" = load i32, i32* @"count"
  %".14" = icmp slt i32 %".12", %".13"
  br i1 %".14", label %".8", label %".10"
.8:
  %".16" = load i32, i32* %"i"
  %".17" = getelementptr [100 x i32], [100 x i32]* @"input_number", i32 0, i32 %".16"
  %".18" = bitcast [3 x i8]* @"140711695072800" to i8*
  %".19" = call i32 (i8*, ...) @"scanf"(i8* %".18", i32* %".17")
  br label %".9"
.9:
  %".21" = load i32, i32* %"i"
  %".22" = add i32 %".21", 1
  store i32 %".22", i32* %"i"
  br label %".7"
.10:
  %"i.1" = alloca i32
  store i32 0, i32* %"i.1"
  br label %".26"
.26:
  %".31" = load i32, i32* %"i.1"
  %".32" = load i32, i32* @"count"
  %".33" = icmp slt i32 %".31", %".32"
  br i1 %".33", label %".27", label %".29"
.27:
  %"j" = alloca i32
  store i32 0, i32* %"j"
  br label %".36"
.28:
  %".84" = load i32, i32* %"i.1"
  %".85" = add i32 %".84", 1
  store i32 %".85", i32* %"i.1"
  br label %".26"
.29:
  %"i.2" = alloca i32
  store i32 0, i32* %"i.2"
  br label %".89"
.36:
  %".41" = load i32, i32* %"j"
  %".42" = load i32, i32* @"count"
  %".43" = load i32, i32* %"i.1"
  %".44" = sub i32 %".42", %".43"
  %".45" = sub i32 %".44", 1
  %".46" = icmp slt i32 %".41", %".45"
  br i1 %".46", label %".37", label %".39"
.37:
  %".51" = load i32, i32* %"j"
  %".52" = getelementptr [100 x i32], [100 x i32]* @"input_number", i32 0, i32 %".51"
  %".53" = load i32, i32* %".52"
  %".54" = load i32, i32* %"j"
  %".55" = add i32 %".54", 1
  %".56" = getelementptr [100 x i32], [100 x i32]* @"input_number", i32 0, i32 %".55"
  %".57" = load i32, i32* %".56"
  %".58" = icmp sgt i32 %".53", %".57"
  br i1 %".58", label %".48", label %".49"
.38:
  %".79" = load i32, i32* %"j"
  %".80" = add i32 %".79", 1
  store i32 %".80", i32* %"j"
  br label %".36"
.39:
  br label %".28"
.48:
  %".60" = load i32, i32* %"j"
  %".61" = getelementptr [100 x i32], [100 x i32]* @"input_number", i32 0, i32 %".60"
  %".62" = load i32, i32* %".61"
  %"temp" = alloca i32
  store i32 %".62", i32* %"temp"
  %".64" = load i32, i32* %"j"
  %".65" = add i32 %".64", 1
  %".66" = getelementptr [100 x i32], [100 x i32]* @"input_number", i32 0, i32 %".65"
  %".67" = load i32, i32* %".66"
  %".68" = load i32, i32* %"j"
  %".69" = getelementptr [100 x i32], [100 x i32]* @"input_number", i32 0, i32 %".68"
  store i32 %".67", i32* %".69"
  %".71" = load i32, i32* %"temp"
  %".72" = load i32, i32* %"j"
  %".73" = add i32 %".72", 1
  %".74" = getelementptr [100 x i32], [100 x i32]* @"input_number", i32 0, i32 %".73"
  store i32 %".71", i32* %".74"
  br label %".50"
.49:
  br label %".50"
.50:
  br label %".38"
.89:
  %".94" = load i32, i32* %"i.2"
  %".95" = load i32, i32* @"count"
  %".96" = icmp slt i32 %".94", %".95"
  br i1 %".96", label %".90", label %".92"
.90:
  %".98" = load i32, i32* %"i.2"
  %".99" = getelementptr [100 x i32], [100 x i32]* @"input_number", i32 0, i32 %".98"
  %".100" = load i32, i32* %".99"
  %".101" = bitcast [4 x i8]* @"140711695153808" to i8*
  %".102" = call i32 (i8*, ...) @"printf"(i8* %".101", i32 %".100")
  br label %".91"
.91:
  %".104" = load i32, i32* %"i.2"
  %".105" = add i32 %".104", 1
  store i32 %".105", i32* %"i.2"
  br label %".89"
.92:
  %".108" = bitcast [2 x i8]* @"140711695179008" to i8*
  %".109" = call i32 (i8*, ...) @"printf"(i8* %".108")
  ret i32 0
}

@"140711695054160" = internal constant [3 x i8] c"%d\00"
@"140711695072800" = internal constant [3 x i8] c"%d\00"
@"140711695153808" = internal constant [4 x i8] c"%d \00"
@"140711695179008" = internal constant [2 x i8] c"\0a\00"
