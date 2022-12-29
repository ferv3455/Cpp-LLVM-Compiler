from typing import Any, Callable

import llvmlite.ir as ll

from .context import Context
from .builder import Builder
from ..parser import Symbol


# Decorator definition

handlers = dict()

def handler(name: str):
    global handlers
    def wrapper(func: Callable) -> Callable:
        if name in handlers:
            raise SyntaxError("Multiple handlers assigned to " + name)
        handlers[name] = func
        return func
    return wrapper


# ================= CODE BEGINS HERE=================

# TYPE DEFINITIONS
int_type = ll.IntType(32)
bool_type = ll.IntType(8)
char_type = ll.IntType(8)
double_type = ll.DoubleType()
void_type = ll.VoidType()
voidptr_type = ll.PointerType(char_type)
type_dict = {
    'int': int_type,
    'bool': bool_type,
    'char': char_type,
    'double': double_type,
    'void': void_type,
    'ptr': voidptr_type,
}


# HANDLERS FOR ALL SYMBOLS
@handler('macro')
def proc_macro(symbol: Symbol, builder: Builder, context: Context, proc: Callable):
    content = symbol.token.value
    begin = content.index('<')
    end = content.index('>')
    name = content[begin + 1 : end].strip()

    if name == 'cstdio':
        printf_type = ll.FunctionType(int_type, (voidptr_type, ), var_arg=True)
        ll.Function(context.module, printf_type, name='printf')
        ll.Function(context.module, printf_type, name='scanf')
    elif name == 'cstring':
        char_ptr_type = ll.PointerType(char_type)
        strlen_type = ll.FunctionType(int_type, (char_ptr_type, ))
        ll.Function(context.module, strlen_type, name='strlen')
        strcmp_type = ll.FunctionType(int_type, (char_ptr_type, char_ptr_type))
        ll.Function(context.module, strcmp_type, name='strcmp')
        strcat_type = ll.FunctionType(char_ptr_type, (char_ptr_type, char_ptr_type))
        ll.Function(context.module, strcat_type, name='strcat')
        ll.Function(context.module, strcat_type, name='strcpy')
        strnlen_type = ll.FunctionType(int_type, (char_ptr_type, int_type))
        ll.Function(context.module, strnlen_type, name='strnlen')
        strncmp_type = ll.FunctionType(int_type, (char_ptr_type, char_ptr_type, int_type))
        ll.Function(context.module, strncmp_type, name='strncmp')
        strncat_type = ll.FunctionType(char_ptr_type, (char_ptr_type, char_ptr_type, int_type))
        ll.Function(context.module, strncat_type, name='strncat')
        ll.Function(context.module, strncat_type, name='strncpy')

@handler('TYPE-SPECS')
@handler('DECLARATORS')
def proc_type_specs(symbol: Symbol, builder: Builder, context: Context, proc: Callable):
    return [proc(s, builder, context) for s in symbol.symbols]

@handler('FUNC-ST')
def proc_func_st(symbol: Symbol, builder: Builder, context: Context, proc: Callable):
    # Check syntax
    types, name, param_list = symbol.symbols[:3]
    name = name.token.value
    if len(param_list.symbols) == 3:
        params = proc(param_list.symbols[1], builder, context)
    else:
        params = list()

    # Return type
    types = proc(types, builder, context)
    ret_type = type_dict[types[0].name]

    # Parameter types
    param_types = list()
    for param in params:
        var_type = type_dict[param['type'].name]
        if 'size' in param['var']:
            var_type = ll.ArrayType(var_type, param['var']['size'][0].constant)
            var_type = ll.PointerType(var_type)
        param_types.append(var_type)
    
    # Function declaration
    func_type = ll.FunctionType(ret_type, param_types)
    func = ll.Function(context.module, func_type, name=name)
    block = func.append_basic_block()
    builder.position_at_end(block)

    # Create context for the function
    inner_context = context.addChild()
    inner_context.func = func
    inner_context.block = block

    # Add parameters
    for param, arg in zip(params, func.args):
        var_type = type_dict[param['type'].name]
        if 'size' in param['var']:
            var_type = ll.ArrayType(var_type, param['var']['size'][0].constant)
            var_type = ll.PointerType(var_type)
        var_name = param['var']['name']
        var_ptr = builder.alloca(var_type, name=var_name)
        inner_context.variables[var_name] = {
            'ptr': var_ptr,
            'type': str(var_type)
        }
        builder.store(arg, var_ptr)

    # Process compound statement
    proc(symbol.symbols[3], builder, inner_context)

    # Add return; if return void
    if ret_type == void_type:
        builder.ret_void()
    return func

