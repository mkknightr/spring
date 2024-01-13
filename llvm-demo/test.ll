; ModuleID = ""
target triple = "arm64-apple-darwin"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

define void @"print_hello"()
{
entry:
  %".2" = call i32 (i8*, ...) @"printf"(i8* getelementptr ([14 x i8], [14 x i8]* @"fmt_str", i32 0, i32 0))
  ret void
}

@"fmt_str" = internal constant [14 x i8] c"Hello, World!\0a"
define i32 @"main"()
{
entry:
  call void @"print_hello"()
  ret i32 0
}
