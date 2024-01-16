; ModuleID = ""
target triple = "arm64-apple-macosx"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"

define i32 @"main"()
{
main.entry:
  %".2" = bitcast [23 x i8]* @".str0" to i8*
  %".3" = call i32 (i8*, ...) @"printf"(i8* %".2", i32 3, i32 2, i32 1)
  ret i32 0
}

declare i32 @"printf"(i8* %".1", ...)

@".str0" = internal constant [23 x i8] c"Hello, world! %d %d %d\00"