@handler('PARAMS')
def proc_params(symbol: Symbol, builder: Builder, context: Context, proc: Callable):
    params = list()
    for decl in symbol.symbols:
        var_type = proc(decl.symbols[0], builder, context)
        var_name = proc(decl.symbols[1], builder, context)
        params.append({
            'type': var_type[0],
            'var': var_name[0]
        })
    return params

@handler('SEL-ST')
def proc_sel_st(symbol: Symbol, builder: Builder, context: Context, proc: Callable):
    if symbol.symbols[0].name == 'if':
        # Three blocks
        if_true = builder.append_basic_block()
        if_false = builder.append_basic_block()
        end = builder.append_basic_block()

        # Check condition
        condition = toBoolean(proc(symbol.symbols[2], builder, context), builder)
        builder.cbranch(condition, if_true, if_false)

        # True block
        builder.position_at_end(if_true)
        proc(symbol.symbols[4], builder, context)
        builder.branch(end)

        # False block
        builder.position_at_end(if_false)
        if len(symbol.symbols) > 5:
            proc(symbol.symbols[6], builder, context)
        builder.branch(end)

        # Move to end
        builder.position_at_end(end)

    else:
        raise SyntaxError("Not Implemented")

@handler('ITER-ST')
def proc_iter_st(symbol: Symbol, builder: Builder, context: Context, proc: Callable):
    if symbol.symbols[0].name == 'for':
        s1, s2, s3 = proc(symbol.symbols[2], builder, context)
        st = symbol.symbols[4]

        inner_context = context.addChild()

        # Initialization
        proc(s1, builder, inner_context)

        # Four blocks
        condition = builder.append_basic_block()
        body = builder.append_basic_block()
        body_end = builder.append_basic_block()
        end = builder.append_basic_block()
        inner_context.exit.append(end)       # break
        inner_context.exit.append(body_end)  # continue

        # End of last block
        builder.branch(condition)

        # Condition block
        builder.position_at_end(condition)
        res = toBoolean(proc(s2, builder, inner_context), builder)
        builder.cbranch(res, body, end)

        # Body block
        builder.position_at_end(body)
        proc(st, builder, inner_context)
        builder.branch(body_end)

        # Body-end block
        builder.position_at_end(body_end)
        proc(s3, builder, inner_context)
        builder.branch(condition)

        # Move to end
        builder.position_at_end(end)

    elif symbol.symbols[0].name == 'while':
        expr = symbol.symbols[2]
        st = symbol.symbols[4]

        inner_context = context.addChild()

        # Three blocks
        condition = builder.append_basic_block()
        body = builder.append_basic_block()
        end = builder.append_basic_block()
        inner_context.exit.append(end)       # break
        inner_context.exit.append(body)      # continue

        # End of last block
        builder.branch(condition)

        # Condition block
        builder.position_at_end(condition)
        res = toBoolean(proc(expr, builder, inner_context), builder)
        builder.cbranch(res, body, end)

        # Body block
        builder.position_at_end(body)
        proc(st, builder, inner_context)
        builder.branch(condition)

        # Move to end
        builder.position_at_end(end)

    elif symbol.symbols[0].name == 'do':
        expr = symbol.symbols[4]
        st = symbol.symbols[1]

        inner_context = context.addChild()

        # Three blocks
        body = builder.append_basic_block()
        condition = builder.append_basic_block()
        end = builder.append_basic_block()
        inner_context.exit.append(end)       # break
        inner_context.exit.append(body)      # continue

        # End of last block
        builder.branch(body)

        # Body block
        builder.position_at_end(body)
        proc(st, builder, inner_context)
        builder.branch(condition)

        # Condition block
        builder.position_at_end(condition)
        res = toBoolean(proc(expr, builder, inner_context), builder)
        builder.cbranch(res, body, end)

        # Move to end
        builder.position_at_end(end)

    else:
        raise SyntaxError("Not Implemented")

