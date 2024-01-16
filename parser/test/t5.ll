; ModuleID = ""
target triple = "arm64-apple-macosx"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"

define void @"swap"(i32* %"a", i32* %"b")
{
swap.entry:
  %".4" = alloca i32*
  store i32* %"a", i32** %".4"
  %".6" = alloca i32*
  store i32* %"b", i32** %".6"
  %"temp" = alloca i32
  %".8" = load i32*, i32** %".4"
  %".9" = load i32, i32* %".8"
  store i32 %".9", i32* %"temp"
  %".11" = load i32*, i32** %".6"
  %".12" = load i32, i32* %".11"
  %".13" = load i32*, i32** %".4"
  store i32 %".12", i32* %".13"
  %".15" = load i32, i32* %"temp"
  %".16" = load i32*, i32** %".6"
  store i32 %".15", i32* %".16"
  ret void
}

define i32 @"main"()
{
main.entry:
  %"a" = alloca i32
  store i32 1, i32* %"a"
  %"b" = alloca i32
  store i32 2, i32* %"b"
  %".4" = bitcast [17 x i8]* @".str0" to i8*
  %".5" = load i32, i32* %"a"
  %".6" = load i32, i32* %"b"
  %".7" = call i32 (i8*, ...) @"printf"(i8* %".4", i32 %".5", i32 %".6")
  call void @"swap"(i32* %"a", i32* %"b")
  %".9" = bitcast [17 x i8]* @".str1" to i8*
  %".10" = load i32, i32* %"a"
  %".11" = load i32, i32* %"b"
  %".12" = call i32 (i8*, ...) @"printf"(i8* %".9", i32 %".10", i32 %".11")
  ret i32 0
}

declare i32 @"printf"(i8* %".1", ...)

@".str0" = internal constant [17 x i8] c"a : %d, b : %d \0a\00"
@".str1" = internal constant [17 x i8] c"a : %d, b : %d \0a\00"