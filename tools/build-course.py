"""Build one self-contained HTML file from the editable course sources."""
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
lessons=json.loads((root/'course/lessons.json').read_text())
expanded=json.loads((root/'workbook/expanded-lessons.json').read_text())
for lesson,detail in zip(lessons,expanded):
    lesson['deep']={k:detail[k] for k in ['hands','meaning','start','worked']}
html=(root/'course/shell.html').read_text()+'const lessons='+json.dumps(lessons,ensure_ascii=False)+';\n'+(root/'course/runtime.js').read_text()+'\n</script></body></html>\n'
(root/'Algebra_Adventure.html').write_text(html)
print('Built 12-episode offline course.')
