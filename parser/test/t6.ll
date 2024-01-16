; ModuleID = ""
target triple = "arm64-apple-macosx"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"

define i32 @"main"()
{
main.entry:
  %"array" = alloca [10 x i32]
  %".2" = getelementptr inbounds [10 x i32], [10 x i32]* %"array", i32 0, i32 0
  store i32 1, i32* %".2"
  %".4" = getelementptr inbounds [10 x i32], [10 x i32]* %"array", i32 0, i32 1
  store i32 0, i32* %".4"
  %".6" = bitcast [23 x i8]* @".str0" to i8*
  %".7" = getelementptr inbounds [10 x i32], [10 x i32]* %"array", i32 0, i32 0
  %".8" = load i32, i32* %".7"
  %".9" = getelementptr inbounds [10 x i32], [10 x i32]* %"array", i32 0, i32 1
  %".10" = load i32, i32* %".9"
  %".11" = call i32 (i8*, ...) @"printf"(i8* %".6", i32 %".8", i32 %".10")
  ret i32 0
}

declare i32 @"printf"(i8* %".1", ...)

@".str0" = internal constant [23 x i8] c"a[0] : %d, a[1] : %d \0a\00"