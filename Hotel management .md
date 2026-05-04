<!DOCTYPE html>  
<html lang="en">  
<head>  
    <meta charset="UTF-8">  
    <title>Hotel Management System</title>  
    <style>  
        body {  
            font-family: Arial;  
            background-color: #f4f4f4;  
            padding: 20px;  
        }  
        h1 {  
            color: #333;  
        }  
        input, button {  
            padding: 10px;  
            margin: 5px;  
        }  
        table {  
            border-collapse: collapse;  
            width: 100%;  
            margin-top: 20px;  
        }  
        table, th, td {  
            border: 1px solid #000;  
        }  
        th, td {  
            padding: 10px;  
            text-align: left;  
        }  
    </style>  
</head>  
<body>  
  
<h1>Hotel Management System</h1>  
  
<input type="text" id="name" placeholder="Guest Name">  
<input type="number" id="room" placeholder="Room Number">  
<button onclick="addGuest()">Add Guest</button>  
  
<h2>Guest List</h2>  
<table>  
    <thead>  
        <tr>  
            <th>Name</th>  
            <th>Room</th>  
        </tr>  
    </thead>  
    <tbody id="guestList"></tbody>  
</table>  
  
<h3 id="totalRooms">Total Rooms Occupied: 0</h3>  
  
<script>  
    let guests = [];  
  
    function addGuest() {  
        let name = document.getElementById("name").value;  
        let room = document.getElementById("room").value;  
  
        if (name === "" || room === "") {  
            alert("Please fill all fields");  
            return;  
        }  
  
        guests.push({name: name, room: room});  
        displayGuests();  
  
        document.getElementById("name").value = "";  
        document.getElementById("room").value = "";  
    }  
  
    function displayGuests() {  
        let list = document.getElementById("guestList");  
        list.innerHTML = "";  
  
        guests.forEach(g => {  
            let row = `<tr>  
                <td>${g.name}</td>  
                <td>${g.room}</td>  
            </tr>`;  
            list.innerHTML += row;  
        });  
  
        document.getElementById("totalRooms").innerText =  
            "Total Rooms Occupied: " + guests.length;  
    }  
</script>  
  
</body>  
</html>  