@handler('FOR-COND')
def proc_for_cond(symbol: Symbol, builder: Builder, context: Context, proc: Callable):
    return (symbol.symbols[0], symbol.symbols[2], symbol.symbols[4])

@handler('JMP-ST')
def proc_jmp_st(symbol: Symbol, builder: Builder, context: Context, proc: Callable):
    if symbol.symbols[0].name == 'return':
        if symbol.symbols[1].name == 'semicolon':
            return builder.ret_void();
        else:
            return builder.ret(proc(symbol.symbols[1], builder, context));

    elif symbol.symbols[0].name == 'break':
        builder.branch(context.exit[0])

    elif symbol.symbols[0].name == 'continue':
        builder.branch(context.exit[1])

    return None

@handler('DECL')
def proc_decl(symbol: Symbol, builder: Builder, context: Context, proc: Callable):
    if symbol.symbols[0].name == 'using':
        return None
    else:
        if len(symbol.symbols) == 3:
            raise NotImplemented
        types, declarators = (proc(s, builder, context) for s in symbol.symbols)
        var_type = type_dict[types[0].name]
        for dec in declarators:
            if 'size' in dec:
                var_type = ll.ArrayType(var_type, dec['size'][0].constant)
            if context.func is None:
                # global
                var_global = ll.GlobalVariable(context.module, var_type, dec['name'])
                init = dec.get('init', ll.Constant(var_global.value_type, ll.Undefined))
                var_global.initializer = init
                context.globals[dec['name']] = {
                    'ptr': var_global,
                    'type': str(var_type)
                }
            else:
                # local
                var_ptr = builder.alloca(var_type, name=dec['name'])
                context.variables[dec['name']] = {
                    'ptr': var_ptr,
                    'type': str(var_type)
                }
                if 'init' in dec:
                    builder.store(dec['init'], var_ptr)

@handler('TYPE-SPEC')
def proc_type_spec(symbol: Symbol, builder: Builder, context: Context, proc: Callable):
    return symbol.symbols[0]

@handler('ID-DECL')
def proc_id_decl(symbol: Symbol, builder: Builder, context: Context, proc: Callable):
    res = {'name': symbol.symbols[0].token.value}
    children_num = len(symbol.symbols)
    if children_num == 3:
        res['init'] = proc(symbol.symbols[2], builder, context)
    elif children_num == 4:
        res['size'] = (proc(symbol.symbols[2], builder, context), )
    
    return res

@handler('LVAL')
def proc_lval(symbol: Symbol, builder: Builder, context: Context, proc: Callable):
    if len(symbol.symbols) == 1:
        return fetchID(symbol.symbols[0].symbols[0].token.value, builder, context, True)
    else:
        # Array element
        i = proc(symbol.symbols[2], builder, context)
        return fetchArrayElem(symbol.symbols[0].symbols[0].token.value, i, builder, context, True)

