---
sidebar_position: 5
---

# Примеры кода (Code Snippets)

Готовые реализации ключевых алгоритмов и функций для разработки систем управления морскими автономными судами.

## Базовые структуры данных

### Представление позиции и скорости

```python
from dataclasses import dataclass
from typing import Tuple

@dataclass
class Position:
    """Позиция судна в координатах (широта, долгота)"""
    latitude: float  # Широта в градусах
    longitude: float  # Долгота в градусах
    
    def to_cartesian(self, origin: 'Position') -> Tuple[float, float]:
        """Преобразование в декартовы координаты относительно начала"""
        # Упрощенное преобразование (для малых расстояний)
        lat_diff = (self.latitude - origin.latitude) * 111000  # метры
        lon_diff = (self.longitude - origin.longitude) * 111000 * \
                   __import__('math').cos(__import__('math').radians(origin.latitude))
        return (lon_diff, lat_diff)

@dataclass
class Velocity:
    """Скорость судна"""
    speed: float  # Скорость в узлах
    course: float  # Курс в градусах (0-360)
    
    def to_components(self) -> Tuple[float, float]:
        """Преобразование в компоненты скорости (vx, vy)"""
        import math
        rad = math.radians(self.course)
        # Скорость в м/с (1 узел = 0.51444 м/с)
        v = self.speed * 0.51444
        vx = v * math.sin(rad)
        vy = v * math.cos(rad)
        return (vx, vy)

@dataclass
class ShipState:
    """Состояние судна"""
    position: Position
    velocity: Velocity
    heading: float  # Курс в градусах
    timestamp: float  # Время в секундах
```

### Обнаруженный объект

```python
@dataclass
class DetectedObject:
    """Обнаруженный объект (другое судно, препятствие)"""
    object_id: str
    position: Position
    velocity: Velocity
    distance: float  # Расстояние в метрах
    bearing: float  # Азимут в градусах
    object_type: str  # 'ship', 'buoy', 'land', etc.
    confidence: float  # Уверенность в обнаружении (0-1)
    last_update: float  # Время последнего обновления
```

## Алгоритмы избежания столкновений

### Расчет CPA и TCPA

```python
import math

def calculate_cpa_tcpa(own_state: ShipState, 
                       other_object: DetectedObject) -> Tuple[float, float]:
    """
    Расчет CPA (Closest Point of Approach) и TCPA (Time to CPA)
    
    Args:
        own_state: Состояние собственного судна
        other_object: Обнаруженный объект
    
    Returns:
        (CPA, TCPA): Минимальное расстояние и время до него
    """
    # Преобразование в декартовы координаты
    own_pos = own_state.position.to_cartesian(own_state.position)
    other_pos = other_object.position.to_cartesian(own_state.position)
    
    # Компоненты скорости
    own_vx, own_vy = own_state.velocity.to_components()
    other_vx, other_vy = other_object.velocity.to_components()
    
    # Относительная позиция и скорость
    dx = other_pos[0] - own_pos[0]
    dy = other_pos[1] - own_pos[1]
    dvx = other_vx - own_vx
    dvy = other_vy - own_vy
    
    # Расчет TCPA
    denom = dvx**2 + dvy**2
    if denom < 1e-6:  # Суда движутся параллельно
        tcpa = float('inf')
    else:
        tcpa = -(dx * dvx + dy * dvy) / denom
        tcpa = max(0, tcpa)  # TCPA не может быть отрицательным
    
    # Расчет CPA
    if tcpa == float('inf'):
        # Суда движутся параллельно, CPA = текущее расстояние
        cpa = math.sqrt(dx**2 + dy**2)
    else:
        # Позиция в момент CPA
        x_cpa = dx + dvx * tcpa
        y_cpa = dy + dvy * tcpa
        cpa = math.sqrt(x_cpa**2 + y_cpa**2)
    
    return (cpa, tcpa)

def assess_collision_risk(cpa: float, tcpa: float, 
                         safe_distance: float = 500) -> str:
    """
    Оценка риска столкновения
    
    Args:
        cpa: Минимальное расстояние (метры)
        tcpa: Время до минимального расстояния (секунды)
        safe_distance: Безопасное расстояние (метры)
    
    Returns:
        Уровень риска: 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'
    """
    if cpa > safe_distance * 2:
        return 'LOW'
    elif cpa > safe_distance:
        if tcpa > 300:  # 5 минут
            return 'MEDIUM'
        else:
            return 'HIGH'
    else:
        return 'CRITICAL'
```

