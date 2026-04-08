import re

with open('md_to_image_hermes.py', 'r') as f:
    content = f.read()

lines = content.split('\n')
result = []
for line in lines:
    has_chinese_quote = '\u201c' in line or '\u201d' in line
    is_render_call = line.strip().startswith(('r.render_', 'r.y '))
    
    if has_chinese_quote and is_render_call:
        m = re.match(r'^(\s*r\.\w+\(\s*)(")(.*)(\)\s*)$', line, re.DOTALL)
        if m and ('\u201c' in m.group(3) or '\u201d' in m.group(3)):
            prefix = m.group(1)
            body = m.group(3)
            suffix = m.group(4)
            new_line = prefix + "'" + body + "'" + suffix
            print(f'  Fixed: {new_line[:100]}')
            result.append(new_line)
        else:
            result.append(line)
    else:
        result.append(line)

with open('md_to_image_hermes.py', 'w') as f:
    f.write('\n'.join(result))
print('Done')
