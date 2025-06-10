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

    def to_dict(self):
        return {
            'frame_id': self.frame_id,
            'width': self.width,
            'height': self.height,
            'parent_id': self.parent.frame_id if self.parent else None,
            'child_ids': [c.frame_id for c in self.child]
        }