### Определение типа встречи

```python
def determine_encounter_type(own_state: ShipState, 
                            other_object: DetectedObject) -> str:
    """
    Определение типа встречи судов согласно COLREGs
    
    Args:
        own_state: Состояние собственного судна
        other_object: Обнаруженный объект
    
    Returns:
        Тип встречи: 'HEAD_ON', 'CROSSING', 'OVERTAKING', 'SAFE'
    """
    import math
    
    # Азимут до другого судна
    bearing = other_object.bearing
    own_course = own_state.velocity.course
    
    # Нормализация углов
    relative_bearing = (bearing - own_course) % 360
    
    # Курс другого судна
    other_course = math.degrees(math.atan2(
        other_object.velocity.to_components()[0],
        other_object.velocity.to_components()[1]
    )) % 360
    
    # Относительный курс
    relative_course = (other_course - own_course) % 360
    
    # Определение типа встречи
    if 10 < relative_bearing < 350:  # Судно не впереди и не позади
        if 170 < relative_bearing < 190:  # Встречное направление
            return 'HEAD_ON'
        elif 20 < relative_bearing < 160:  # Пересечение справа
            return 'CROSSING'
        elif 200 < relative_bearing < 340:  # Пересечение слева
            return 'CROSSING'
    
    # Проверка обгона
    if abs(relative_course) < 30 or abs(relative_course - 360) < 30:
        if 20 < relative_bearing < 160:
            return 'OVERTAKING'
    
    return 'SAFE'
```

### Dynamic Window Approach (DWA)