@handler('EXPR-L16')
def proc_expr_l16(symbol: Symbol, builder: Builder, context: Context, proc: Callable):
    if symbol.symbols[1].name == 'assignment-op':
        value = proc(symbol.symbols[2], builder, context)
        var_ptr = proc(symbol.symbols[0], builder, context)
        builder.store(value, var_ptr)
        return value
    elif symbol.symbols[1].name == 'arithm-assign-op':
        value = proc(symbol.symbols[2], builder, context)
        var_ptr = proc(symbol.symbols[0], builder, context)
        last = builder.load(var_ptr)
        if symbol.symbols[1].token.value == '+=':
            new_val = builder.add(last, value)
        elif symbol.symbols[1].token.value == '-=':
            new_val = builder.sub(last, value)
        elif symbol.symbols[1].token.value == '*=':
            new_val = builder.mul(last, value)
        elif symbol.symbols[1].token.value == '/=':
            new_val = builder.sdiv(last, value)
        elif symbol.symbols[1].token.value == '%=':
            new_val = builder.srem(last, value)
        else:
            raise SyntaxError("Not Implemented")
        builder.store(new_val, var_ptr)
        return value
    elif symbol.symbols[1].name == 'bit-assign-op':
        value = proc(symbol.symbols[2], builder, context)
        var_ptr = proc(symbol.symbols[0], builder, context)
        last = builder.load(var_ptr)
        if symbol.symbols[1].token.value == '<<=':
            new_val = builder.shl(last, value)
        elif symbol.symbols[1].token.value == '>>=':
            new_val = builder.ashr(last, value)
        elif symbol.symbols[1].token.value == '&=':
            new_val = builder.and_(last, value)
        elif symbol.symbols[1].token.value == '^=':
            new_val = builder.xor(last, value)
        elif symbol.symbols[1].token.value == '|=':
            new_val = builder.or_(last, value)
        else:
            raise SyntaxError("Not Implemented")
        builder.store(new_val, var_ptr)
        return value
    else:
        raise SyntaxError("Not Implemented")

@handler('EXPR-L15')
def proc_expr_l15(symbol: Symbol, builder: Builder, context: Context, proc: Callable):
    operator1 = toBoolean(proc(symbol.symbols[0], builder, context), builder)
    operator2 = toBoolean(proc(symbol.symbols[2], builder, context), builder)
    return builder.or_(operator1, operator2)

@handler('EXPR-L14')
def proc_expr_l14(symbol: Symbol, builder: Builder, context: Context, proc: Callable):
    operator1 = toBoolean(proc(symbol.symbols[0], builder, context), builder)
    operator2 = toBoolean(proc(symbol.symbols[2], builder, context), builder)
    return builder.and_(operator1, operator2)

@handler('EXPR-L13')
def proc_expr_l13(symbol: Symbol, builder: Builder, context: Context, proc: Callable):
    operator1 = proc(symbol.symbols[0], builder, context)
    operator2 = proc(symbol.symbols[2], builder, context)
    return builder.or_(operator1, operator2)

@handler('EXPR-L12')
def proc_expr_l12(symbol: Symbol, builder: Builder, context: Context, proc: Callable):
    operator1 = proc(symbol.symbols[0], builder, context)
    operator2 = proc(symbol.symbols[2], builder, context)
    return builder.xor_(operator1, operator2)

@handler('EXPR-L11')
def proc_expr_l11(symbol: Symbol, builder: Builder, context: Context, proc: Callable):
    operator1 = proc(symbol.symbols[0], builder, context)
    operator2 = proc(symbol.symbols[2], builder, context)
    return builder.and_(operator1, operator2)

@handler('EXPR-L10')
def proc_expr_l10(symbol: Symbol, builder: Builder, context: Context, proc: Callable):
    operator1 = proc(symbol.symbols[0], builder, context)
    operator2 = proc(symbol.symbols[2], builder, context)
    return builder.icmp_signed(symbol.symbols[1].token.value, operator1, operator2)

@handler('EXPR-L7')
def proc_expr_l7(symbol: Symbol, builder: Builder, context: Context, proc: Callable):
    operator1 = proc(symbol.symbols[0], builder, context)
    operator2 = proc(symbol.symbols[2], builder, context)
    if symbol.symbols[1].token.value == '<<':
        return builder.shl(operator1, operator2)
    elif symbol.symbols[1].token.value == '>>':
        return builder.ashr(operator1, operator2)
    else:
        raise SyntaxError("Not Implemented")

@handler('EXPR-L6')
def proc_expr_l6(symbol: Symbol, builder: Builder, context: Context, proc: Callable):
    operator1 = proc(symbol.symbols[0], builder, context)
    operator2 = proc(symbol.symbols[2], builder, context)
    if symbol.symbols[1].token.value == '+':
        return builder.add(operator1, operator2)
    elif symbol.symbols[1].token.value == '-':
        return builder.sub(operator1, operator2)
    else:
        raise SyntaxError("Not Implemented")

