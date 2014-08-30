#!/usr/bin/perl
# btrfsman_arr.cgi
# BTRFS Manager - Add Remove Replace Management

require './btrfsman-lib.pl';
&ReadParse();

ui_print_header(undef, $text{'arr_title'}, "", undef, 1, 1);

if($in){
  print $text{'txt_arg'}, $in, $text{'txt_p'};
}

$act = $in{'act'};
$dev =  $in{'dev'};
$mp = $in{'mp'};
$opt = $in{'opt'};


if ($dev =~ /[ %&<>!\x27\x60\x3B\x3A\x\n\r\l]/) {
	print "not a safe string";
}

if (($act) && ($mp) && ($dev)  ) {
  #if ($newlabel) {
  #  print "Taking Action Executing Command:#", $text{'txt_p'};
  #  print "btrfs device $act $dev $mp $opt", $text{'txt_p'};
  #  print $text{'arr_operation'}, $text{'txt_p'} ;
  #}
}
else
{
	print $text{'arr_h'};	
  print $text{'arr_help'};
  
  show_parted();

  print $text{'arr_expert_h'};
  print $text{'txt_devicesynopsis'}; 
  
  print ui_form_start("btrfsman_arr.cgi");
  # 'form-data'
  #$text{'arr_expert_bt'},  $text{'arr_expert_bt_help'}, 

  print ui_textbox('opt_cmd', 'btrfs device',20,1), $text{'txt_p'};
  print ui_textbox('opt_ar','add',20,0), $text{'txt_p'};
  #print ui_textbox('opt_d','-d raid10',20,0), $text{'txt_p'};
  #print ui_textbox('opt_label','-L NewLabel',30,0), $text{'txt_p'};
  print ui_textbox('opt_o',' ',20,0), $text{'txt_p'};
  print ui_textbox('opt_dev','/dev/sdWW /dev/sdXX /dev/sdYY /dev/sdZZ',40,0), $text{'txt_p'};
  print ui_textbox('opt_mp','/mnt/XXX',40,0), $text{'txt_p'};
  
  
  print ui_form_end( [[undef, $text{'arr_expert_bt'}]] );
  
  
	
}

 
ui_print_footer('/', 'Webmin index', '', 'Module menu');

