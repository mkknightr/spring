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
  %".9" = bitcast [18 x i8]* @".str0" to i8*
  %".10" = load i32, i32* %"d"
  %".11" = call i32 (i8*, ...) @"printf"(i8* %".9", i32 %".10")
  %".12" = bitcast [22 x i8]* @".str1" to i8*
  %".13" = load i32, i32* %"a"
  %".14" = load i32, i32* %"b"
  %".15" = sub i32 %".13", %".14"
  %".16" = call i32 (i8*, ...) @"printf"(i8* %".12", i32 %".15")
  ret i32 0
}

declare i32 @"printf"(i8* %".1", ...)

@".str0" = internal constant [18 x i8] c"Value of d is %d\0a\00"
@".str1" = internal constant [22 x i8] c"Value of a - b is %d\0a\00"