@handler('EXPR-L5')
def proc_expr_l5(symbol: Symbol, builder: Builder, context: Context, proc: Callable):
    operator1 = proc(symbol.symbols[0], builder, context)
    operator2 = proc(symbol.symbols[2], builder, context)
    if symbol.symbols[1].token.value == '*':
        return builder.mul(operator1, operator2)
    elif symbol.symbols[1].token.value == '/':
        return builder.sdiv(operator1, operator2)
    elif symbol.symbols[1].token.value == '%':
        return builder.srem(operator1, operator2)
    else:
        raise SyntaxError("Not Implemented")

@handler('EXPR-L3')
def proc_expr_l3(symbol: Symbol, builder: Builder, context: Context, proc: Callable):
    if len(symbol.symbols) == 1:
        return proc(symbol.symbols[0], builder, context)

    if symbol.symbols[0].name == 'increment-op':
        # Increment
        lval = symbol.symbols[1]
        if len(lval.symbols) == 1:
            name = lval.symbols[0].symbols[0].token.value
            last = fetchID(name, builder, context)
            dest = fetchID(name, builder, context, True)
        else:
            name = lval.symbols[0].symbols[0].token.value
            index = proc(lval.symbols[2], builder, context)
            last = fetchArrayElem(name, index, builder, context)
            dest = fetchArrayElem(name, index, builder, context, True)
        if symbol.symbols[0].token.value == '++':
            new_val = builder.add(last, ll.Constant(int_type, 1))
        else:
            new_val = builder.sub(last, ll.Constant(int_type, 1))
        builder.store(new_val, dest)
        return new_val

    elif symbol.symbols[0].name == 'bit-op' and symbol.symbols[0].value == '&':
        # Return the address
        lval = symbol.symbols[1]
        if len(lval.symbols) == 1:
            name = lval.symbols[0].symbols[0].token.value
            return fetchID(name, builder, context, True)
        else:
            name = lval.symbols[0].symbols[0].token.value
            index = proc(lval.symbols[2], builder, context)
            return fetchArrayElem(name, index, builder, context, True)

    elif symbol.symbols[0].name == 'arithmetic-op':
        # +/-
        if symbol.symbols[0].token.value == '-':
            return builder.neg(proc(symbol.symbols[1], builder, context))
        else:
            return proc(symbol.symbols[1], builder, context)

    elif symbol.symbols[0].name == 'logical-op' and symbol.symbols[0].value == '!':
        # !
        val = toBoolean(proc(symbol.symbols[1], builder, context), builder)
        return builder.icmp_signed('==', val, ll.Constant(val.type, 0))

    elif symbol.symbols[0].name == 'bit-op' and symbol.symbols[0].value == '~':
        # ~
        return builder.not_(proc(symbol.symbols[1], builder, context))

    else:
        raise SyntaxError("Not Implemented")

@handler('EXPR-L2')
def proc_expr_l2(symbol: Symbol, builder: Builder, context: Context, proc: Callable):       
    if symbol.symbols[1].name == 'ARG-LIST':
        # Function call
        func = fetchID(symbol.symbols[0].symbols[0].token.value, builder, context, True)
        params = proc(symbol.symbols[1], builder, context)
        casted_params = list()
        for (i, param) in enumerate(params):
            if i < len(func.args):
                # print(param, '===========', func.args[i])
                casted_params.append(builder.bitcast(param, func.args[i].type))
            else:
                casted_params.append(param)

        return builder.call(func, casted_params)
    elif symbol.symbols[1].name == 'bracket':
        # Array element
        i = proc(symbol.symbols[2], builder, context)
        return fetchArrayElem(symbol.symbols[0].symbols[0].token.value, i, builder, context)
    elif symbol.symbols[1].name == 'increment-op':
        # Increment
        lval = symbol.symbols[0]
        if len(lval.symbols) == 1:
            name = lval.symbols[0].symbols[0].token.value
            last = fetchID(name, builder, context)
            dest = fetchID(name, builder, context, True)
        else:
            name = lval.symbols[0].symbols[0].token.value
            index = proc(lval.symbols[2], builder, context)
            last = fetchArrayElem(name, index, builder, context)
            dest = fetchArrayElem(name, index, builder, context, True)
        if symbol.symbols[1].token.value == '++':
            new_val = builder.add(last, ll.Constant(int_type, 1))
        else:
            new_val = builder.sub(last, ll.Constant(int_type, 1))
        builder.store(new_val, dest)
        return last

    raise SyntaxError("Not Implemented")

