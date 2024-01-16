; ModuleID = ""
target triple = "arm64-apple-macosx"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"

define void @"printArray"(i32* %"arr", i32 %"i")
{
printArray.entry:
  %".4" = alloca i32*
  store i32* %"arr", i32** %".4"
  %".6" = alloca i32
  store i32 %"i", i32* %".6"
  %".8" = bitcast [6 x i8]* @".str0" to i8*
  %".9" = load i32, i32* %".6"
  %".10" = getelementptr i32*, i32** %".4", i32 0, i32 %".9" = load i32, i32* %".6"
  %".11" = load i32, i32* %".10"
  %".12" = call i32 (i8*, ...) @"printf"(i8* %".8", i32 %".11")
  ret void
}

declare i32 @"printf"(i8* %".1", ...)

@".str0" = internal constant [6 x i8] c"%d \0a \00"
define i32 @"main"()
{
main.entry:
  %"array" = alloca [10 x i32]
  %".2" = getelementptr [10 x i32], [10 x i32]* %"array", i32 0, i32 i32 0
  store i32 1, i32* %".2"
  %".4" = getelementptr [10 x i32], [10 x i32]* %"array", i32 0, i32 i32 1
  store i32 0, i32* %".4"
  %".6" = getelementptr [10 x i32], [10 x i32]* %"array", i32 0, i32 i32 2
  store i32 3, i32* %".6"
  %".8" = getelementptr [10 x i32], [10 x i32]* %"array", i32 0, i32 i32 3
  store i32 4, i32* %".8"
  %".10" = getelementptr [10 x i32], [10 x i32]* %"array", i32 0, i32 i32 5
  store i32 5, i32* %".10"
  %".12" = getelementptr [10 x i32], [10 x i32]* %"array", i32 0, i32 i32 6
  store i32 7, i32* %".12"
  %".14" = getelementptr [10 x i32], [10 x i32]* %"array", i32 0, i32 i32 8
  store i32 0, i32* %".14"
  %".16" = bitcast [46 x i8]* @".str1" to i8*
  %".17" = call i32 (i8*, ...) @"printf"(i8* %".16")
  %".18" = load [10 x i32], [10 x i32]* %"array"
  %".19" = bitcast [10 x i32] %".18" to i32*
  call void @"printArray"(i32* %".19", i32 0)
  %".21" = load [10 x i32], [10 x i32]* %"array"
  %".22" = bitcast [10 x i32] %".21" to i32*
  call void @"printArray"(i32* %".22", i32 1)
  %".24" = load [10 x i32], [10 x i32]* %"array"
  %".25" = bitcast [10 x i32] %".24" to i32*
  call void @"printArray"(i32* %".25", i32 2)
  %".27" = load [10 x i32], [10 x i32]* %"array"
  %".28" = bitcast [10 x i32] %".27" to i32*
  call void @"printArray"(i32* %".28", i32 3)
  %".30" = load [10 x i32], [10 x i32]* %"array"
  %".31" = bitcast [10 x i32] %".30" to i32*
  call void @"printArray"(i32* %".31", i32 5)
  %".33" = load [10 x i32], [10 x i32]* %"array"
  %".34" = bitcast [10 x i32] %".33" to i32*
  call void @"printArray"(i32* %".34", i32 6)
  %".36" = load [10 x i32], [10 x i32]* %"array"
  %".37" = bitcast [10 x i32] %".36" to i32*
  call void @"printArray"(i32* %".37", i32 8)
  ret i32 0
}

@".str1" = internal constant [46 x i8] c"I am going to print some elements of array a \00"