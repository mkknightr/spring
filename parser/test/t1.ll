; ModuleID = ""
target triple = "arm64-apple-macosx"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"

define i32 @"main"()
{
main.entry:
  %"a" = alloca i32
  store i32 10, i32* %"a"
  %"b" = alloca i32
  store i32 9, i32* %"b"
  %"c" = alloca i32
  %".4" = sub i32 0, 1
  store i32 %".4", i32* %"c"
  %".6" = load i32, i32* %"a"
  %".7" = load i32, i32* %"c"
  %".8" = sub i32 %".6", %".7"
  store i32 %".8", i32* %"a"
  ret i32 0
}
