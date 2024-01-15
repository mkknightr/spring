import json
from antlr4 import *
from CLexer import CLexer
from CParser import CParser
from CParserVisitor import CParserVisitor
from antlr4.tree.Trees import Trees 
from semantic import semanticVisitor


def format_tree(node, indent=""):
    result = ""
    if node.getChildCount() == 0:
        return f"{indent}{Trees.getNodeText(node, None)}\n"
    else:
        result += f"{indent}{Trees.getNodeText(node, None)}\n"
        for i in range(node.getChildCount()):
            result += format_tree(node.getChild(i), indent + "  ")
        return result



class JsonExportVisitor(CParserVisitor):
    def visit(self, ctx):
        if isinstance(ctx, TerminalNode):
            return {"type": "Terminal", "text": ctx.getText()}

        result = {"type": type(ctx).__name__, "children": []}
        if ctx.children:
            for child in ctx.children:
                child_result = self.visit(child)
                # 只有当子结果不是None时才添加到children列表中
                if child_result is not None:
                    result["children"].append(child_result)
        return result

    def visitChildren(self, ctx):
        children = []
        for child in ctx.children:
            child_result = self.visit(child)
            children.append(child_result)
        return children

    def defaultResult(self):
        return []

    def aggregateResult(self, aggregate, next_result):
        # 聚合结果
        if next_result is not None:
            return aggregate + [next_result]
        return aggregate

input_stream = FileStream("/Users/kni/projects/spring/parser/test/hello.c")
lexer = CLexer(input_stream)
stream = CommonTokenStream(lexer)

token_stream_text = stream.getText()
print("Token Stream Text:", token_stream_text)
# print tokens in the form of table 
print("{:<10} {:<20} {:<15} {:<15}".format("Token Type", "Text", "Line", "Column")) 
print("="*60) 

for token in stream.tokens:
    token_type = token.type
    print("{:<10} {:<20} {:<15} {:<15}".format(
        CLexer.symbolicNames[token.type], 
        token.text, 
        token.line, 
        token.column
        ))
        
parser = CParser(stream)
tree = parser.program()

tree_str = Trees.toStringTree(tree,None,  parser)


visitor = JsonExportVisitor()
json_tree = visitor.visit(tree)
json_str = json.dumps(json_tree, indent=2)

semanticAnalizer = semanticVisitor() 
semanticAnalizer.visit(tree)
semanticAnalizer.save("/Users/kni/projects/spring/parser/test/hello.ll")

with open('AST.json', 'w') as f:
    f.write(json_str)

