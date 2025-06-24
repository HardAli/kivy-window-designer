import createwinstate
from models import Frame
from typing import List, Dict

from createwinstate import CreateWinState

IMPOST_THICKNESS = createwinstate.shirina_peregorodok  # ширина перегородки (например, 58 мм)

class WindowCalculator:
    """Класс для расчёта всех перегородок (импостов) в оконной конструкции."""

    def __init__(self, root_frame: Frame):
        self.root = root_frame

    def get_all_imposts(self) -> List[Dict]:
        """
        Возвращает список всех перегородок (импостов) между дочерними фреймами.
        Каждая перегородка содержит:
        - parent_id: ID родительского фрейма
        - index: номер перегородки (между кем и кем)
        - orientation: вертикальная или горизонтальная
        - length: длина перегородки
        - thickness: константная ширина перегородки
        """
        imposts = []
        imposts.append({'length': self.root.width})
        imposts.append({'length': self.root.width})
        imposts.append({'length': self.root.height})
        imposts.append({'length': self.root.height})
        self._traverse_and_collect(self.root, imposts)
        self.root._log_tree_structure()
        self.log_frame_sizes(self.root)
        return imposts

    def _traverse_and_collect(self, frame: Frame, imposts: List[Dict]):
        if len(frame.child) > 1:
            print(f'\n\n\n\n {len(frame.child)}   {frame.orientation}   {frame.frame_id}\n\n\n\n')
            orientation = 'vertical' if frame.orientation == 'horizontal' else 'horizontal'
            if frame.orientation == 'horizontal':
                length = frame.height
            elif frame.orientation == 'vertical':
                length = frame.width

            for i in range(len(frame.child) - 1):
                imposts.append({
                    'length': length
                    # 'parent_id': frame.frame_id,
                    # 'index': i,
                    # 'orientation': orientation,
                    # 'thickness': IMPOST_THICKNESS
                })

        for child in frame.child:
            self._traverse_and_collect(child, imposts)

    def log_frame_sizes(self, frame: Frame, level=0):
        indent = "  " * level
        print(f"{indent}Frame {frame.frame_id} | size = ({frame.width} x {frame.height})")
        for child in frame.child:
            self.log_frame_sizes(child, level + 1)