@handler('ARG-LIST')
def proc_arg_list(symbol: Symbol, builder: Builder, context: Context, proc: Callable):
    if len(symbol.symbols) == 2:
        return tuple()

    return proc(symbol.symbols[1], builder, context)

@handler('ARGS')
def proc_args(symbol: Symbol, builder: Builder, context: Context, proc: Callable):
    return tuple(proc(s, builder, context) for s in symbol.symbols)

@handler('ID')
def proc_id(symbol: Symbol, builder: Builder, context: Context, proc: Callable):
    if len(symbol.symbols) == 1:
        res = proc(symbol.symbols[0], builder, context)
    else:
        res = proc(symbol.symbols[2], builder, context)
    if isinstance(res, str):
        raise SyntaxError(res + " not defined")
    
    return res

@handler('OPERAND')
def proc_operand(symbol: Symbol, builder: Builder, context: Context, proc: Callable):
    if len(symbol.symbols) == 1:
        return proc(symbol.symbols[0], builder, context)
    else:
        return proc(symbol.symbols[1], builder, context)

@handler('id')
def proc_id_lit(symbol: Symbol, builder: Builder, context: Context, proc: Callable):
    return fetchID(symbol.token.value, builder, context)

@handler('int-lit')
def proc_int_lit(symbol: Symbol, builder: Builder, context: Context, proc: Callable):
    return ll.Constant(int_type, int(symbol.token.value))

@handler('str-lit')
def proc_str_lit(symbol: Symbol, builder: Builder, context: Context, proc: Callable):
    msg = eval(symbol.token.value) + '\0'
    msg_const = ll.Constant(ll.ArrayType(ll.IntType(8), len(msg)),
                            bytearray(msg.encode('utf8')))
    msg_global = ll.GlobalVariable(context.module, msg_const.type, str(id(symbol)))
    msg_global.linkage = 'internal'
    msg_global.global_constant = True
    msg_global.initializer = msg_const
    return msg_global

@handler('char-lit')
def proc_char_lit(symbol: Symbol, builder: Builder, context: Context, proc: Callable):
    val = ord(eval(symbol.token.value))
    return ll.Constant(char_type, val)

@handler('true')
def proc_true(symbol: Symbol, builder: Builder, context: Context, proc: Callable):
    return ll.Constant(bool_type, 1)

@handler('false')
def proc_false(symbol: Symbol, builder: Builder, context: Context, proc: Callable):
    return ll.Constant(bool_type, 0)

def fetchID(name: str, builder: Builder, context: Context, ptr: bool = False):
    # Find the identifier in the symbol table
    if name in context.variables:
        res = context.variables[name]['ptr']
        var_type = context.variables[name]['type']
    elif name in context.globals:
        res = context.module.get_global(name)
        var_type = context.globals[name]['type']
    else:
        try:
            # Functions
            return context.module.get_global(name)
        except KeyError:
            raise SyntaxError("ID not found: {}".format(name))

    if var_type.startswith('[') and var_type.endswith(']'):
        # Array
        if ptr:
            raise SyntaxError("Not Implemented")
    else:
        if not ptr:
            res = builder.load(res)
    
    return res

def fetchArrayElem(name: str, index: Any, builder: Builder, context: Context, ptr: bool = False):
    # Find the identifier in the symbol table
    array = fetchID(name, builder, context)
    res = builder.gep(array, (ll.Constant(int_type, 0), index))
    if not ptr:
        res = builder.load(res)
    return res

def toBoolean(val: Any, builder: Builder):
    if val.type == type_dict['char'] or val.type == type_dict['int']:
        return builder.icmp_signed('!=', val, ll.Constant(val.type, 0))
    elif val.type == type_dict['double']:
        return builder.fcmp_ordered('!=', val, ll.Constant(val.type, 0))
    else:
        return val