const fs=require("fs")
function getStudent(){
    try{
        const students = JSON.parse(
            fs.readFileSync("students.json")
        );
        return students;
    }
    catch(error){
        console.log("Error reading students file");
        return [];
    }
}
function showStudent(){
    try{
    const students=getStudent();
    console.log(students)
    }
    catch(error){
        console.log("error showing students");
    }
}
function addStudent(name, marks){
    try{
    const students = getStudent();
    const existingStudent =
        students.find(student => student.name === name);
    if(existingStudent){
        console.log("Student already exists");
        return;
    }
    students.push({
        name,
        marks
    });

    fs.writeFileSync(
        "students.json",
        JSON.stringify(students)
    );
    console.log("student added successfully");
}
catch(error){
    console.log("error adding a student");
}
}
function findStudent(name){
    try{
    let students =JSON.parse(fs.readFileSync("students.json"));
    for(let student of students){
        if(student.name===name){
            return student;
        }
    }
    return null;
}
catch(error){
    console.log("error finding student");
    return null;
}
}
function deleteStudent(name){
    try{
    const students=getStudent();
    const updateStudent=students.filter(
        student=>student.name!==name
    );
    fs.writeFileSync(
        "students.json",
        JSON.stringify(updateStudent)
    );
    console.log("student deleted successfully")
}
catch(error){
    console.log("error deleting student");
}
}
function updateMarks(name, newMarks){
    try{
        const students = getStudent();

        for(let student of students){
            if(student.name === name){
                student.marks = newMarks;

                fs.writeFileSync(
                    "students.json",
                    JSON.stringify(students)
                );

                console.log("Marks updated successfully");
                return;
            }
        }

        console.log("Student not found");
    }
    catch(error){
        console.log("Error updating marks");
    }
}
module.exports={
    showStudent,
    addStudent,
    findStudent,
    deleteStudent,
    updateMarks
}
