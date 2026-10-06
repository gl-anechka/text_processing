import re
import time

# генерация регулярки
def build_reg(depth):
    if depth == 0:
        return ''
    
    # учитываем вложенность скобок
    nested = build_reg(depth-1)
    bracket = (r'(?:\(' + nested + r'\)' + r'|\[' + nested + r'\]' + r'|\{' + nested + r'\}' + r')')

    # учитываем соседство скобок
    return r'(?:' + bracket + r')*'

# итоговая регулярка (добавлены начало и конец строки)
def build_reg_final(depth):
    return r'\A' + build_reg(depth) + r'\Z'

# время выполнения на большой строке
start = time.time()
regexp = re.compile(build_reg_final(10))
st = '([{([{([{()}])}])}])'*250
res = re.findall(regexp, st)
t = time.time() - start

print(bool(res), t)
