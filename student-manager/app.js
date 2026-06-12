const students=[
    {name: "A" ,marks:90},
    {name:"B",marks:40},
    {name:"C",marks:80}
];
function showStudents(){
    console.log(students)
}
function addstudent(name,marks){
    students.push({
        name,
        marks
    });
}
function getPassedStudent(){
    const result=students
    .filter(student=>student.marks>50)
    .map(student=>student.name)
    console.log(result)
}

function totalMarks(){
    const total=students.reduce(
        (sum,student)=>sum+student.marks,0
    );
    console.log(total)
}


function findStudent(name){
    const student=students.find(
        student=>student.name===name
    );
    console.log(student)

}
console.log("All Students:");
showStudents();

addstudent("D", 70);

console.log("\nAfter Adding:");
showStudents();

console.log("\nPassed Students:");
getPassedStudent();

console.log("\nTotal Marks:");
totalMarks();

console.log("\nFind Student:");
findStudent("A");

const studentService = require("./studentServer");

studentService.showStudents();

studentService.addStudent("D", 70);

studentService.showStudents();



