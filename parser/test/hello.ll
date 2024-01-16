; ModuleID = ""
target triple = "arm64-apple-macosx"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"

define i32 @"test"(i32 %"a", i32 %"b")
{
test.entry:
  %".4" = alloca i32
  store i32 %"a", i32* %".4"
  %".6" = alloca i32
  store i32 %"b", i32* %".6"
  %".8" = call i32 (i8*, ...) @"printf"(i8* getelementptr ([5 x i8], [5 x i8]* @".str0", i32 0, i32 0))
  ret i32 1
}

declare i32 @"printf"(i8* %".1", ...)

@".str0" = internal constant [5 x i8] c"test\00"
define i32 @"main"()
{
main.entry:
  %"item" = alloca i32
  %".2" = call i32 (i8*, ...) @"printf"(i8* getelementptr ([14 x i8], [14 x i8]* @".str1", i32 0, i32 0))
  %"itemm" = alloca i8
  ret i32 0
}

@".str1" = internal constant [14 x i8] c"Hello, World!\00"