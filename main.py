import register

register.register('JXJJZX').mainFuc()
"""以 JXJJZX 为前缀遍历 0001 到 0240"""
register.register('JXJJXX', 10, 200).mainFuc()
"""以 JXJJXX 为前缀遍历 0010 到 0200"""
register.register('JXJJZX', 0, 0, 1).mainFuc()
"""以 JXJJZX 为前缀遍历在 result.txt 中出现的帐号"""