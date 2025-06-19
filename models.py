from dataclasses import dataclass, field
from typing import Optional, List
from kivy.uix.widget import Widget


@dataclass
class Frame:
    frame_id: int
    width: int
    height: int
    parent: Optional['Frame']
    layout: Widget
    child: List['Frame'] = field(default_factory=list)
    main_frame: bool = False
    manual_set_parametrs: bool = False
    orientation: str = 'horizontal'

    def __repr__(self):
        return f"id={self.frame_id} sz={self.width}x{self.height} orientation = {self.orientation}"

    def to_dict(self):
        return {
            'frame_id': self.frame_id,
            'width': self.width,
            'height': self.height,
            'parent_id': self.parent.frame_id if self.parent else None,
            'child_ids': [c.frame_id for c in self.child]
        }

    def get_new_true_size(self):
        pass
