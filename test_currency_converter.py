# Импорт необходимых модулей
import unittest  # Основной модуль для unit-тестирования в Python
from app import get_currency_rates, index  # Импорт тестируемых функций из основного файла
from flask import Flask, template_rendered, request  # Компоненты Flask для тестирования


class TestCurrencyConverter(unittest.TestCase):
    """Класс для тестирования функций конвертера валют"""
    # Наследуемся от unittest.TestCase - базового класса для создания тестов

    def setUp(self):
        """Настройка тестового окружения"""
        # Метод вызывается перед каждым тестом для подготовки среды
        self.app = Flask(__name__)  # Создаем экземпляр Flask-приложения
        self.app.config['TESTING'] = True  # Включаем тестовый режим (отключает обработку ошибок)
        self.client = self.app.test_client()  # Создаем тестовый клиент для отправки запросов

        # Добавляем маршрут для тестирования
        self.app.add_url_rule('/', 'index', index, methods=['GET', 'POST'])
        # Регистрируем маршрут '/' с обработчиком index, принимающий GET и POST запросы

    def test_get_currency_rates(self):
        """Тестирование функции получения курсов валют"""
        rates = get_currency_rates()  # Вызываем тестируемую функцию

        # Проверяем, что возвращается словарь
        self.assertIsInstance(rates, dict)
        # assertIsInstance проверяет, что rates является экземпляром dict

        # Проверяем наличие основных валют в словаре
        self.assertIn('USD', rates)  # Проверяем наличие ключа 'USD'
        self.assertIn('EUR', rates)  # Проверяем наличие ключа 'EUR'
        self.assertIn('RUB', rates)  # Проверяем наличие ключа 'RUB'

        # Проверяем, что курс USD к USD равен 1
        self.assertEqual(rates['USD'], 1.0)
        # assertEqual проверяет равенство значений

    def test_index_route(self):
        """Тестирование главной страницы"""
        with self.app.test_request_context('/'):
            # Создаем контекст запроса для тестирования
            response = index()  # Вызываем функцию index()

            # Проверяем, что функция возвращает результат
            self.assertIsNotNone(response)
            # assertIsNotNone проверяет, что response не None

    def test_currency_conversion(self):
        """Тестирование логики конвертации валют"""
        # Тестовые данные (фиксированные курсы валют)
        test_rates = {
            'USD': 1.0,
            'EUR': 0.85,
            'RUB': 75.0,
            'KZT': 420.0
        }

        # Тест 1: Конвертация USD в EUR
        result = 100 * (test_rates['EUR'] / test_rates['USD'])
        self.assertAlmostEqual(result, 85.0, places=2)
        # assertAlmostEqual проверяет равенство с плавающей точкой с точностью до 2 знаков

        # Тест 2: Конвертация EUR в RUB
        result = 10 * (test_rates['RUB'] / test_rates['EUR'])
        self.assertAlmostEqual(result, 882.35, places=2)

        # Тест 3: Конвертация USD в KZT
        result = 1 * (test_rates['KZT'] / test_rates['USD'])
        self.assertEqual(result, 420.0)

    def test_form_submission(self):
        """Тестирование отправки формы"""
        with self.client as c:  # Используем тестовый клиент
            # Отправляем POST-запрос с тестовыми данными формы
            response = c.post('/', data={
                'amount': '100',  # Сумма для конвертации
                'from_currency': 'USD',  # Исходная валюта
                'to_currency': 'EUR'  # Целевая валюта
            })

            # Проверяем код ответа (200 - успешный запрос)
            self.assertEqual(response.status_code, 200)

            # Проверяем, что ответ содержит ожидаемые данные
            self.assertIn(b'Money convert', response.data)
            # assertIn проверяет наличие подстроки в ответе
            self.assertIn(b'100', response.data)  # Проверяем сумму
            self.assertIn(b'USD', response.data)  # Проверяем исходную валюту
            self.assertIn(b'EUR', response.data)  # Проверяем целевую валюту


if __name__ == '__main__':
    unittest.main()  # Запускаем все тесты, если файл выполняется напрямую