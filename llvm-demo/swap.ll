; ModuleID = "my_module"
target triple = "arm64-apple-macos"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

define i32 @"main"()
{
entry:
  %".2" = bitcast [4 x i8]* @"fmt_str" to i8*
  %"var_a" = alloca i32
  %"var_b" = alloca i32
  store i32 11451, i32* %"var_a"
  store i32 7890, i32* %"var_b"
  %"val_a" = load i32, i32* %"var_a"
  %"val_b" = load i32, i32* %"var_b"
  %".5" = call i32 (i8*, ...) @"printf"(i8* %".2", i32 %"val_a")
  %".6" = call i32 (i8*, ...) @"printf"(i8* %".2", i32 %"val_b")
  call void @"swap"(i32* %"var_a", i32* %"var_b")
  %"val_a.1" = load i32, i32* %"var_a"
  %"val_b.1" = load i32, i32* %"var_b"
  %".8" = call i32 (i8*, ...) @"printf"(i8* %".2", i32 %"val_a.1")
  %".9" = call i32 (i8*, ...) @"printf"(i8* %".2", i32 %"val_b.1")
  %"arr" = alloca [5 x i32]
  %"elem_ptr" = getelementptr [5 x i32], [5 x i32]* %"arr", i32 0, i32 0
  store i32 1, i32* %"elem_ptr"
  %"elem_ptr.1" = getelementptr [5 x i32], [5 x i32]* %"arr", i32 0, i32 1
  store i32 2, i32* %"elem_ptr.1"
  %"elem_ptr.2" = getelementptr [5 x i32], [5 x i32]* %"arr", i32 0, i32 2
  store i32 3, i32* %"elem_ptr.2"
  %"elem_ptr.3" = getelementptr [5 x i32], [5 x i32]* %"arr", i32 0, i32 3
  store i32 4, i32* %"elem_ptr.3"
  %"elem_ptr.4" = getelementptr [5 x i32], [5 x i32]* %"arr", i32 0, i32 4
  store i32 5, i32* %"elem_ptr.4"
  %"arr_ptr" = bitcast [5 x i32]* %"arr" to i32*
  call void @"printArray"(i32* %"arr_ptr", i32 5)
  ret i32 0
}

@"fmt_str" = internal constant [4 x i8] c"%d\0a\00"
define void @"swap"(i32* %".1", i32* %".2")
{
entry:
  %"a_val" = load i32, i32* %".1"
  %"b_val" = load i32, i32* %".2"
  %"temp" = alloca i32
  store i32 %"a_val", i32* %"temp"
  store i32 %"b_val", i32* %".1"
  %"temp_val" = load i32, i32* %"temp"
  store i32 %"temp_val", i32* %".2"
  ret void
}

define void @"printArray"(i32* %".1", i32 %".2")
{
entry:
  %"i" = alloca i32
  store i32 0, i32* %"i"
  br label %"loop_cond"
loop_cond:
  %"i_val" = load i32, i32* %"i"
  %"cond" = icmp slt i32 %"i_val", %".2"
  br i1 %"cond", label %"loop_body", label %"after_loop"
loop_body:
  %"element_ptr" = getelementptr i32, i32* %".1", i32 %"i_val"
  %"element" = load i32, i32* %"element_ptr"
  %".7" = bitcast [4 x i8]* @"fmt_str" to i8*
  %".8" = call i32 (i8*, ...) @"printf"(i8* %".7", i32 %"element")
  %"next_i_val" = add i32 %"i_val", 1
  store i32 %"next_i_val", i32* %"i"
  br label %"loop_cond"
after_loop:
  ret void
}
