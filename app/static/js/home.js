var focus_ind_1=0, focus_ind_2=0, focus_ind_3=0;
var activity_of_action_1=0, activity_of_action_2=0, activity_of_action_3=0;
function note_action_as_active(val)
{
  if (val==1) activity_of_action_1=1;
  if (val==2) activity_of_action_2=1;
  if (val==3) activity_of_action_3=1;
}
function note_action_as_non_active(val)
{
  if (val==1) activity_of_action_1=0;
  if (val==2) activity_of_action_2=0;
  if (val==3) activity_of_action_3=0;
}
function move_action(val)
{
  $("#caption"+val).attr("style","padding-left: 2%; position: absolute; margin-top:95%; opacity:0; transition: 0.1s ease;");
  $("#form_action_"+val).attr("style","margin-top: 100%; transition: 0.3s ease; z-index: -1;");
}
function move_action_back(val)
{
  if (val==1 && focus_ind_1==0 && activity_of_action_1==0)
  {
    $("#form_action_"+val).attr("style","margin-top: 0%; position: absolute; z-index:-1; transition: 0.3s ease;");
    $("#caption"+val).attr("style","padding-left: 2%; position:absolute; margin-top:100%; color: #000; opacity:1; transition: 0.4s cubic-bezier(.26, .76, .30, .80);");
  }
  if (val==2 && focus_ind_2==0 && activity_of_action_2==0)
  {
    $("#form_action_"+val).attr("style","margin-top: 0%; transition: 0.3s ease;");
    $("#caption"+val).attr("style","padding-left: 2%; position:absolute; margin-top:100%; color: #000; opacity:1; transition: 0.4s cubic-bezier(.26, .76, .30, .80);");
  }
  if (val==3 && focus_ind_3==0 && activity_of_action_3==0)
  {
    $("#form_action_"+val).attr("style","margin-top: 0%; transition: 0.3s ease;");
    $("#caption"+val).attr("style","padding-left: 2%; position:absolute; margin-top:100%; color: #000; opacity:1; transition: 0.4s cubic-bezier(.26, .76, .30, .80);");
  }

}
function focus_on(val)
{
  if (val==1) focus_ind_1=1;
  if (val==2) focus_ind_2=1;
  if (val==3) focus_ind_3=1;
}
function focus_off(val)
{
  if (val==1) focus_ind_1=0;
  if (val==2) focus_ind_2=0;
  if (val==3) focus_ind_3=0;
}

function close_action_on_click()
{
  if (activity_of_action_1==1)
  {
    $("#sp_for_1").attr("style","display: block; margin-top:100%;");
    $("#sp_caption_1").attr("style","margin-top:0%; padding-left:2%;");
  }
  if (activity_of_action_1==0)
  {
    $("#sp_for_1").attr("style","display: none;");
    $("#sp_caption_1").attr("style","margin-top:100%; padding-left:2%;");
  }

  if (activity_of_action_2==1)
  {
    $("#sp_for_2").attr("style","display: block; margin-top:100%;");
    $("#sp_caption_2").attr("style","margin-top:0%; padding-left:2%;");
  }
  if (activity_of_action_2==0)
  {
    $("#sp_for_2").attr("style","display: none;");
    $("#sp_caption_2").attr("style","margin-top:100%; padding-left:2%;");
  }

}


var cursor_on_exercise_menu=0;
var exercise_list_stage=0;
var exercise_menu_stage=0;
function start_ex()
{
  $(".exercise_menu").attr("style","display:block;")
  exercise_menu_stage=1;
}
function cursor_on_exercise_menu_up()
{
  cursor_on_exercise_menu=1;
}
function cursor_on_exercise_menu_down()
{
  cursor_on_exercise_menu=0;
}
function cursor_on_exercise_list_up()
{
  exercise_list_stage=1;
}
function cursor_on_exercise_list_down()
{
  exercise_list_stage=0;
}
function close_exercise_menu_on_click()
{
  if (cursor_on_exercise_menu==0 && exercise_menu_stage==1) close_exercise_menu();
}

function close_exercise_menu()
{
  $(".exercise_menu").attr("style","display:none;");
  exercise_menu_stage=0;
}

var cursor_on_help_menu=0;
var help_menu_stage=0;
function start_help()
{
  $(".help_menu").attr("style","display:block;")
  help_menu_stage=1;
}
function cursor_on_help_menu_up()
{
  cursor_on_help_menu=1;
}
function cursor_on_help_menu_down()
{
  cursor_on_help_menu=0;
}
function close_help_menu_on_click()
{
  if (cursor_on_help_menu==0 && help_menu_stage==1)
  {
    $(".help_menu").attr("style","display:none;");
    help_menu_stage=0;
  }
}

