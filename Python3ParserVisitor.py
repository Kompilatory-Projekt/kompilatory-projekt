# Generated from Python3Parser.g4 by ANTLR 4.11.1
import utils
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .Python3Parser import Python3Parser
else:
    from Python3Parser import Python3Parser

# This class defines a complete generic visitor for a parse tree produced by Python3Parser.

class Python3ParserVisitor(ParseTreeVisitor):
    param_type_map = {
        'int': 'int',
        'float': 'float',
        'str': 'string',
        'bool': 'bool'
    }

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
        return result


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
        
        params = []
        if ctx.parameters().getChildCount() > 2:
            params = [self.visit(param) for param in ctx.parameters().typedargslist().tfpdef()]
            
        body = self.visit(ctx.block())
        
        return_type = 'void'
        if ctx.getChild(3).getText() == '->':
            return_type = self.visit(ctx.getChild(4))

        return f"{return_type} {func_name}({', '.join(params)}) {{\n{body}\n}}\n"


    # Visit a parse tree produced by Python3Parser#parameters.
    def visitParameters(self, ctx:Python3Parser.ParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#typedargslist.
    def visitTypedargslist(self, ctx:Python3Parser.TypedargslistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#tfpdef.
    def visitTfpdef(self, ctx:Python3Parser.TfpdefContext):
        param_name = self.visit(ctx.name())
        param_type = self.visit(ctx.test())
        
        return f"{param_type} {param_name}"


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
        n = ctx.getChildCount()
        result = None
        for i in range(n):
            c = ctx.getChild(i)

            if c.getText() == '\n':
               if result is None:
                   result = c.getText()
               else:
                   result += c.getText()
            else:
                childResult = c.accept(self)
                result = self.aggregateResult(result, childResult)

        return result


    # Visit a parse tree produced by Python3Parser#simple_stmt.
    def visitSimple_stmt(self, ctx:Python3Parser.Simple_stmtContext):
        result = self.visitChildren(ctx)

        return result


    # Visit a parse tree produced by Python3Parser#expr_stmt.
    def visitExpr_stmt(self, ctx:Python3Parser.Expr_stmtContext):
        if ctx.getChildCount() == 3:
            # Assignment
            if ctx.getChild(1).getText() == '=':
                _type, _value = utils.getTypeOf(ctx.getChild(2).getText())
                result = f"{_type} {self.visitChildren(ctx.getChild(0))} = {_value};\n"
                return result           
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
        return f"return {expr};\n"


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
        result = f"if ({condition}) {{\n{block}}}\n"

        for i in range(1, ctx.getChildCount()//4):
            condition = self.visit(ctx.test(i)) 
            block = self.visit(ctx.block(i))
            result += f"else if ({condition}) {{\n{block}}}\n"
        
        if ctx.getChildCount() % 4 == 3:
            block = self.visit(ctx.block(ctx.getChildCount()//4))
            result += f"else {{\n{block}}}\n"

        return result


    # Visit a parse tree produced by Python3Parser#while_stmt.
    def visitWhile_stmt(self, ctx:Python3Parser.While_stmtContext):
        condition = self.visit(ctx.test())  
        block = self.visit(ctx.block(0))  
        result = f"while ({condition}) {{\n{block}}}\n"

        return result

    # Visit a parse tree produced by Python3Parser#for_stmt.
    def visitFor_stmt(self, ctx:Python3Parser.For_stmtContext):

        test = self.visit(ctx.testlist())

        if test.startswith("range"):
            test = test[5:].split(',')
            if len(test) == 1:
                test = [0, test[0], 1]
            elif len(test) == 2:
                test = [test[0], test[1], 1]

            sign = '<' if int(test[0]) < int(test[1]) else '>'
            result = f"for(int {params} = {test[0]}; {params} {sign} {test[1]}; {params} += {test[2]}) {{\n{block}}}\n"
        else:
            params = self.visit(ctx.exprlist())
            block = self.visit(ctx.block(0))
            result = f"for(auto {params[0]} : {test[0]}) {{\n{block}}}\n"

        print(self.visit(ctx.testlist()))

        return result


    # Visit a parse tree produced by Python3Parser#try_stmt.
    def visitTry_stmt(self, ctx:Python3Parser.Try_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#with_stmt.
    def visitWith_stmt(self, ctx:Python3Parser.With_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#with_item.
    def visitWith_item(self, ctx:Python3Parser.With_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#except_clause.
    def visitExcept_clause(self, ctx:Python3Parser.Except_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#block.
    def visitBlock(self, ctx:Python3Parser.BlockContext):
        return self.visitChildren(ctx)


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

        # Map Python comparison operators to C++ ones
        operator_mapping = {
            '>': '>',
            '<': '<',
            '==': '==',
            '!=': '!=',
            '>=': '>=',
            '<=': '<=',
            'is': '==',
            'isnot': '!='
        }

        # Convert the Python comparison operator to a C++ one
        cpp_operator = operator_mapping.get(operator, operator)

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
        if ctx.getChildCount() == 3:
            left = self.visit(ctx.expr(0))
            operator = ctx.getChild(1).getText()
            right = self.visit(ctx.expr(1))

            operator_mapping = {
                '+': '+',
                '-': '-',
                '*': '*',
                '/': '/',
                '%': '%',
                '**': 'pow',
                '<<': '<<',
                '>>': '>>',
                '&': '&',
                '^': '^',
                '|': '|',
                '//': '/'  # Integer division in Python, regular division in C++
            }

            if operator in operator_mapping:
                operator = operator_mapping[operator]

                return f"{left} {operator} {right}"
            else:
                return self.visitChildren(ctx)
            
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#atom_expr.
    def visitAtom_expr(self, ctx:Python3Parser.Atom_exprContext):
        if ctx.getChild(0).getText() == 'print':
            trailer = ctx.trailer(0)
            
            if trailer.getChild(1).getText() == ')': # If there are empty parentheses
                return "cout << endl;\n"
            
            return f"cout << {self.visit(trailer)} << endl;\n"
        
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#atom.
    def visitAtom(self, ctx:Python3Parser.AtomContext):
        text = ctx.getText()
        
        if text in self.param_type_map:
            return self.param_type_map.get(text, 'auto')
            
        if text.startswith("'") and text.endswith("'"):
            return f'"{text[1:-1]}"'  # Changed single quotes to double quotes
        
        return text


    # Visit a parse tree produced by Python3Parser#name.
    def visitName(self, ctx:Python3Parser.NameContext):
        return ctx.getText()


    # Visit a parse tree produced by Python3Parser#testlist_comp.
    def visitTestlist_comp(self, ctx:Python3Parser.Testlist_compContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#trailer.
    def visitTrailer(self, ctx:Python3Parser.TrailerContext):
        if ctx.getChild(1).getText() == '(' and ctx.getChild(2).getText() == ')':
            return self.visit(ctx.arglist())
        
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
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#arglist.
    def visitArglist(self, ctx:Python3Parser.ArglistContext):

        result = ctx.getChild(0).getText()
        for i in range(1, ctx.getChildCount()):
            result += ctx.getChild(i).getText()
            
        return result


    # Visit a parse tree produced by Python3Parser#argument.
    def visitArgument(self, ctx:Python3Parser.ArgumentContext):
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