from src.char.CharSkillButton import is_float
from src.char.BaseChar import BaseChar
from src.char.Fei import Fei

char_dict = {
        'char_Fei': {'cls': Fei, 'res_cd': 12, 'echo_cd': 25},
    }

char_names = char_dict.keys()

def get_char_by_pos(task, box, index, old_char):
    highest_confidence = 0
    info = None
    name = "unknown"
    char = None
    if old_char and old_char.char_name in char_names:
        char = task.find_one(old_char.char_name, box=box, threshold=0.6)
        if char:
            return old_char

    if not char:
        char = task.find_best_match_in_box(box, char_names, threshold=0.6)
        if char:
            info = char_dict.get(char.name)
            name = char.name
            cls = info.get('cls')
            return cls(task, index, info.get('res_cd'), info.get('echo_cd'), info.get('liberation_cd') or 25,
                       char_name=name)
    task.log_info(f'could not find char {info} {highest_confidence}')
    if old_char:
        return old_char
    has_cd = task.ocr(box=box)
    if has_cd and is_float(has_cd[0].name):
        task.log_info(f'found char {has_cd[0]} wait and reload')
        task.next_frame()
        return get_char_by_pos(task, box, index, old_char)
    if task.debug:
        task.screenshot(f'could not find char {index}')
    return BaseChar(task, index, char_name=name)
