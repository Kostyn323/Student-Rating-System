import csv
import os
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


class RatingSystem:
    def __init__(self, filename='data.csv'):
        self.filename = filename
        self.students = []
        self.weights = {
            'Math': 1.5, 'English': 1.0, 'Bjd': 0.5, 'Russian': 0.5,
            'Python': 2.5, 'Java': 2.5, 'Evm': 2.0, 'Database': 2.0
        }

        self.semesters = {
            '1': {'name': '1-й семестр', 'start': datetime(2025, 9, 1), 'end': datetime(2026, 1, 25)},
            '2': {'name': '2-й семестр', 'start': datetime(2026, 2, 15), 'end': datetime(2026, 5, 25)}
        }
        self.all_period = {
            'start': min(s['start'] for s in self.semesters.values()),
            'end': max(s['end'] for s in self.semesters.values())
        }

        self.load_from_csv()

    def load_from_csv(self):
        try:
            with open(self.filename, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.students = []
                for row in reader:
                    if 'Name' not in row or 'Date' not in row:
                        continue
                    row['Grade'] = float(row['Grade'])
                    row['Semester'] = int(row['Semester'])
                    row['Date'] = datetime.strptime(row['Date'], '%Y-%m-%d')
                    self.students.append(row)
        except Exception as e:
            print(f"Ошибка при загрузке файла: {e}. Файл будет сброшен.")
            self.students = []

    def save_to_csv(self):
        with open(self.filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['Name', 'Subject', 'Grade', 'Semester', 'Date'])
            writer.writeheader()
            for s in self.students:
                row = s.copy()
                row['Date'] = s['Date'].strftime('%Y-%m-%d')
                writer.writerow(row)

    def _select_from_list(self, items, prompt):
        items = sorted(list(set(items)))
        error_msg = ""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            if error_msg:
                print(error_msg)
                error_msg = ""

            print(f"\nВыберите {prompt}:")
            for i, item in enumerate(items, 1):
                print(f"{i}. {item}")
            print("0. Ввести вручную")
            print("Введите 'exit' для отмены операции")

            user_input = input("----------------------------\nВаш выбор: ").strip()
            if user_input.lower() == 'exit':
                return 'exit'

            try:
                choice = int(user_input)
                if 0 < choice <= len(items):
                    return items[choice - 1]
                elif choice == 0:
                    manual_input = input(f"Введите {prompt} вручную: ").strip()
                    if manual_input.lower() == 'exit':
                        return 'exit'
                    return manual_input
                else:
                    error_msg = "----------------------------\nОшибка: выбран номер вне списка"
            except ValueError:
                error_msg = "----------------------------\nОшибка: введите число или 'exit'"

    def add_grade(self):
        names = {s['Name'] for s in self.students}
        subjects = {s['Subject'] for s in self.students}

        name = self._select_from_list(names, "студента")
        if name == 'exit': print("----------------------------"); return

        subject = self._select_from_list(subjects, "предмет")
        if subject == 'exit': print("----------------------------"); return

        # валидация оценки
        error_msg = ""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            if error_msg: print(error_msg)
            print(f"\nВыбранный студент: {name}\nВыбранный предмет: {subject}\n")

            user_input = input("Оценка (2-5) или 'exit': ").strip()
            if user_input.lower() == 'exit': print("----------------------------"); return
            try:
                grade = float(user_input)
                if 2 <= grade <= 5:
                    break
                error_msg = "-----------------------------\nОшибка: оценка должна быть в диапазоне от 2 до 5"
            except ValueError:
                error_msg = "-----------------------------\nОшибка: введите числовое значение"

        # валидация семестра
        error_msg = ""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            if error_msg: print(error_msg)
            print(f"\nВыбранный студент: {name}\nВыбранный предмет: {subject}\nОценка: {grade}\n")

            sem_choice = input("Семестр (1 или 2) или 'exit': ").strip()
            if sem_choice.lower() == 'exit': print("----------------------------"); return
            if sem_choice in self.semesters:
                break
            error_msg = "--------------------------\nОшибка: выберите 1 или 2 семестр"

        start, end = self.semesters[sem_choice]['start'], self.semesters[sem_choice]['end']

        # валидация даты
        error_msg = ""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            if error_msg: print(error_msg)
            print(f"\nВыбранный студент: {name}\nВыбранный предмет: {subject}\nОценка: {grade}\nСеместр: {sem_choice}\n")

            try:
                date_str = input(
                    f"Дата ({sem_choice} семестр, {start.strftime('%Y-%m-%d')} - {end.strftime('%Y-%m-%d')}) или 'exit': ").strip()
                if date_str.lower() == 'exit': print("----------------------------"); return
                date = datetime.strptime(date_str, '%Y-%m-%d')
                if start <= date <= end:
                    break
                error_msg = "------------------------------\nОшибка: Дата вне диапазона текущего семестра"
            except ValueError:
                error_msg = "------------------------------\nОшибка формата. Используйте ГГГГ-ММ-ДД"

        self.students.append(
            {'Name': name, 'Subject': subject, 'Grade': grade, 'Semester': int(sem_choice), 'Date': date})
        self.save_to_csv()
        print("\nЗапись успешно добавлена")
        input("\nНажмите Enter...")

    def view_all_grades(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        if not self.students:
            print("\nБаза данных пуста")
            input("\nНажмите Enter...")
            return
        print(f"\n{'Имя':<15} | {'Предмет':<10} | {'Оценка':<6} | {'Семестр':<7} | {'Дата':<10}")
        print("-" * 65)
        for s in self.students:
            print(
                f"{s['Name']:<15} | {s['Subject']:<10} | {s['Grade']:<6.1f} | {s['Semester']:<7} | {s['Date'].strftime('%Y-%m-%d')}")
        input("\nНажмите Enter...")

    def edit_grade(self):
        error_msg = ""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            names = sorted(list({s['Name'] for s in self.students}))
            if not names:
                print("\nСписок студентов пуст")
                input("\nНажмите Enter...")
                return

            if error_msg: print(error_msg)
            print("\nВыберите студента для редактирования:")
            for i, name in enumerate(names, 1):
                print(f"{i}. {name}")
            print("0. Выйти в меню")

            user_input = input("----------------------------\nВаш выбор: ").strip()
            if user_input == '0': print("----------------------------"); return
            try:
                choice = int(user_input) - 1
                if 0 <= choice < len(names):
                    selected_name = names[choice]
                    break
                error_msg = "----------------------------\nОшибка: номер вне списка"
            except ValueError:
                error_msg = "----------------------------\nОшибка: введите номер или 0 для выхода"

        records = [i for i, s in enumerate(self.students) if s['Name'] == selected_name]

        # выбор ID записи
        error_msg = ""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            if error_msg: print(error_msg)
            print(f"\nОценки студента {selected_name}:")
            for i in records:
                s = self.students[i]
                print(f"[{i}] {s['Subject']} - {s['Grade']} ({s['Date'].strftime('%Y-%m-%d')})")
            print("\nДля отмены введите 'exit'")

            user_input = input("----------------------------\nВведите ID записи для изменения: ").strip()
            if user_input.lower() == 'exit': print("----------------------------"); return
            try:
                idx = int(user_input)
                if idx in records:
                    break
                error_msg = "\n----------------------------\nОшибка: этот ID не принадлежит выбранному студенту"
            except ValueError:
                error_msg = "\n----------------------------\nОшибка: введите числовой ID"

        # изменение оценки
        error_msg = ""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            if error_msg: print(error_msg)
            print(f"\nРедактирование записи [{idx}]: {self.students[idx]['Subject']} для {selected_name}")

            user_input = input(f"Новая оценка (2-5) или 'exit': ").strip()
            if user_input.lower() == 'exit': print("----------------------------"); return
            try:
                new_grade = float(user_input)
                if 2 <= new_grade <= 5:
                    self.students[idx]['Grade'] = new_grade
                    self.save_to_csv()
                    print("\nОценка успешно изменена")
                    break
                error_msg = "----------------------------\nОшибка: оценка должна быть в диапазоне 2-5"
            except ValueError:
                error_msg = "----------------------------\nОшибка: введите число"
        input("\nНажмите Enter...")

    def calculate_student_rating(self, name):
        s_data = [s for s in self.students if s['Name'] == name]
        return self._calculate_rating_from_list(s_data)

    def _calculate_rating_from_list(self, data_list):
        subjects = {s['Subject'] for s in data_list}
        w_sum = sum((sum(s['Grade'] for s in data_list if s['Subject'] == sub) / len(
            [s for s in data_list if s['Subject'] == sub])) * self.weights.get(sub, 1.0) for sub in subjects)
        w_total = sum(self.weights.get(sub, 1.0) for sub in subjects)
        return round(w_sum / w_total, 2) if w_total > 0 else 0

    def show_rankings(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        names = list({s['Name'] for s in self.students})
        if not names:
            print("\nНет данных для формирования рейтинга")
            input("\nНажмите Enter...")
            return
        ranked = sorted([{'Name': n, 'Score': self.calculate_student_rating(n)} for n in names],
                        key=lambda x: x['Score'], reverse=True)
        print("\n--- Рейтинг ---")
        for i, r in enumerate(ranked, 1):
            print(f"{i}. {r['Name']} — {r['Score']}")
        input("\nНажмите Enter...")

    def show_student_summary(self):
        error_msg = ""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            names = sorted(list({s['Name'] for s in self.students}))
            if not names:
                print("\nСписок студентов пуст.")
                input("\nНажмите Enter...")
                return

            if error_msg: print(error_msg)
            print("\nВыберите студента для просмотра сводки:")
            for i, name in enumerate(names, 1):
                print(f"{i}. {name}")
            print("0. Выйти в меню")

            user_input = input("Выбор студента: ").strip()
            if user_input == '0': print("----------------------------"); return
            try:
                choice = int(user_input) - 1
                if 0 <= choice < len(names):
                    name = names[choice]
                    break
                error_msg = "----------------------------\nОшибка: номер вне списка"
            except ValueError:
                error_msg = "----------------------------\nОшибка: введите число"

        os.system('cls' if os.name == 'nt' else 'clear')
        s_data = [s for s in self.students if s['Name'] == name]
        print(f"\nСводка по {name}: Общий рейтинг {self.calculate_student_rating(name)}")
        print("-" * 30)
        for sub in sorted({s['Subject'] for s in s_data}):
            grades = [s['Grade'] for s in s_data if s['Subject'] == sub]
            print(f"{sub:<15} | Средний балл: {sum(grades) / len(grades):.1f}")
        input("\nНажмите Enter...")

    def compare_students(self):
        error_msg = ""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            names = sorted(list({s['Name'] for s in self.students}))
            if not names:
                print("\nНет студентов для сравнения")
                input("\nНажмите Enter...")
                return

            if error_msg: print(error_msg)
            print("\nДоступные студенты:")
            for i, n in enumerate(names, 1):
                print(f"{i}. {n}")
            print("Введите 'exit' для отмены операции")

            user_input = input("Выберите номера (через запятую): ").strip()
            if 'exit' in user_input.lower(): print("----------------------------"); return
            try:
                choices = [int(c.strip()) - 1 for c in user_input.split(',')]
                selected = [names[c] for c in choices if 0 <= c < len(names)]
                if selected:
                    break
                error_msg = "----------------------------\nОшибка: не выбрано ни одного существующего номера"
            except ValueError:
                error_msg = "----------------------------\nОшибка: введите корректные номера через запятую"

        os.system('cls' if os.name == 'nt' else 'clear')
        all_subs = sorted(list({s['Subject'] for s in self.students}))
        header = f"\n{'Студент':<15} | {'Рейтинг':<8} | " + " | ".join([f"{sub:<10}" for sub in all_subs])
        print(header)
        print("-" * len(header))

        for name in selected:
            row = [f"{name:<15}", f"{self.calculate_student_rating(name):<8}"]
            for sub in all_subs:
                grades = [s['Grade'] for s in self.students if s['Name'] == name and s['Subject'] == sub]
                row.append(f"{sum(grades) / len(grades):<10.1f}" if grades else f"{'0.0':<10}")
            print(" | ".join(row))
        input("\nНажмите Enter...")

    def show_problematic_subjects(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n--- Проблемные предметы (< 3.5) ---")
        found = False
        for sub in {s['Subject'] for s in self.students}:
            grades = [s['Grade'] for s in self.students if s['Subject'] == sub]
            avg = sum(grades) / len(grades)
            if avg < 3.5:
                print(f"{sub}: {round(avg, 2)}")
                found = True
        if not found:
            print("Проблемных предметов нет. Все средние показатели выше 3.5")
        input("\nНажмите Enter...")

    def show_dynamics(self):
        error_msg = ""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            names = sorted(list({s['Name'] for s in self.students}))
            if not names:
                print("----------------------------\nНет данных для графика")
                input("\nНажмите Enter...")
                print("----------------------------")
                return

            if error_msg: print(error_msg)
            print("\nВыберите студентов для графика (через запятую):")
            for i, name in enumerate(names, 1):
                print(f"{i}. {name}")
            print("0. Все")
            print("Для отмены введите 'exit'")

            user_input = input("Ваш выбор: ").strip()
            if 'exit' in user_input.lower(): print("----------------------------"); return

            choices = [c.strip() for c in user_input.split(',')]
            if '0' in choices:
                selected = names
                break
            else:
                selected = []
                for c in choices:
                    if c.isdigit():
                        idx = int(c) - 1
                        if 0 <= idx < len(names):
                            selected.append(names[idx])
                if selected:
                    break
                error_msg = "----------------------------\nОшибка: неверный выбор студентов. Повторите ввод."

        # выбор периода
        error_msg = ""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            if error_msg: print(error_msg)
            print("\nВыберите период для отображения динамики:")
            print(
                f"0. Весь период ({self.all_period['start'].strftime('%Y-%m-%d')} — {self.all_period['end'].strftime('%Y-%m-%d')})")
            for k, v in self.semesters.items():
                print(f"{k}. {v['name']} ({v['start'].strftime('%Y-%m-%d')} — {v['end'].strftime('%Y-%m-%d')})")
            print(f"3. Произвольный период (Границы: {self.all_period['start'].strftime('%Y-%m-%d')} — {self.all_period['end'].strftime('%Y-%m-%d')})")
            print("00. Назад в меню")

            choice = input("Ваш выбор: ").strip()
            if choice == '00': print("----------------------------"); return

            if choice in self.semesters:
                start_date, end_date = self.semesters[choice]['start'], self.semesters[choice]['end']
                break
            elif choice == '0':
                start_date, end_date = self.all_period['start'], self.all_period['end']
                break
            elif choice == '3':
                try:
                    start_input = input("Начало (ГГГГ-ММ-ДД): ").strip()
                    end_input = input("Конец (ГГГГ-ММ-ДД): ").strip()
                    start_date = datetime.strptime(start_input, '%Y-%m-%d')
                    end_date = datetime.strptime(end_input, '%Y-%m-%d')

                    if start_date < self.all_period['start'] or end_date > self.all_period['end']:
                        error_msg = f"----------------------------\nОшибка: даты должны быть строго в границах учебного процесса {self.all_period['start'].strftime('%Y-%m-%d')} — {self.all_period['end'].strftime('%Y-%m-%d')}"
                        continue
                    if start_date > end_date:
                        error_msg = "----------------------------\nОшибка: Дата начала не может быть позже даты конца"
                        continue
                    break
                except ValueError:
                    error_msg = "----------------------------\nОшибка формата даты. Используйте шаблон ГГГГ-ММ-ДД."
            else:
                error_msg = "----------------------------\nНекорректный выбор пункта меню"

        plt.figure(figsize=(12, 6))
        graph_built = False

        for name in selected:
            data = sorted([s for s in self.students if s['Name'] == name and start_date <= s['Date'] <= end_date],
                          key=lambda x: x['Date'])
            if not data: continue

            graph_built = True
            agg_dates, agg_ratings, curr = [], [], data[0]['Date']
            while curr <= data[-1]['Date']:
                subset = [s for s in data if s['Date'] <= curr]
                if subset:
                    agg_dates.append(curr)
                    agg_ratings.append(self._calculate_rating_from_list(subset))
                curr += timedelta(days=10)
            plt.plot(agg_dates, agg_ratings, marker='o', label=name, markersize=4)

        if not graph_built:
            print("\nЗа выбранный период времени нет оценок у указанных студентов")
            input("\nНажмите Enter...")
            return

        plt.title("Динамика рейтинга студентов")
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.show()

    def export_ratings(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        names = list({s['Name'] for s in self.students})
        if not names:
            print("Нет данных для экспорта")
            input("\nНажмите Enter...")
            return
        ranked = sorted([{'Name': n, 'Score': self.calculate_student_rating(n)} for n in names],
                        key=lambda x: x['Score'], reverse=True)
        try:
            with open('rating_report.csv', 'w', newline='', encoding='utf-8') as f:
                w = csv.DictWriter(f, fieldnames=['Rank', 'Name', 'Score'])
                w.writeheader()
                for i, r in enumerate(ranked, 1):
                    w.writerow({'Rank': i, 'Name': r['Name'], 'Score': r['Score']})
            print("Данные успешно сохранены в файл 'rating_report.csv'")
        except Exception as e:
            print(f"----------------------------\nОшибка при записи файла: {e}")
        input("\nНажмите Enter...")


def main():
    rs = RatingSystem()
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=====     Меню     =====")
        print("1. Добавить | 2. Список | 3. Редактировать | 4. Рейтинг | 5. Сводка | 6. Сравнение | 7. Проблемы | 8. Динамика | 9. Экспорт | 10. Выход")
        choice = input("Выбор: ").strip()
        if choice == '1':
            rs.add_grade()
        elif choice == '2':
            rs.view_all_grades()
        elif choice == '3':
            rs.edit_grade()
        elif choice == '4':
            rs.show_rankings()
        elif choice == '5':
            rs.show_student_summary()
        elif choice == '6':
            rs.compare_students()
        elif choice == '7':
            rs.show_problematic_subjects()
        elif choice == '8':
            rs.show_dynamics()
        elif choice == '9':
            rs.export_ratings()
        elif choice == '10':
            break


if __name__ == '__main__':
    main()