var cursor_on_about_menu=0;
var about_menu_stage=0;
function start_about()
{
  $(".about_menu").attr("style","display:block;");
  about_menu_stage=1;
}
function cursor_on_about_menu_up()
{
  cursor_on_about_menu=1;
}
function cursor_on_about_menu_down()
{
  cursor_on_about_menu=0;
}
function close_about_menu_on_click()
{
  if (cursor_on_about_menu==0 && about_menu_stage==1)
  {
    $(".about_menu").attr("style","display:none;");
    about_menu_stage=0;
  }
}

var fback=0;
function light_up_cross()
{
  fback=1;
}
function light_out_cross()
{
  fback=0;
}
function check_and_kick()
{
  if (exercise_list_stage==0) close_all_exercises_in_exlist();
}
function open_feedback_field()
{
  if (fback==0) $("#feedback_field").attr("style","display:block;");
}
function close_feedback_field()
{
  $("#feedback_field").attr("style","display:none;");
}


var date_flag=0;
function date_go()
{
  var today = new Date();
  var dd = String(today.getDate()).padStart(2, '0');
  var mm = String(today.getMonth() + 1).padStart(2, '0');
  var yyyy = today.getFullYear();
  today = yyyy + "-" + mm + "-" + dd;
  $d=today;
  if (date_flag==0)
  {
    $("#date").attr("value",$d);
    date_flag=1;
  } else
  {
    date_flag=0;
    $("#date").attr("value","");
  }
}

function isValidDate(dateString)
{
  if(!/^\d{4}\-\d{2}\-\d{2}$/.test(dateString))
  return false;
  var parts = dateString.split("-");
  var day = parseInt(parts[2], 10);
  var month = parseInt(parts[1], 10);
  var year = parseInt(parts[0], 10);
  if(year < 1000 || year > 3000 || month == 0 || month > 12)
  return false;
  var monthLength = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ];
  if(year % 400 == 0 || (year % 100 != 0 && year % 4 == 0))
  monthLength[1] = 29;
  return day > 0 && day <= monthLength[month - 1];
};

function open_special_exercise_with_order(val)
{
  $("#block"+val).attr("style","display:block;");
}
function close_all_exercises_in_exlist()
{
  for (var val=1; val<=7; val++) $("#block"+val).attr("style","display:none;");
}

var i=1;
var j=1;
var sett=0;
var cur="";
var saved_id=1;
var inp_id=1;
var arr_exe=new Array();
var arr_wei=new Array();
function clean_weight_field()
{
  document.getElementById('weight').value="";
}
function del(val)
{
  $("#saved"+val).attr("style","display:none;");
  $("#inpex"+val).attr("value","");
  $("#inpwe"+val).attr("value","");
  var train = document.getElementById('all_exercises_during_training').value;
  $("#all_exercises_during_training").attr("value",train.replace(arr_exe[val]+":"+arr_wei[val]+"+", ""));
}
function fix_exercise_to_save()
{
  var s="<div onclick='del(" + saved_id + ")' id='saved" + saved_id + "' style='height:auto;'>" + document.getElementById('exercise' + sett).innerHTML + "<pre>   </pre>" + document.getElementById('weight').value + "</div>";
  arr_exe[saved_id]=document.getElementById('exname_' + sett).innerHTML;
  arr_wei[saved_id]=document.getElementById('weight').value;
  $("#inpex"+inp_id).attr("value",arr_exe[inp_id]);
  $("#inpwe"+inp_id).attr("value",arr_wei[inp_id]);
  inp_id++;
  saved_id++;
  document.getElementById('fixing_field').innerHTML+=s;
  document.getElementById('all_exercises_during_training').value+=arr_exe[saved_id-1] + ":" + arr_wei[saved_id-1] + "+"
}
function fix_selected_exercise(val)
{
  sett=val;
  if (cur=="")
  {
    cur="<input id='ept' type='button' style='color: #fff; width: auto; position: absolute; background-color: #303030;border-color: #000;top: 46%; right: 40%;' value='" + document.getElementById('exname_' + sett).innerHTML + "'>";
    document.getElementById('external_exercise_block').innerHTML+=cur;
  }
  else
  $("#ept").attr("value",document.getElementById('exname_' + sett).innerHTML);
}
function stop_time()
{
    if (!isValidDate(document.getElementById('date').value))
    {
      $("#date").attr("style","border-color: red; width: 50%;");
      event.preventDefault();
    }
}
