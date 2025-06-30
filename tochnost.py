import re
from collections import defaultdict
from statistics import mean
from typing import List, Dict


class ChessGameAnalyzer:
    def __init__(self, file_path: str):
        self.games = []
        self._parse_file(file_path)

    def _parse_file(self, file_path: str) -> None:
        pattern = re.compile(r"(https?://\S+)\s+Турнир:\s+(.*?)\s+(\d{4})[^\d]*([\d.]+)", re.UNICODE)
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                match = pattern.search(line)
                if match:
                    url, tournament, year, accuracy = match.groups()
                    self.games.append({
                        'url': url.strip(),
                        'tournament': tournament.strip(),
                        'year': int(year),
                        'accuracy': float(accuracy)
                    })

    def get_all_accuracies(self) -> List[float]:
        return [game['accuracy'] for game in self.games]

    def get_average_accuracy(self) -> float:
        accuracies = self.get_all_accuracies()
        return round(mean(accuracies), 2) if accuracies else 0.0

    def get_average_accuracy_by_tournament(self) -> Dict[str, float]:
        tournament_map = defaultdict(list)
        for game in self.games:
            tournament_map[game['tournament']].append(game['accuracy'])

        return {
            tournament: round(mean(accs), 2)
            for tournament, accs in tournament_map.items()
        }

    def get_average_accuracy_by_year(self) -> Dict[int, Dict[str, float | int]]:
        year_map = defaultdict(list)
        for game in self.games:
            year_map[game['year']].append(game['accuracy'])

        return {
            year: {
                'Средняя точьность': round(mean(accs), 2),
                'Количество игр': len(accs)
            }
            for year, accs in year_map.items()
        }

    def print_summary(self) -> None:
        print(f"📌 Средняя точность за все матчи: {self.get_average_accuracy()}")

        print("\n📊 Средняя точность по турнирам:")
        for tournament, acc in self.get_average_accuracy_by_tournament().items():
            print(f"— {tournament}: {acc}")

        print("\n📆 Средняя точность по годам:")
        for year, acc in sorted(self.get_average_accuracy_by_year().items()):
            print(f"— {year}: {acc}")


if __name__ == "__main__":
    analyzer = ChessGameAnalyzer("prov.txt")
    analyzer.print_summary()

    # Получить список всех точностей
    all_accuracies = analyzer.get_all_accuracies()
    print("\n📈 Все точности:", all_accuracies)

    summ = 0
    for i in all_accuracies:
        summ += float(i)

    print(f'\n\n srednyi {summ / len(all_accuracies) , print(len(all_accuracies))}')