```python
class DynamicWindowApproach:
    """Реализация алгоритма Dynamic Window Approach"""
    
    def __init__(self, max_speed: float = 10, max_angular_velocity: float = 1.0):
        """
        Инициализация DWA
        
        Args:
            max_speed: Максимальная скорость (м/с)
            max_angular_velocity: Максимальная угловая скорость (рад/с)
        """
        self.max_speed = max_speed
        self.max_angular_velocity = max_angular_velocity
    
    def calculate_dynamic_window(self, current_velocity: float, 
                                current_angular_velocity: float,
                                acceleration: float = 0.5,
                                dt: float = 0.1) -> Tuple[Tuple[float, float], 
                                                          Tuple[float, float]]:
        """
        Расчет динамического окна
        
        Args:
            current_velocity: Текущая скорость (м/с)
            current_angular_velocity: Текущая угловая скорость (рад/с)
            acceleration: Максимальное ускорение (м/с²)
            dt: Временной шаг (секунды)
        
        Returns:
            ((v_min, v_max), (w_min, w_max)): Диапазоны скорости и угловой скорости
        """
        # Ограничения по ускорению
        v_min = max(0, current_velocity - acceleration * dt)
        v_max = min(self.max_speed, current_velocity + acceleration * dt)
        
        w_min = max(-self.max_angular_velocity, 
                   current_angular_velocity - acceleration * dt)
        w_max = min(self.max_angular_velocity, 
                   current_angular_velocity + acceleration * dt)
        
        return ((v_min, v_max), (w_min, w_max))
    
    def evaluate_trajectory(self, velocity: float, angular_velocity: float,
                           obstacles: list, goal_position: Tuple[float, float],
                           current_position: Tuple[float, float],
                           dt: float = 0.1) -> float:
        """
        Оценка траектории
        
        Args:
            velocity: Скорость (м/с)
            angular_velocity: Угловая скорость (рад/с)
            obstacles: Список препятствий
            goal_position: Целевая позиция
            current_position: Текущая позиция
            dt: Временной шаг
        
        Returns:
            Оценка траектории (чем выше, тем лучше)
        """
        import math
        
        # Симуляция траектории на горизонт T
        T = 1.0  # Горизонт планирования (секунды)
        steps = int(T / dt)
        
        x, y, theta = current_position[0], current_position[1], 0
        min_distance_to_obstacle = float('inf')
        
        for _ in range(steps):
            # Обновление позиции
            x += velocity * math.cos(theta) * dt
            y += velocity * math.sin(theta) * dt
            theta += angular_velocity * dt
            
            # Проверка расстояния до препятствий
            for obstacle in obstacles:
                dist = math.sqrt((x - obstacle[0])**2 + (y - obstacle[1])**2)
                min_distance_to_obstacle = min(min_distance_to_obstacle, dist)
        
        # Компоненты оценки
        heading_score = 1.0 / (1.0 + abs(theta))  # Предпочитаем малые углы
        distance_to_goal = math.sqrt((x - goal_position[0])**2 + 
                                    (y - goal_position[1])**2)
        goal_score = 1.0 / (1.0 + distance_to_goal)
        obstacle_score = min_distance_to_obstacle / 100.0  # Нормализация
        
        # Итоговая оценка (взвешенная сумма)
        total_score = 0.3 * heading_score + 0.5 * goal_score + 0.2 * obstacle_score
        
        return total_score
    
    def select_velocity(self, current_velocity: float,
                       current_angular_velocity: float,
                       obstacles: list,
                       goal_position: Tuple[float, float],
                       current_position: Tuple[float, float]) -> Tuple[float, float]:
        """
        Выбор оптимальной скорости и угловой скорости
        
        Returns:
            (velocity, angular_velocity): Оптимальные параметры движения
        """
        # Расчет динамического окна
        (v_min, v_max), (w_min, w_max) = self.calculate_dynamic_window(
            current_velocity, current_angular_velocity)
        
        best_score = -float('inf')
        best_velocity = current_velocity
        best_angular_velocity = 0
        
        # Перебор возможных скоростей
        v_resolution = 0.1
        w_resolution = 0.1
        
        v = v_min
        while v <= v_max:
            w = w_min
            while w <= w_max:
                score = self.evaluate_trajectory(v, w, obstacles, 
                                               goal_position, current_position)
                if score > best_score:
                    best_score = score
                    best_velocity = v
                    best_angular_velocity = w
                w += w_resolution
            v += v_resolution
        
        return (best_velocity, best_angular_velocity)
```

## Алгоритмы планирования пути

### A* алгоритм

