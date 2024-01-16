; ModuleID = ""
target triple = "arm64-apple-macosx"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"

define void @"printArray"([1000 x i32] %"arr", i32 %"i")
{
printArray.entry:
  %".4" = alloca [1000 x i32]
  store [1000 x i32] %"arr", [1000 x i32]* %".4"
  %".6" = alloca i32
  store i32 %"i", i32* %".6"
  %".8" = bitcast [5 x i8]* @".str0" to i8*
  %".9" = load i32, i32* %".6"
  %".10" = getelementptr [1000 x i32], [1000 x i32]* %".4", i32 0, i32 %".9"
  %".11" = load i32, i32* %".10"
  %".12" = call i32 (i8*, ...) @"printf"(i8* %".8", i32 %".11")
  ret void
}

declare i32 @"printf"(i8* %".1", ...)

@".str0" = internal constant [5 x i8] c"%d \0a\00"
define i32 @"main"()
{
main.entry:
  %"a.array" = alloca [1000 x i32]
  %".2" = getelementptr [1000 x i32], [1000 x i32]* %"a.array", i32 0, i32 0
  store i32 1, i32* %".2"
  %".4" = getelementptr [1000 x i32], [1000 x i32]* %"a.array", i32 0, i32 1
  store i32 0, i32* %".4"
  %".6" = getelementptr [1000 x i32], [1000 x i32]* %"a.array", i32 0, i32 2
  store i32 3, i32* %".6"
  %".8" = getelementptr [1000 x i32], [1000 x i32]* %"a.array", i32 0, i32 3
  store i32 4, i32* %".8"
  %".10" = getelementptr [1000 x i32], [1000 x i32]* %"a.array", i32 0, i32 5
  store i32 5, i32* %".10"
  %".12" = getelementptr [1000 x i32], [1000 x i32]* %"a.array", i32 0, i32 6
  store i32 7, i32* %".12"
  %".14" = getelementptr [1000 x i32], [1000 x i32]* %"a.array", i32 0, i32 8
  store i32 0, i32* %".14"
  %".16" = bitcast [47 x i8]* @".str1" to i8*
  %".17" = call i32 (i8*, ...) @"printf"(i8* %".16")
  %".18" = load [1000 x i32], [1000 x i32]* %"a.array"
  call void @"printArray"([1000 x i32] %".18", i32 0)
  %".20" = load [1000 x i32], [1000 x i32]* %"a.array"
  call void @"printArray"([1000 x i32] %".20", i32 1)
  %".22" = load [1000 x i32], [1000 x i32]* %"a.array"
  call void @"printArray"([1000 x i32] %".22", i32 2)
  %".24" = load [1000 x i32], [1000 x i32]* %"a.array"
  call void @"printArray"([1000 x i32] %".24", i32 3)
  %".26" = load [1000 x i32], [1000 x i32]* %"a.array"
  call void @"printArray"([1000 x i32] %".26", i32 5)
  %".28" = load [1000 x i32], [1000 x i32]* %"a.array"
  call void @"printArray"([1000 x i32] %".28", i32 6)
  %".30" = load [1000 x i32], [1000 x i32]* %"a.array"
  call void @"printArray"([1000 x i32] %".30", i32 8)
  ret i32 0
}

@".str1" = internal constant [47 x i8] c"I am going to print some elements of array a \0a\00"