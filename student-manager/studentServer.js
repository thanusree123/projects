const fs=require("fs")

function getStudent(){
    const data=fs.readFileSync(
        "students.json",
        "utf8"
    );
    return JSON.parse(data);
}
function showStudent(){
    const students=getStudent();
    console.log(students)
}
function addStudent(name,marks){
    const student=getStudent()
    student.push({
        name,
        marks
    });
    fs.writeFileSync(
        "students.json",
        JSON.stringify(student)
    )
}

module.exports={
    showStudent,
    addStudent
}