```python
import heapq
from typing import List, Tuple, Dict, Optional

class AStarPathPlanner:
    """Реализация алгоритма A* для планирования пути"""
    
    def __init__(self, grid: List[List[int]], cell_size: float = 10.0):
        """
        Инициализация планировщика
        
        Args:
            grid: Сетка препятствий (0 = свободно, 1 = препятствие)
            cell_size: Размер ячейки в метрах
        """
        self.grid = grid
        self.cell_size = cell_size
        self.height = len(grid)
        self.width = len(grid[0]) if grid else 0
    
    def heuristic(self, pos: Tuple[int, int], 
                 goal: Tuple[int, int]) -> float:
        """Эвристическая функция (Манхэттенское расстояние)"""
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])
    
    def get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Получение соседних ячеек"""
        neighbors = []
        x, y = pos
        
        # 8-связность
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if self.grid[ny][nx] == 0:  # Свободная ячейка
                        neighbors.append((nx, ny))
        
        return neighbors
    
    def plan_path(self, start: Tuple[int, int], 
                 goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        """
        Планирование пути от start к goal
        
        Returns:
            Список ячеек пути или None если пути нет
        """
        open_set = [(0, start)]
        came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
        g_score: Dict[Tuple[int, int], float] = {start: 0}
        f_score: Dict[Tuple[int, int], float] = {start: self.heuristic(start, goal)}
        
        closed_set = set()
        
        while open_set:
            current = heapq.heappop(open_set)[1]
            
            if current == goal:
                # Восстановление пути
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                return path[::-1]
            
            closed_set.add(current)
            
            for neighbor in self.get_neighbors(current):
                if neighbor in closed_set:
                    continue
                
                # Расчет стоимости
                dx = abs(neighbor[0] - current[0])
                dy = abs(neighbor[1] - current[1])
                cost = 1.414 if dx == 1 and dy == 1 else 1.0  # Диагональ дороже
                
                tentative_g = g_score[current] + cost
                
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + self.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
        
        return None  # Пути нет
    
    def path_to_waypoints(self, path: List[Tuple[int, int]]) -> List[Tuple[float, float]]:
        """Преобразование пути из ячеек в координаты"""
        waypoints = []
        for x, y in path:
            lon = x * self.cell_size
            lat = y * self.cell_size
            waypoints.append((lon, lat))
        return waypoints
```

## Утилиты

### Преобразование углов

```python
import math

def normalize_angle(angle: float) -> float:
    """Нормализация угла в диапазон [0, 360)"""
    return angle % 360

def angle_difference(angle1: float, angle2: float) -> float:
    """Расчет разницы между двумя углами"""
    diff = (angle2 - angle1) % 360
    if diff > 180:
        diff -= 360
    return diff

def course_to_bearing(course: float) -> float:
    """Преобразование курса в азимут"""
    return normalize_angle(90 - course)

def bearing_to_course(bearing: float) -> float:
    """Преобразование азимута в курс"""
    return normalize_angle(90 - bearing)
```

### Логирование и мониторинг

```python
import logging
from datetime import datetime

class ShipSystemLogger:
    """Логирование событий системы управления судном"""
    
    def __init__(self, log_file: str = 'ship_system.log'):
        self.logger = logging.getLogger('ShipSystem')
        self.logger.setLevel(logging.DEBUG)
        
        # Файловый обработчик
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.DEBUG)
        
        # Форматер
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        fh.setFormatter(formatter)
        
        self.logger.addHandler(fh)
    
    def log_collision_risk(self, object_id: str, risk_level: str, 
                          cpa: float, tcpa: float):
        """Логирование риска столкновения"""
        self.logger.warning(
            f'Collision risk detected: Object {object_id}, '
            f'Risk Level: {risk_level}, CPA: {cpa:.1f}m, TCPA: {tcpa:.1f}s'
        )
    
    def log_maneuver(self, maneuver_type: str, new_course: float, 
                    new_speed: float):
        """Логирование маневра"""
        self.logger.info(
            f'Maneuver executed: Type: {maneuver_type}, '
            f'New Course: {new_course:.1f}°, New Speed: {new_speed:.1f} knots'
        )
    
    def log_system_status(self, status: dict):
        """Логирование статуса системы"""
        self.logger.info(f'System Status: {status}')
```

## Дополнительные ресурсы

- [Гайд по избежанию столкновений](/docs/guides/01-collision-avoidance-guide.md)
- [Гайд по планированию пути](/docs/guides/02-path-planning-guide.md)
- [Глоссарий](/docs/glossary-extended)
- [Статьи](/docs/papers)

## Примечания

Все примеры кода предоставлены в образовательных целях. При использовании в реальных системах требуется:

1. Тщательное тестирование и валидация
2. Адаптация к конкретным требованиям и ограничениям судна
3. Соответствие международным правилам и стандартам
4. Обеспечение надежности и отказоустойчивости
5. Регулярное обновление и улучшение алгоритмов
