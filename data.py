from peewee import SqliteDatabase, Model, CharField, IntegerField, ForeignKeyField

# Настройки базы данных
DB_NAME = "materials.db"
db = SqliteDatabase(DB_NAME)


class BaseModel(Model):
    """Базовая модель с общими настройками."""
    class Meta:
        database = db


class Category(BaseModel):
    """Модель категории материалов."""
    name = CharField(unique=True)

    def __str__(self):
        return f"Category(id={self.id}, name='{self.name}')"


class Material(BaseModel):
    """Модель материалов."""
    code = CharField(unique=True)
    name = CharField()
    price = IntegerField()
    category = ForeignKeyField(Category, backref="materials", on_delete="CASCADE")

    def __str__(self):
        return f"Material(id={self.id}, code='{self.code}', name='{self.name}', price={self.price}, category='{self.category.name}')"


class DatabaseManager:
    """Класс для управления базой данных."""

    def __init__(self):
        """Инициализация базы данных."""
        db.connect()
        db.create_tables([Category, Material], safe=True)

    def add_category(self, name: str, materials: list = []) -> Category:
        """Добавляет новую категорию. Если передан список материалов, они тоже добавляются."""
        category, created = Category.get_or_create(name=name)

        for material in materials:
            self.add_material(material["code"], material["name"], material["price"], category.name)

        return category

    def add_material(self, code: str, name: str, price: int, category_name: str) -> Material:
        """Добавляет новый материал в указанную категорию."""
        category = self.add_category(category_name)  # Если категории нет, она создастся
        material, created = Material.get_or_create(code=code, defaults={"name": name, "price": price, "category": category})
        if not created:
            material.name = name
            material.price = price
            material.category = category
            material.save()
        return material

    def delete_category(self, name: str) -> bool:
        """Удаляет категорию и все её материалы."""
        try:
            category = Category.get(Category.name == name)
            category.delete_instance(recursive=True)  # Удаляет категорию и все материалы
            return True
        except Category.DoesNotExist:
            return False

    def delete_material(self, code: str) -> bool:
        """Удаляет материал по его коду."""
        try:
            material = Material.get(Material.code == code)
            material.delete_instance()
            return True
        except Material.DoesNotExist:
            return False

    def update_material(self, code: str, name: str = None, price: int = None, category_name: str = None) -> bool:
        """Обновляет данные материала."""
        try:
            material = Material.get(Material.code == code)
            if name:
                material.name = name
            if price:
                material.price = price
            if category_name:
                material.category = self.add_category(category_name)
            material.save()
            return True
        except Material.DoesNotExist:
            return False

    def get_all_categories(self) -> list:
        """Возвращает список всех категорий."""
        return [category.name for category in Category.select()]

    def get_all_materials(self) -> list:
        """Возвращает список всех материалов."""
        return [str(material) for material in Material.select()]

    def get_materials_by_category(self, category_name: str) -> list:
        """Возвращает список всех материалов в указанной категории."""
        try:
            category = Category.get(Category.name == category_name)
            return [str(material) for material in category.materials]
        except Category.DoesNotExist:
            return []  # Если категории нет, возвращаем пустой список

    def search_material_by_code(self, code: str) -> str:
        """Ищет материал по коду."""
        try:
            material = Material.get(Material.code == code)
            return str(material)
        except Material.DoesNotExist:
            return "Материал не найден"

    def search_material_by_name(self, name: str) -> list:
        """Ищет материалы по имени (частичный поиск)."""
        return [str(material) for material in Material.select().where(Material.name.contains(name))]

    def calculate_total_cost(self) -> int:
        """Возвращает общую стоимость всех материалов."""
        return sum(material.price for material in Material.select())

    def close(self):
        """Закрывает соединение с базой данных."""
        db.close()


# --- Пример использования ---
if __name__ == "__main__":
    db_manager = DatabaseManager()

    # Добавляем категории с материалами
    db_manager.add_category("Ручка", [
        {"code": "HND-001", "name": "Деревянная ручка", "price": 150},
        {"code": "HND-002", "name": "Металлическая ручка", "price": 250},
        {"code": "HND-003", "name": "Пластиковая ручка", "price": 100}
    ])

    db_manager.add_category("Стекло", [
        {"code": "GLS-001", "name": "Закаленное стекло", "price": 500},
        {"code": "GLS-002", "name": "Обычное стекло", "price": 300}
    ])

    # Вывод всех категорий
    print("\n📂 Все категории:")
    print(db_manager.get_all_categories())

    # Вывод всех материалов
    print("\n📦 Все материалы:")
    print(db_manager.get_all_materials())

    # Поиск материала по коду
    print("\n🔍 Поиск материала по коду 'HND-002':")
    print(db_manager.search_material_by_code("HND-002"))

    # Поиск материалов по имени
    print("\n🔎 Поиск материалов по имени 'ручка':")
    print(db_manager.search_material_by_name("ручка"))

    # Общая стоимость всех материалов
    print("\n💰 Общая стоимость всех материалов:")
    print(db_manager.calculate_total_cost())

    # Удаление материала
    db_manager.delete_material("HND-003")

    # Удаление категории
    db_manager.delete_category("Стекло")

    # Вывод всех материалов после удаления
    print("\n📦 Все материалы после удаления:")
    print(db_manager.get_all_materials())

    db_manager.close()
