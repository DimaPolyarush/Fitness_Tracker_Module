
class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')
     

class Training:
    training_type = ""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    """Базовый класс тренировки."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message = InfoMessage(self.__class__.__name__,
                                   self.duration,
                                   self.get_distance(),
                                   self.get_mean_speed(),
                                   self.get_spent_calories())
        return info_message


class Running(Training):
    """Тренировка: бег."""
    training_type = "RUN"
    run_cal_1 = 18
    run_cal_2 = 20

    def get_spent_calories(self) -> float:
        run_cal_3 = self.run_cal_1 * self.get_mean_speed() - self.run_cal_2
        rcal = (run_cal_3 * self.weight / self.M_IN_KM) * (self.duration * 60)
        return rcal


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    training_type = "WLK"
    walk_calorie_1 = 0.035
    walk_calorie_2 = 0.029
    cof = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        cal1 = self.get_mean_speed() ** self.cof // self.height
        cal2 = self.walk_calorie_1 * self.weight
        cal3 = cal1 * self.walk_calorie_2 * self.weight
        calres = (cal2 + cal3) * (self.duration * 60)
        return calres


class Swimming(Training):
    """Тренировка: плавание."""
    training_type = "SWM"
    swim_calorie_1 = 1.1
    swim_calorie_2 = 2
    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        speed1 = self.length_pool * self.count_pool
        self.speed = speed1 / super().M_IN_KM / self.duration
        return self.speed

    def get_spent_calories(self) -> float:
        calories1 = self.get_mean_speed() + self.swim_calorie_1
        calories = calories1 * self.swim_calorie_2 * self.weight
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_train = {'SWM': Swimming,
                  'RUN': Running,
                  'WLK': SportsWalking}
    return type_train[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)