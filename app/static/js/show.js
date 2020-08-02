var j=1;
function turn_off_empty()
{
  $("#empty").attr("style","display:none;");
}
function turn_off_exercises()
{
  $("#all_exercises").attr("style","display:none;");
}
function turn_on_exercises()
{
  $("#all_exercises").attr("style","display:block;");
}
function delete_ex(val)
{
  $('#div_'+val).attr("style","display:none;");
  $('#span_'+val).attr("style","display:none;");
  $('#confirm_delete_button').attr("style","display:block");
  document.getElementById('exercise_list_to_deleting').value+=document.getElementById('span_'+val).innerHTML+"+"
  exist[val]=0;
}
function turn_off_trainings()
{
  $("#all_training").attr("style","display:none;");
}
function turn_on_trainings()
{
  $("#all_training").attr("style","display:block;");
}
