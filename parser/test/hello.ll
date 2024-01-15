; ModuleID = ""
target triple = "arm64-apple-macosx"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"

define i32 @"main"()
{
main.entry:
  %".2" = call i32 (i8*, ...) @"printf"(i8* getelementptr ([14 x i8], [14 x i8]* @"printf_str", i32 0, i32 0))
  ret i32 0
}

declare i32 @"printf"(i8* %".1", ...)

@"printf_str" = internal constant [14 x i8] c"Hello, World!\00"