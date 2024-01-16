; ModuleID = "/Users/kni/projects/spring/llvm-demo/fadd.py"
target triple = "arm64-apple-macos"
target datalayout = ""

define double @"main"(double %".1", double %".2")
{
entry:
  %"res" = fadd double %".1", %".2"
  ret double %"res"
}
