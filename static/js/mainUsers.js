let table = document.getElementById("users-table")
let userSearch = document.getElementById("users-user-search")


userSearch.addEventListener('keydown',filterSearchIndex)
userSearch.addEventListener('keyup',filterSearchIndex)

function filterSearchIndex(){
    if(userSearch.value!=="") {
        const resultSet = new Set();
        for(let i=1;i<table.rows.length;i++){
            let row = table.rows[i];
            if(
                row.cells.item(0).innerHTML.toLowerCase().includes(userSearch.value.toLowerCase()) ||
                row.cells.item(1).innerHTML.toLowerCase().includes(userSearch.value.toLowerCase()) ||
                row.cells.item(4).innerHTML.toLowerCase().includes(userSearch.value.toLowerCase()) ||
                row.cells.item(6).innerHTML.toLowerCase().includes(userSearch.value.toLowerCase()) ||
                row.cells.item(7).innerHTML.toLowerCase().includes(userSearch.value.toLowerCase()) ||
                row.cells.item(8).innerHTML.toLowerCase().includes(userSearch.value.toLowerCase()) 
            ){  
                resultSet.add(i)
                row.style.display = "";
            }else{
                resultSet.delete(i)
                row.style.display = "none";
            }
        }   
        if(resultSet.size == 0){
            table.rows[0].style.display = "none";
            document.getElementById("result-count").innerHTML = "No Results found..."
        }else{
            table.rows[0].style.display = "";
            document.getElementById("result-count").innerHTML = ""
        }
    }else{
        for(let i=1;i<table.rows.length;i++){
            let row = table.rows[i];
                row.style.display = "";
        }
    }
}

