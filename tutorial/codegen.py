import llvmlite.ir as ll


# Module of the whole program
module = ll.Module('test')
module.triple = ""
builder = ll.IRBuilder()

# Define hello-world message (global variable int8[])
msg = "Hello world!\n\0"
msg_const = ll.Constant(ll.ArrayType(ll.IntType(8), len(msg)),
                        bytearray(msg.encode("utf8")))
msg_global = ll.GlobalVariable(module, msg_const.type, name="msg")
msg_global.linkage = 'internal'
msg_global.global_constant = True
msg_global.initializer = msg_const

# Declare printf
int_type = ll.IntType(32)
char_type = ll.IntType(8)
voidptr_type = ll.PointerType(char_type)
printf_type = ll.FunctionType(int_type, (voidptr_type, ), var_arg=True)
printf = ll.Function(module, printf_type, name="printf")

# Define function main: print hello world for `argc` times
func_type = ll.FunctionType(int_type, 
    (int_type, ll.PointerType(ll.PointerType(char_type))))
func = ll.Function(module, func_type, name='main')

# There are four blocks in the function: entry, condition, loop, end
bb_entry = func.append_basic_block()
bb_cond = func.append_basic_block()
bb_loop = func.append_basic_block()
bb_end = func.append_basic_block()

# Add block entry into builder (an empty block)
builder.position_at_end(bb_entry)
builder.branch(bb_cond)                 # every block should end with `branch`, `cbranch` or `ret`

# Add block cond into builder
builder.position_at_end(bb_cond)

#   if i >= argc: break;
int_i = builder.phi(int_type)              # one variable cannot be assigned twice in LLVM IR, so `phi` is used
int_i.add_incoming(ll.Constant(int_type, 0), bb_entry)    # int i = 0 (initialize)
cond = builder.icmp_signed('<', int_i, func.args[0])
builder.cbranch(cond, bb_loop, bb_end)

# Add block loop into builder
builder.position_at_end(bb_loop)

#    printf(msg);
msg_tmp = builder.bitcast(msg_global, voidptr_type)
builder.call(printf, (msg_tmp, ))

#   i++;
int_next = builder.add(int_i, ll.Constant(int_type, 1))    # int next = i + 1
int_i.add_incoming(int_next, bb_loop)                      # int i = next
builder.branch(bb_cond)

# Add block end into builder
builder.position_at_end(bb_end)

#    return 0;
builder.ret(ll.Constant(func.return_value.type, 0))

print(module)
with open('./test.ll', 'w') as fout:
    print(module, file=fout)
