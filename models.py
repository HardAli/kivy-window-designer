from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List
from kivy.uix.widget import Widget
from arrowwidget import ArrowWidget




@dataclass
class Frame:
    frame_id: int
    parent: Optional[Frame]
    layout: Widget
    width: int = 100
    height: int = 100
    child: List[Frame] = field(default_factory=list)
    main_frame: bool = False
    manual_set_parametr_w: bool = False
    manual_set_parametr_h: bool = False
    orientation: str = 'horizontal'
    arrow_widget: ArrowWidget = ArrowWidget('deaf')

    def __repr__(self):
        child_ids = [c.frame_id for c in self.child]
        return (f"Frame(id={self.frame_id}, size=({self.width}x{self.height}), "
                f"children={child_ids}, manual_w={self.manual_set_parametr_w})")

    def get_brother(self):
        if self.main_frame or not self.parent:
            print('⚠ Это main_frame или нет родителя — братьев нет')
            return []
        return [child for child in self.parent.child if child is not self]

        brothers.remove(my_frame)
        return brothers

    def to_dict(self):
        return {
            'frame_id': self.frame_id,
            'width': self.width,
            'height': self.height,
            'parent_id': self.parent.frame_id if self.parent else None,
            'child_ids': [c.frame_id for c in self.child]
        }

    def recalculate_frames(self):
        """Рекурсивно пересчитывает размеры всех дочерних фреймов."""
        parent_width, parent_height = self.width, self.height
        if len(self.child) == 1:
            self.child[0].width = parent_width
            self.child[0].height = parent_height
        elif not len(self.child):
            return None

        fixed_total_w = sum(child.width for child in self.child if child.manual_set_parametr_w)
        fixed_total_h = sum(child.height for child in self.child if child.manual_set_parametr_h)



    def recalculate_dimensions(self) -> None:
        """Рекурсивно пересчитывает размеры всех дочерних фреймов."""
        print(f'frame_id: {self.frame_id}, {self}')
        dimension = 'width' if self.orientation == 'horizontal' else 'height'
        manual_attr = 'manual_set_parametr_w' if dimension == 'width' else 'manual_set_parametr_h'
        parent_size = getattr(self, dimension)
        print(f'parent_size: {parent_size}')

        # Считаем сумму фиксированных значений
        fixed_total = sum(
            getattr(child, dimension)
            for child in self.child
            if getattr(child, manual_attr)
        )

        # Список масштабируемых детей
        scalable_children = [child for child in self.child if not getattr(child, manual_attr)]
        num_scalable = len(scalable_children)
        remaining = parent_size - fixed_total

        if remaining < 0:
            print(f"⚠ Ошибка: фиксированные дети больше родителя (frame_id={self.frame_id})")
            return

        # Новый размер для масштабируемых детей
        per_child_size = remaining // num_scalable if num_scalable else parent_size

        # Установка новых размеров
        for child in self.child:
            if not getattr(child, manual_attr):
                setattr(child, dimension, per_child_size)

        # Рекурсивный спуск к детям
        for child in self.child:
            child.recalculate_dimensions()

    def update_layouts_size_hint(self):
        branch = [*self.parent.child]
        pw = self.parent.width
        ph = self.parent.height

        if pw == 0 and ph == 0:
            print("error Размер родителя недопустим")
            return

        for frame in branch:
            layout = frame.layout
            if not layout or not layout.parent:
                continue

            layout.size_hint_x = frame.width / pw
            layout.size_hint_y = frame.height / ph

            print(layout.size_hint_x, layout.size_hint_y, frame.frame_id)

            # Перерисовываем
        if self.parent.layout:
            self.parent.layout.do_layout()

    def _log_tree_structure(self, level: int = 0) -> None:
        indent = "    " * level
        manual_w = "🔒" if getattr(self, "manual_set_parametr_w", False) else "🔓"
        manual_h = "🔒" if getattr(self, "manual_set_parametr_h", False) else "🔓"

        print(f"{indent}📦 Frame {self.frame_id} | width: {self.width} {manual_w} | height: {self.height} {manual_h}"
              f" | orient = {self.orientation}")

        for child in self.child:
            child._log_tree_structure(level + 1)

    def update_width(self, new_width: int) -> None:
        self._update_dimension(
            new_value=new_width,
            current_value=self.width,
            dimension='width',
            manual_attr='manual_set_parametr_w',
        )

    def update_height(self, new_height: int) -> None:
        self._update_dimension(
            new_value=new_height,
            current_value=self.height,
            dimension='height',
            manual_attr='manual_set_parametr_h',
        )

    def _update_dimension(self, new_value: int, current_value: int, dimension: str, manual_attr: str) -> None:
        print(f"\n🔧 Обработка фрейма {self.frame_id} | dimension = {dimension}")
        print(f"▶ Родительский размер: {new_value}")

        if new_value <= 0:
            print(f"❌ Ошибка: новое значение {dimension} недопустимо ({new_value})")
            return

        setattr(self, dimension, new_value)

        # Считаем сумму фиксированных значений
        fixed_total = 0
        for child in self.child:
            if getattr(child, manual_attr):
                fixed_size = getattr(child, dimension)
                print(f"   🔒 фиксированный ребёнок {child.frame_id}: {dimension} = {fixed_size}")
                fixed_total += fixed_size

        # Определяем количество дитей повернутых не в ту сторону
        minus_num_scalable = 0
        for child in self.child:
            if not getattr(child, manual_attr):
                if dimension == 'width' and child.orientation == 'vertical':
                    minus_num_scalable += 1
                elif dimension == 'height' and child.orientation == 'horizontal':
                    minus_num_scalable += 1

        # Определяем масштабируемых детей
        scalable_children = [child for child in self.child if not getattr(child, manual_attr)]
        num_scalable = len(scalable_children)
        num_scalable = num_scalable - minus_num_scalable if num_scalable != minus_num_scalable else 1
        remaining = new_value - fixed_total



        print(f"📦 Сумма фиксированных значений: {fixed_total}")
        print(f"📐 Оставшееся пространство: {remaining} | количество масштабируемых детей: {num_scalable}")

        if remaining < 0:
            print(f"❌ Ошибка: фиксированные значения превышают родительский размер ({fixed_total} > {new_value})")
            return

        per_child_size = remaining // num_scalable if num_scalable else 0
        print(f"🧮 Назначаемый размер для автоматических детей: {per_child_size}")

        # Присваиваем размеры и вызываем рекурсивное обновление
        for child in self.child:
            is_manual = getattr(child, manual_attr)
            target_size = getattr(child, dimension) if is_manual else per_child_size

            setattr(child, dimension, target_size)
            update_method = getattr(child, f"update_{dimension}")
            print(f"↪ Установка {dimension} = {target_size} для ребенка {child.frame_id} | manual = {is_manual}")
            update_method(target_size)





