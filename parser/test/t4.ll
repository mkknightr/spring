; ModuleID = ""
target triple = "arm64-apple-macosx"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"

define i32 @"main"()
{
main.entry:
  %"a" = alloca i32
  store i32 1, i32* %"a"
  %"b" = alloca i32
  store i32 2, i32* %"b"
  %"c" = alloca i32
  store i32 3, i32* %"c"
  %"d" = alloca i32
  %".5" = load i32, i32* %"a"
  %".6" = load i32, i32* %"b"
  %".7" = add i32 %".5", %".6"
  store i32 %".7", i32* %"d"
  %".9" = bitcast [15 x i8]* @".str0" to i8*
  %".10" = icmp sgt i32 1, 2
  %".11" = call i32 (i8*, ...) @"printf"(i8* %".9", i1 %".10")
  %".12" = bitcast [15 x i8]* @".str1" to i8*
  %".13" = icmp slt i32 1, 2
  %".14" = call i32 (i8*, ...) @"printf"(i8* %".12", i1 %".13")
  %".15" = bitcast [15 x i8]* @".str2" to i8*
  %".16" = icmp sle i32 1, 2
  %".17" = call i32 (i8*, ...) @"printf"(i8* %".15", i1 %".16")
  %".18" = bitcast [15 x i8]* @".str3" to i8*
  %".19" = icmp sge i32 1, 2
  %".20" = call i32 (i8*, ...) @"printf"(i8* %".18", i1 %".19")
  %".21" = bitcast [15 x i8]* @".str4" to i8*
  %".22" = icmp eq i32 1, 2
  %".23" = call i32 (i8*, ...) @"printf"(i8* %".21", i1 %".22")
  %".24" = bitcast [15 x i8]* @".str5" to i8*
  %".25" = icmp ne i32 1, 2
  %".26" = call i32 (i8*, ...) @"printf"(i8* %".24", i1 %".25")
  ret i32 0
}

declare i32 @"printf"(i8* %".1", ...)

@".str0" = internal constant [15 x i8] c"1 > 2   :  %d\0a\00"
@".str1" = internal constant [15 x i8] c"1 < 2   :  %d\0a\00"
@".str2" = internal constant [15 x i8] c"1 <= 2  :  %d\0a\00"
@".str3" = internal constant [15 x i8] c"1 >= 2  :  %d\0a\00"
@".str4" = internal constant [15 x i8] c"1 == 2  :  %d\0a\00"
@".str5" = internal constant [15 x i8] c"1 != 2  :  %d\0a\00"