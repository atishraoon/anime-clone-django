

const a =document.getElementById('toggle-edit')
const editpic = document.getElementById('edit-profile')

const toggle_edit = () => {
if (editpic.style.display === "block") {
  editpic.style.display = "none";
} else {
  editpic.style.display = "block";
}
}; 


a.addEventListener('click', toggle_edit);