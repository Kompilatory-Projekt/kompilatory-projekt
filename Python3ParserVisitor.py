# Generated from Python3Parser.g4 by ANTLR 4.11.1
from collections import deque
import re

import utils

from antlr4 import *
if __name__ is not None and "." in __name__:
    from .Python3Parser import Python3Parser
else:
    from Python3Parser import Python3Parser

# This class defines a complete generic visitor for a parse tree produced by Python3Parser.

class Python3ParserVisitor(ParseTreeVisitor):
    class Scopes:
        scopes = deque()
        
        GLOBAL_SCOPE_FUNCTIONS = {"print", "range", "abs", "round"}

        def __init__(self):
            self.enterScope() # Enter the global scope
            # Add the global scope functions to the global scope
            for func in self.GLOBAL_SCOPE_FUNCTIONS:
                self.getCurrentScope()["functions"].add(func)
        
        def enterScope(self):
            self.scopes.append({"variables": set(), "functions": set(), "classes": set()})
            
        def exitScope(self):
            self.scopes.pop()
                        
        def getCurrentScope(self):
            return self.scopes[-1]
        
        def inScope(self, name, return_subscope: bool = False) -> bool:
            for scope in self.scopes:
                for subscope in scope.values():
                    if name in subscope:
                        if return_subscope:
                            return True, subscope
                        return True
                    
            return False
        
        def addToCurrentScope(self, name, subscope):
            if self.inScope(name): # If the variable/function/class is overriden
                self.removeFromCurrentScope(name)
            
            self.getCurrentScope()[subscope].add(name)
            
        def removeFromCurrentScope(self, name):
            self.errorIfNotInScope(name)
            
            for scope in self.scopes:
                for subscope in scope.values():
                    if name in scope[subscope]:
                        scope[subscope].remove(name)
                        break
        
        subscope_names = {
                "variables": "Variable",
                "functions": "Function",
                "classes": "Class"
            }

        def errorIfNotInScope(self, name):
            is_scope = self.inScope(name)
            if not is_scope:
                raise NameError(f"{name} does not exist in the current scope")
            
    
    
    param_type_map = {
        'int': 'int',
        'float': 'float',
        'str': 'string',
        'bool': 'bool'
    }
    
    comparison_operator_map = {
        '>': '>',
        '<': '<',
        '==': '==',
        '!=': '!=',
        '>=': '>=',
        '<=': '<=',
        'is': '==',
        'isnot': '!='
    }
    
    arithmetic_operator_map = {
        '+': '+',
        '-': '-',
        '*': '*',
        '/': '/',
        '%': '%',
        '<<': '<<',
        '>>': '>>',
        '&': '&',
        '^': '^',
        '|': '|',
        '//': '/'  # Integer division in Python, regular division in C++
    }
    
    exception_type_map = {
        'Exception': 'std::exception',
        'ValueError': 'std::invalid_argument',
        'TypeError': 'std::invalid_argument',
        'NameError': 'std::invalid_argument',
        'ZeroDivisionError': 'std::domain_error',
        'IndexError': 'std::out_of_range',
        'KeyError': 'std::out_of_range',
        'FileNotFoundError': 'std::invalid_argument',
        'OSError': 'std::system_error',
        'NotImplementedError': 'std::logic_error',
        'AttributeError': 'std::invalid_argument',
        'ImportError': 'std::invalid_argument',
        'SyntaxError': 'std::invalid_argument',
        'IndentationError': 'std::invalid_argument',
        'OverflowError': 'std::overflow_error',
        'RuntimeError': 'std::runtime_error',
        'StopIteration': 'std::exception',
        'UnboundLocalError': 'std::invalid_argument',
        'UnicodeDecodeError': 'std::invalid_argument',
        'UnicodeEncodeError': 'std::invalid_argument',
        'UnicodeTranslateError': 'std::invalid_argument',
        'AssertionError': 'std::logic_error',
        'BufferError': 'std::runtime_error',
        'EOFError': 'std::eof_error',
        'ImportError': 'std::runtime_error',
        'LookupError': 'std::out_of_range',
        'MemoryError': 'std::bad_alloc',
        'ReferenceError': 'std::invalid_argument',
        'SystemExit': 'std::exception',
        'TypeError': 'std::invalid_argument',
        'ValueError': 'std::invalid_argument',
        'Warning': 'std::exception',
    }

    cpp_libraries_to_include = set()
    scopes = Scopes()
    
    # --------------
    # Custom methods
    # --------------
    
    def map_exception_type(self, except_clause):
        # Map Python exception types to C++ ones
        python_exception_type = except_clause.getChild(1).getText()
        cpp_exception_type = self.exception_type_map.get(python_exception_type, 'std::exception')
        
        return cpp_exception_type

    def get_exception_alias(self, except_clause: Python3Parser.Except_clauseContext):
        # Get the alias for the exception, if any
        if except_clause.getChildCount() == 3:
            return except_clause.alias().getText()
        else:
            return 'e'  # Default alias
        
    def is_nth_child(self, ctx, n):
        parent = ctx.parentCtx
        if not parent:
            return False
        
        return parent.getChild(n) == ctx

    # --------------
    # ANTLR4 methods
    # --------------
    
    def aggregateResult(self, aggregate, nextResult):
        result = ""
        if aggregate is not None:
            result += aggregate
        if nextResult is not None:
            result += nextResult
        
        return result
    
    def visitTerminal(self, node):
        if node.getSymbol().text == "<EOF>":
            return "<EOF>"
        
        return self.defaultResult()

    # Visit a parse tree produced by Python3Parser#single_input.
    def visitSingle_input(self, ctx:Python3Parser.Single_inputContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#file_input.
    def visitFile_input(self, ctx:Python3Parser.File_inputContext):
        result = self.visitChildren(ctx)

        class_definitions = ""
        function_definitions = ""
        main_code = ""
        eof_code = ""

        lines = result.split("\n")
        in_class = False
        in_function = False
        brace_count = 0

        for line in lines:
            stripped_line = line.strip()
            if "class " in stripped_line:
                in_class = True
            elif re.match(r"^\s*[\w\[\]]+\s+\w+\s*\([^)]*\)\s*", line) is not None:
                in_function = True

            if in_class:
                class_definitions += line + "\n"
                brace_count += stripped_line.count('{')
                brace_count -= stripped_line.count('}')
                
                if brace_count == 0:
                    in_class = False
            elif in_function:
                function_definitions += line + "\n"
                brace_count += stripped_line.count('{')
                brace_count -= stripped_line.count('}')
                
                if brace_count == 0:
                    in_function = False
            elif "<EOF>" in stripped_line:
                eof_code += "<EOF>\n"
            else:
                main_code += line + "\n"

        if "cout" in result:
            self.cpp_libraries_to_include.add("iostream")

        program_result = ""

        for lib in self.cpp_libraries_to_include:
            program_result += f"#include <{lib}>\n"

        program_result += """using namespace std; \n"""
        program_result += class_definitions
        program_result += function_definitions
        program_result += """int main() {\n""" 
        program_result += main_code
        program_result += """return 0;\n}"""
        program_result += eof_code

        return program_result


    # Visit a parse tree produced by Python3Parser#eval_input.
    def visitEval_input(self, ctx:Python3Parser.Eval_inputContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#decorator.
    def visitDecorator(self, ctx:Python3Parser.DecoratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#decorators.
    def visitDecorators(self, ctx:Python3Parser.DecoratorsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#decorated.
    def visitDecorated(self, ctx:Python3Parser.DecoratedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#async_funcdef.
    def visitAsync_funcdef(self, ctx:Python3Parser.Async_funcdefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Python3Parser#funcdef.
    def visitFuncdef(self, ctx:Python3Parser.FuncdefContext):    
        func_name = self.visit(ctx.name())
        
        return_type = 'void'
        if ctx.getChild(3).getText() == '->':
            return_type = self.visit(ctx.getChild(4))           

        self.scopes.addToCurrentScope(func_name, "functions")
        
        self.scopes.enterScope() # Enter the function scope
        
        params = self.visit(ctx.parameters())
        body = self.visit(ctx.block())
        
        self.scopes.exitScope() # Exit the function scope after visiting the block

        return f"{return_type} {func_name}{params} {body}"


    # Visit a parse tree produced by Python3Parser#parameters.
    def visitParameters(self, ctx:Python3Parser.ParametersContext):
        return f'({self.visitChildren(ctx)})'

    # Visit a parse tree produced by Python3Parser#typedargslist.
    def visitTypedargslist(self, ctx:Python3Parser.TypedargslistContext):
        from Python3Parser import Python3Parser
        params = []
        
        num_of_args = ctx.getChildCount() - ctx.getChildCount() // 2 # Subtract commas
        for i in range(num_of_args):
            params.append(self.visit(ctx.tfpdef(i)))
        
        params = filter(lambda param: 'self' != param.split(' ')[1], params)
        
        return ', '.join(params)


    # Visit a parse tree produced by Python3Parser#tfpdef.
    def visitTfpdef(self, ctx:Python3Parser.TfpdefContext):
        param_name = self.visit(ctx.name())
        
        self.scopes.addToCurrentScope(param_name, "variables")
        
        result = f"{param_name}"
        
        if ctx.test():
            param_type = self.visit(ctx.test())
            result = f"{param_type} {param_name}"
        
        return result


    # Visit a parse tree produced by Python3Parser#varargslist.
    def visitVarargslist(self, ctx:Python3Parser.VarargslistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#vfpdef.
    def visitVfpdef(self, ctx:Python3Parser.VfpdefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#stmt.
    def visitStmt(self, ctx:Python3Parser.StmtContext):    
        result = self.visitChildren(ctx)
        return result


    # Visit a parse tree produced by Python3Parser#simple_stmts.
    def visitSimple_stmts(self, ctx:Python3Parser.Simple_stmtsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#simple_stmt.
    def visitSimple_stmt(self, ctx:Python3Parser.Simple_stmtContext):
        if ctx.getText() == "pass":
            return ""
        
        result = self.visitChildren(ctx) + ";\n"
        
        return result


    # Visit a parse tree produced by Python3Parser#expr_stmt.
    def visitExpr_stmt(self, ctx:Python3Parser.Expr_stmtContext):
        from Python3Parser import Python3Parser
        
        # Variable assignment eg. a = 2
        if ctx.getChildCount() == 3 and ctx.getChild(1).getText() == '=':
                type, value = utils.get_type_of(ctx.getChild(2).getText())
                name = self.visit(ctx.getChild(0))
                
                self.scopes.addToCurrentScope(name, "variables")
                
                result = f"{type} {name} = {value}"
                
                return result
            
        # Type-annotated assignment eg. a: int = 2
        elif isinstance(ctx.getChild(1), Python3Parser.AnnassignContext):
            name = self.visit(ctx.testlist_star_expr(0))
            type = self.visit(ctx.annassign().test(0))
            value = self.visit(ctx.annassign().test(1))
            
            # Check if value type is the same as the annotated type
            value_type, _ = utils.get_type_of(value)
            if value_type != type:
                raise TypeError(f"Type mismatch: {value_type} and {type}")
            
            self.scopes.addToCurrentScope(name, "variables")
            
            return f"{type} {name} = {value}"
                
        return self.visitChildren(ctx)   


    # Visit a parse tree produced by Python3Parser#annassign.
    def visitAnnassign(self, ctx:Python3Parser.AnnassignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#testlist_star_expr.
    def visitTestlist_star_expr(self, ctx:Python3Parser.Testlist_star_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#augassign.
    def visitAugassign(self, ctx:Python3Parser.AugassignContext):
        return ctx.getText()


    # Visit a parse tree produced by Python3Parser#del_stmt.
    def visitDel_stmt(self, ctx:Python3Parser.Del_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#pass_stmt.
    def visitPass_stmt(self, ctx:Python3Parser.Pass_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#flow_stmt.
    def visitFlow_stmt(self, ctx:Python3Parser.Flow_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#break_stmt.
    def visitBreak_stmt(self, ctx:Python3Parser.Break_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#continue_stmt.
    def visitContinue_stmt(self, ctx:Python3Parser.Continue_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#return_stmt.
    def visitReturn_stmt(self, ctx:Python3Parser.Return_stmtContext):
        # Get the return expression
        expr = self.visit(ctx.testlist())

        # Format the return statement into a C++ return statement
        return f"return {expr}"


    # Visit a parse tree produced by Python3Parser#yield_stmt.
    def visitYield_stmt(self, ctx:Python3Parser.Yield_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#raise_stmt.
    def visitRaise_stmt(self, ctx:Python3Parser.Raise_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#import_stmt.
    def visitImport_stmt(self, ctx:Python3Parser.Import_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#import_name.
    def visitImport_name(self, ctx:Python3Parser.Import_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#import_from.
    def visitImport_from(self, ctx:Python3Parser.Import_fromContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#import_as_name.
    def visitImport_as_name(self, ctx:Python3Parser.Import_as_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#dotted_as_name.
    def visitDotted_as_name(self, ctx:Python3Parser.Dotted_as_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#import_as_names.
    def visitImport_as_names(self, ctx:Python3Parser.Import_as_namesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#dotted_as_names.
    def visitDotted_as_names(self, ctx:Python3Parser.Dotted_as_namesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#dotted_name.
    def visitDotted_name(self, ctx:Python3Parser.Dotted_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#global_stmt.
    def visitGlobal_stmt(self, ctx:Python3Parser.Global_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#nonlocal_stmt.
    def visitNonlocal_stmt(self, ctx:Python3Parser.Nonlocal_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#assert_stmt.
    def visitAssert_stmt(self, ctx:Python3Parser.Assert_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#compound_stmt.
    def visitCompound_stmt(self, ctx:Python3Parser.Compound_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#async_stmt.
    def visitAsync_stmt(self, ctx:Python3Parser.Async_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#if_stmt.
    def visitIf_stmt(self, ctx:Python3Parser.If_stmtContext):
        condition = self.visit(ctx.test(0))  # Visit the condition of the if statement
        block = self.visit(ctx.block(0))  # Visit the block of the if statement
        result = f"if ({condition}) {block}"

        for i in range(1, ctx.getChildCount()//4):
            condition = self.visit(ctx.test(i)) 
            block = self.visit(ctx.block(i))
            result += f"else if ({condition}) {block}"
        
        if ctx.getChildCount() % 4 == 3:
            block = self.visit(ctx.block(ctx.getChildCount()//4))
            result += f"else {block}"

        return result


    # Visit a parse tree produced by Python3Parser#while_stmt.
    def visitWhile_stmt(self, ctx:Python3Parser.While_stmtContext):
        condition = self.visit(ctx.test())  
        block = self.visit(ctx.block(0))  
        result = f"while ({condition}) {block}"

        return result

    # Visit a parse tree produced by Python3Parser#for_stmt.
    def visitFor_stmt(self, ctx:Python3Parser.For_stmtContext):

        test = self.visit(ctx.testlist())
        param = self.visit(ctx.exprlist())[0] #TODO: Works only for one param
        block = self.visit(ctx.block(0))

        if test.startswith("range"):
            test = test[6:-1].split(',')
            if len(test) == 1:
                test = [0, test[0], 1]
            elif len(test) == 2:
                test = [test[0], test[1], 1]

            sign = '<' if int(test[0]) < int(test[1]) else '>'
            result = f"for(int {param} = {test[0]}; {param} {sign} {test[1]}; {param} += {test[2]}) {block}"
        else:
            result = f"for(auto {param} : {test[0]}) {block}"

        return result


    # Visit a parse tree produced by Python3Parser#try_stmt.
    def visitTry_stmt(self, ctx:Python3Parser.Try_stmtContext):
        result = self.visitChildren(ctx)
        result = f"try {result}"
        
        return result

    # Visit a parse tree produced by Python3Parser#with_stmt.
    def visitWith_stmt(self, ctx:Python3Parser.With_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#with_item.
    def visitWith_item(self, ctx:Python3Parser.With_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#except_clause.
    def visitExcept_clause(self, ctx:Python3Parser.Except_clauseContext):
        exception_type = self.map_exception_type(ctx)
        exception_alias = self.get_exception_alias(ctx)
        
        result = f"catch ({exception_type}& {exception_alias}) "
        
        return result


    # Visit a parse tree produced by Python3Parser#block.
    def visitBlock(self, ctx:Python3Parser.BlockContext):
        result =  self.visitChildren(ctx)
        result = f"{{\n{result}}}\n"
        
        return result

    # Visit a parse tree produced by Python3Parser#match_stmt.
    def visitMatch_stmt(self, ctx:Python3Parser.Match_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#subject_expr.
    def visitSubject_expr(self, ctx:Python3Parser.Subject_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#star_named_expressions.
    def visitStar_named_expressions(self, ctx:Python3Parser.Star_named_expressionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#star_named_expression.
    def visitStar_named_expression(self, ctx:Python3Parser.Star_named_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#case_block.
    def visitCase_block(self, ctx:Python3Parser.Case_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#guard.
    def visitGuard(self, ctx:Python3Parser.GuardContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#patterns.
    def visitPatterns(self, ctx:Python3Parser.PatternsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#pattern.
    def visitPattern(self, ctx:Python3Parser.PatternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#as_pattern.
    def visitAs_pattern(self, ctx:Python3Parser.As_patternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#or_pattern.
    def visitOr_pattern(self, ctx:Python3Parser.Or_patternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#closed_pattern.
    def visitClosed_pattern(self, ctx:Python3Parser.Closed_patternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#literal_pattern.
    def visitLiteral_pattern(self, ctx:Python3Parser.Literal_patternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#literal_expr.
    def visitLiteral_expr(self, ctx:Python3Parser.Literal_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#complex_number.
    def visitComplex_number(self, ctx:Python3Parser.Complex_numberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#signed_number.
    def visitSigned_number(self, ctx:Python3Parser.Signed_numberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#signed_real_number.
    def visitSigned_real_number(self, ctx:Python3Parser.Signed_real_numberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#real_number.
    def visitReal_number(self, ctx:Python3Parser.Real_numberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#imaginary_number.
    def visitImaginary_number(self, ctx:Python3Parser.Imaginary_numberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#capture_pattern.
    def visitCapture_pattern(self, ctx:Python3Parser.Capture_patternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#pattern_capture_target.
    def visitPattern_capture_target(self, ctx:Python3Parser.Pattern_capture_targetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#wildcard_pattern.
    def visitWildcard_pattern(self, ctx:Python3Parser.Wildcard_patternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#value_pattern.
    def visitValue_pattern(self, ctx:Python3Parser.Value_patternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#attr.
    def visitAttr(self, ctx:Python3Parser.AttrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#name_or_attr.
    def visitName_or_attr(self, ctx:Python3Parser.Name_or_attrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#group_pattern.
    def visitGroup_pattern(self, ctx:Python3Parser.Group_patternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#sequence_pattern.
    def visitSequence_pattern(self, ctx:Python3Parser.Sequence_patternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#open_sequence_pattern.
    def visitOpen_sequence_pattern(self, ctx:Python3Parser.Open_sequence_patternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#maybe_sequence_pattern.
    def visitMaybe_sequence_pattern(self, ctx:Python3Parser.Maybe_sequence_patternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#maybe_star_pattern.
    def visitMaybe_star_pattern(self, ctx:Python3Parser.Maybe_star_patternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#star_pattern.
    def visitStar_pattern(self, ctx:Python3Parser.Star_patternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#mapping_pattern.
    def visitMapping_pattern(self, ctx:Python3Parser.Mapping_patternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#items_pattern.
    def visitItems_pattern(self, ctx:Python3Parser.Items_patternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#key_value_pattern.
    def visitKey_value_pattern(self, ctx:Python3Parser.Key_value_patternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#double_star_pattern.
    def visitDouble_star_pattern(self, ctx:Python3Parser.Double_star_patternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#class_pattern.
    def visitClass_pattern(self, ctx:Python3Parser.Class_patternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#positional_patterns.
    def visitPositional_patterns(self, ctx:Python3Parser.Positional_patternsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#keyword_patterns.
    def visitKeyword_patterns(self, ctx:Python3Parser.Keyword_patternsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#keyword_pattern.
    def visitKeyword_pattern(self, ctx:Python3Parser.Keyword_patternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#test.
    def visitTest(self, ctx:Python3Parser.TestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#test_nocond.
    def visitTest_nocond(self, ctx:Python3Parser.Test_nocondContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#lambdef.
    def visitLambdef(self, ctx:Python3Parser.LambdefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#lambdef_nocond.
    def visitLambdef_nocond(self, ctx:Python3Parser.Lambdef_nocondContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#or_test.
    def visitOr_test(self, ctx:Python3Parser.Or_testContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#and_test.
    def visitAnd_test(self, ctx:Python3Parser.And_testContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#not_test.
    def visitNot_test(self, ctx:Python3Parser.Not_testContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#comparison.
    def visitComparison(self, ctx:Python3Parser.ComparisonContext):
        left = self.visit(ctx.expr(0))  # Visit the left operand

        # Check if a comparison operator exists
        if ctx.comp_op():
            operator = ctx.comp_op(0).getText()
        else:
            operator = ''

        right = self.visit(ctx.expr(1)) if ctx.expr(1) else ''  # Visit the right operand if it exists

        # Convert the Python comparison operator to a C++ one
        cpp_operator = self.comparison_operator_map.get(operator, operator)

        # Return the C++ comparison expression
        return f"{left} {cpp_operator} {right}" if operator else left


    # Visit a parse tree produced by Python3Parser#comp_op.
    def visitComp_op(self, ctx:Python3Parser.Comp_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#star_expr.
    def visitStar_expr(self, ctx:Python3Parser.Star_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#expr.
    def visitExpr(self, ctx:Python3Parser.ExprContext):
        # If the expr has 3 children, it is an "item operator item" expression
        if ctx.getChildCount() == 3:
            left = self.visit(ctx.expr(0))
            operator = ctx.getChild(1).getText()
            right = self.visit(ctx.expr(1))

            if operator == '**':
                self.cpp_libraries_to_include.add("cmath")
                return f"pow({left}, {right})"

            if operator in self.arithmetic_operator_map:
                operator = self.arithmetic_operator_map[operator]

                return f"{left} {operator} {right}"
        
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#atom_expr.
    def visitAtom_expr(self, ctx:Python3Parser.Atom_exprContext):
        name = self.visit(ctx.atom()) # Atom expr always has one atom
        
        if name == 'print':
            trailer = ctx.trailer(0)
            
            if trailer.getChild(1).getText() == ')': # If there are empty parentheses
                return "cout << endl"
            
            cout_args = self.visit(trailer)
            
            if cout_args.startswith('(') and cout_args.endswith(')'):
                cout_args = cout_args[1:-1]
    
            return f"cout << {cout_args} << endl"
        
        if name == 'abs':
            self.cpp_libraries_to_include.add("cmath")
            return f"abs{self.visit(ctx.trailer(0))}"
        
        if name == 'round':
            self.cpp_libraries_to_include.add("cmath")
            return f"round{self.visit(ctx.trailer(0))}"
        
        return self.visitChildren(ctx)

    def get_nth_parent(self, ctx, n):
        parent = ctx
        for _ in range(n):
            parent = parent.parentCtx
            if not parent:
                break
            
        return parent

    # Visit a parse tree produced by Python3Parser#atom.
    def visitAtom(self, ctx:Python3Parser.AtomContext):
        from Python3Parser import Python3Parser
        text = ctx.getText()
        
        if text in self.param_type_map:
            return self.param_type_map.get(text, 'auto')
        
        if text.startswith("'") and text.endswith("'"):
            # Changed single quotes to double quotes
            return f'"{text[1:-1]}"'
        
        if ctx.name():
            name = self.visit(ctx.name())
            
            # Check if the atom comes from assignment
            parent_argument = self.get_nth_parent(ctx, 8) # Argument is 8 levels up
            parent_expr_stmt = self.get_nth_parent(ctx, 9) # Expr_stmt is 9 levels up
            
            # Check if atom is on the left side of an assignment eg. function(atom = 1)
            is_lhs_of_keyword_argument = None
            if isinstance(parent_argument, Python3Parser.ArgumentContext):
                is_keyword_argument = parent_argument.getChildCount() == 3
                is_lhs_of_assignment = parent_argument.getChild(0) == self.get_nth_parent(ctx, 7) # 7 levels up is the test
                
                is_lhs_of_keyword_argument = (is_keyword_argument and is_lhs_of_assignment)
                
            is_being_assigned_to = None
            if isinstance(parent_expr_stmt, Python3Parser.Expr_stmtContext):
                is_being_assigned_to = isinstance(parent_expr_stmt.getChild(1), Python3Parser.AnnassignContext) or parent_expr_stmt.getChildCount() == 3
            
            # If atom is a lhs of an assignment or a keyword argument, return the name, don't check if it exists in scope
            if is_being_assigned_to or is_lhs_of_keyword_argument:
                return self.visitChildren(ctx)

            # If atom is a variable, funcion call or class name check if it exists in scope
            if not self.scopes.inScope(name):
                raise NameError(f"{name} does not exist in any scope")
            
            return self.visitChildren(ctx)
        
        return text


    # Visit a parse tree produced by Python3Parser#name.
    def visitName(self, ctx:Python3Parser.NameContext):
        return ctx.getText()


    # Visit a parse tree produced by Python3Parser#testlist_comp.
    def visitTestlist_comp(self, ctx:Python3Parser.Testlist_compContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#trailer.
    def visitTrailer(self, ctx:Python3Parser.TrailerContext):
        
        if ctx.getChildCount() == 2:
            return ctx.getText()
        
        if ctx.getChildCount() == 3:
            if ctx.getChild(0).getText() == '(' and ctx.getChild(2).getText() == ')':
                return '(' + self.visit(ctx.getChild(1)) + ')'
        
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#subscriptlist.
    def visitSubscriptlist(self, ctx:Python3Parser.SubscriptlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#subscript_.
    def visitSubscript_(self, ctx:Python3Parser.Subscript_Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#sliceop.
    def visitSliceop(self, ctx:Python3Parser.SliceopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#exprlist.
    def visitExprlist(self, ctx:Python3Parser.ExprlistContext):
        result = []
        for i in range(ctx.getChildCount()):
            result.append(ctx.getChild(i).getText())

        if result.count(','):
            result.remove(',')

        return result


    # Visit a parse tree produced by Python3Parser#testlist.
    def visitTestlist(self, ctx:Python3Parser.TestlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#dictorsetmaker.
    def visitDictorsetmaker(self, ctx:Python3Parser.DictorsetmakerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#classdef.
    def visitClassdef(self, ctx:Python3Parser.ClassdefContext):
        return f"{ctx.getChild(0).getText()} {self.visitChildren(ctx)}"


    # Visit a parse tree produced by Python3Parser#arglist.
    def visitArglist(self, ctx:Python3Parser.ArglistContext):
        result = ""
        
        num_of_args = ctx.getChildCount() - ctx.getChildCount() // 2 # Subtract commas
        for i in range(num_of_args):
            result += self.visit(ctx.argument(i))
            if i < num_of_args - 1:
                result += ", "
        
        return result


    # Visit a parse tree produced by Python3Parser#argument.
    def visitArgument(self, ctx:Python3Parser.ArgumentContext):
        # If the argument is a single parameter, func(a)
        if ctx.getChildCount() == 1:
            if ctx.getChild(0).getChildCount() == 1: # TODO: Check if this is correct
                arg_name = self.visit(ctx.getChild(0))
                
                # self.scopes.errorIfNotInScope(arg_name)
                
                return arg_name
        # If argument is a keyword argument, func(a=1)
        if ctx.getChildCount() == 3:
            arg_name = self.visit(ctx.getChild(0))
            arg_value = self.visit(ctx.getChild(2))
            
            return f"{arg_name} = {arg_value}"
        
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#comp_iter.
    def visitComp_iter(self, ctx:Python3Parser.Comp_iterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#comp_for.
    def visitComp_for(self, ctx:Python3Parser.Comp_forContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#comp_if.
    def visitComp_if(self, ctx:Python3Parser.Comp_ifContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#encoding_decl.
    def visitEncoding_decl(self, ctx:Python3Parser.Encoding_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#yield_expr.
    def visitYield_expr(self, ctx:Python3Parser.Yield_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#yield_arg.
    def visitYield_arg(self, ctx:Python3Parser.Yield_argContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#strings.
    def visitStrings(self, ctx:Python3Parser.StringsContext):
        return self.visitChildren(ctx)


del Python3Parser