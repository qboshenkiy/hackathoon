document.getElementById("search-btn").addEventListener("click", function () {
    const name = document.getElementById("search-name").value.toLowerCase();
    const absent_count = document.getElementById("absent_count").value;
    const course = document.getElementById("course").value;
    const group = document.getElementById("group").value;

    const students = [
        { name: "Иван Иванов",  course: "course1", group: "group1" },
        { name: "Мария Петрова",  course: "course2", group: "group2" },
        { name: "Дмитрий Сидоров",  course: "course3", group: "group3" },
    ];

    const filteredStudents = students.filter(student => {
        return (
            (name ? student.name.toLowerCase().includes(name) : true) &&
            (semester ? student.semester === semester : true) &&
            (course ? student.course === course : true) &&
            (group ? student.group === group : true)
            (absent_count ? student.absent_count === absent_count : true)
        );
    });

    const tableBody = document.querySelector(".results-table tbody");
    tableBody.innerHTML = "";

    filteredStudents.forEach(student => {
        const row = tableBody.insertRow();
        row.innerHTML = `<td>${student.name}</td><td>${student.course}</td><td>${student.group}</td><td>${student.absent_count}</td>`;
    });
});
