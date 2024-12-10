// Сопоставление номеров месяцев с названиями
const monthNames = {
    '1': 'january', '2': 'february', '3': 'march', '4': 'april',
    '5': 'may', '6': 'june', '7': 'july', '8': 'august',
    '9': 'september', '10': 'october', '11': 'november', '12': 'december',
};

// Инициализация календарей
const calendars = {
    september: `
        <div class="month">
            <h3>Сентябрь</h3>
            <div class="days">
                ${generateDays(30, 'september')}
            </div>
        </div>
    `,
    october: `
        <div class="month">
            <h3>Октябрь</h3>
            <div class="days">
                ${generateDays(31, 'october')}
            </div>
        </div>
    `,
    november: `
        <div class="month">
            <h3>Ноябрь</h3>
            <div class="days">
                ${generateDays(30, 'november')}
            </div>
        </div>
    `,
    december: `
        <div class="month">
            <h3>Декабрь</h3>
            <div class="days">
                ${generateDays(31, 'december')}
            </div>
        </div>
    `
};

// Функция для генерации дней с учетом сохраненных данных из localStorage
function generateDays(totalDays, month) {
    const savedData = JSON.parse(localStorage.getItem(month)) || {};
    let daysHTML = '';

    for (let i = 1; i <= totalDays; i++) {
        const dayStatus = savedData[i] || 'none'; // Получаем статус дня из localStorage
        const dayClass = dayStatus === 'present' ? 'present' : dayStatus === 'absent' ? 'absent' : '';
        daysHTML += `<span class="day ${dayClass}" data-day="${i}" data-month="${month}">${i}</span>`;
    }

    return daysHTML;
}

// Элементы
const monthSelector = document.getElementById('month');
const calendarContainer = document.getElementById('calendar-container');

// Начальное отображение
const initialMonth = 'september'; // Укажите месяц для первого отображения
calendarContainer.innerHTML = calendars[initialMonth];
attachDayClickEvents(initialMonth);

// Изменение месяца
monthSelector.addEventListener('change', (event) => {
    const selectedMonth = event.target.value;
    calendarContainer.innerHTML = calendars[selectedMonth];
    attachDayClickEvents(selectedMonth); // Привязываем события к дням
});

// Функция для привязки событий клика по ячейкам календаря
function attachDayClickEvents(month) {
    const days = document.querySelectorAll('.day');
    days.forEach(day => {
        day.addEventListener('click', (event) => {
            const element = event.target;
            const dayNumber = element.dataset.day;

            // Определяем текущий статус и переключаем его
            let newStatus;
            if (element.classList.contains('present')) {
                element.classList.remove('present');
                element.classList.add('absent');
                newStatus = 'absent';
            } else if (element.classList.contains('absent')) {
                element.classList.remove('absent');
                newStatus = 'none';
            } else {
                element.classList.add('present');
                newStatus = 'present';
            }

            // Сохраняем в localStorage
            saveToLocalStorage(month, dayNumber, newStatus);

            // Отправляем данные на сервер
            updateAttendanceOnServer(dayNumber, newStatus, month);
        });
    });
}

// Функция для сохранения данных в localStorage
function saveToLocalStorage(month, day, status) {
    const savedData = JSON.parse(localStorage.getItem(month)) || {};
    savedData[day] = status; // Обновляем статус дня
    localStorage.setItem(month, JSON.stringify(savedData)); // Сохраняем обратно
}

// Функция для отправки данных на сервер
function updateAttendanceOnServer(day, status, month) {
    const userId = document.getElementById('user-id').value; // ID пользователя

    fetch('/update-attendance/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(), // CSRF-токен
        },
        body: JSON.stringify({
            day: day,
            month: month,
            status: status,
            user_id: userId,
        }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Ошибка обновления посещаемости на сервере');
        }
        return response.json();
    })
    .then(data => {
        console.log('Attendance updated successfully:', data);
    })
    .catch(error => {
        console.error('Ошибка:', error);
    });
}

// Функция для получения CSRF-токена
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

// Автоматическая отметка посещаемости при загрузке страницы
(function () {
    const userId = document.getElementById('user-id').value;
    const today = new Date();
    const year = today.getFullYear();
    const month = today.getMonth() + 1; // Месяцы начинаются с 0
    const day = today.getDate();

    const autoMarkUrl = `/auto-mark-attendance/${userId}/${year}-${month.toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}/`;

    fetch(autoMarkUrl, {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Attendance marked successfully:', data);

            const monthName = monthNames[month.toString()];
            const dayElement = document.querySelector(`.day[data-day="${day}"][data-month="${monthName}"]`);
            if (dayElement) {
                dayElement.classList.add('present');
                dayElement.classList.remove('absent', 'none');
            }
        } else {
            console.error('Ошибка при отметке посещаемости:', data.error);
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
    });
})();

// Привязываем события при загрузке
attachDayClickEvents(initialMonth);
