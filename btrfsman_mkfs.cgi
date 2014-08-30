#!/usr/bin/perl
# btrfsman_mkfs.cgi
# BTRFS Manager - MakeFileSystem

require './btrfsman-lib.pl';
&ReadParse();

ui_print_header(undef, $text{'mkfs_title'}, "", undef, 1, 1);

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
	print $text{'mkfs_h'};	
  print $text{'mkfs_help'};
  
  show_parted();

  print $text{'mkfs_expert_h'};
  print $text{'txt_mkfssynopsis'}; 
  
  print ui_form_start("btrfsman_mkfs.cgi");
  # 'form-data'
  #$text{'arr_expert_bt'},  $text{'arr_expert_bt_help'}, 

  print ui_textbox('opt_mk', 'mkfs.btrfs',20,1), $text{'txt_p'};
  #print ui_textbox('opt_m','-m raid10',20,0), $text{'txt_p'};
  print ui_select('opt_m', 1, ["-m raid10", "-m raid1", "-m raid0", "-m single", "-m raid5", "-m raid6"]), $text{'txt_p'};
  
  #print ui_textbox('opt_d','-d raid10',20,0), $text{'txt_p'};
  print ui_select('opt_d', 1, ["-d raid10", "-d raid1", "-d raid0", "-d single", "-d raid5", "-d raid6"]), $text{'txt_p'};

  print ui_textbox('opt_label','-L NewLabel',30,0), $text{'txt_p'};
  print ui_textbox('opt_o',' ',20,0), $text{'txt_p'};
  print ui_textbox('opt_dev','/dev/sdWW /dev/sdXX /dev/sdYY /dev/sdZZ',40,0), $text{'txt_p'};
  
  print ui_form_end( [[undef, $text{'mkfs_expert_bt'}]] );

}

 
ui_print_footer('/', 'Webmin index', '', 'Module menu');

