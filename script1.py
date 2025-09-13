# Поиск служб RKeeper и определение их версий
import psutil
import os
import subprocess
import json
from pathlib import Path

print('=== Поиск служб RKeeper и дополнительных служб ===')

# Список искомых служб
target_services = ['RKeeperRefServer', 'rkDExchSrv', 'RKeeperMidServer', 'Sdbsrv64', 'Transport', 'WsAgent']
found_services = {}

# Получаем список всех служб
for service in psutil.win_service_iter():
    service_name = service.name()
    
    # Проверяем, начинается ли имя службы с одного из искомых префиксов
    for target in target_services:
        if service_name.startswith(target):
            try:
                service_info = service.as_dict()
                found_services[service_name] = {
                    'name': service_name,
                    'display_name': service_info.get('display_name', 'Неизвестно'),
                    'status': service_info.get('status', 'Неизвестно'),
                    'start_type': service_info.get('start_type', 'Неизвестно'),
                    'binpath': service_info.get('binpath', 'Неизвестно'),
                    'pid': service_info.get('pid', None)
                }
                print(f'Найдена служба: {service_name}')
                print(f'  Отображаемое имя: {service_info.get("display_name", "Неизвестно")}')
                print(f'  Статус: {service_info.get("status", "Неизвестно")}')
                print(f'  Путь: {service_info.get("binpath", "Неизвестно")}')
                print()
            except Exception as e:
                print(f'Ошибка при получении информации о службе {service_name}: {e}')
            break

if not found_services:
    print('Службы не найдены')
else:
    print(f'Всего найдено служб: {len(found_services)}')

# Сохраняем найденные службы в временный файл для передачи между командами
temp_file = Path('temp_found_services.json')
with open(temp_file, 'w', encoding='utf-8') as f:
    json.dump(found_services, f, ensure_ascii=False, indent=2)
    print(f'Данные сохранены во временный файл: {temp_file.absolute()}')
