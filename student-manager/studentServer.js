const students = [
    { name: "A", marks: 90 },
    { name: "B", marks: 40 },
    { name: "C", marks: 80 }
];

function showStudents() {
    console.log(students);
}

function addStudent(name, marks) {
    students.push({ name, marks });
}

module.exports = {
    showStudents,
    addStudent
};