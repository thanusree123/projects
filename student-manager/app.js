const choice = process.argv[2];
const name = process.argv[3];
const marks = Number(process.argv[4]);
switch(choice){
    case "show":
        studentServer.showStudent();
        break;

    case "add":
        studentServer.addStudent(name, marks);
        break;

    case "find":
        console.log(studentServer.findStudent(name));
        break;

    case "delete":
        studentServer.deleteStudent(name);
        break;

    case "update":
        studentServer.updateMarks(name, marks);
        break;

    default:
        console.log("Invalid command");
}