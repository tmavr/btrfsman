#!/usr/bin/perl
# btrfsman_mkfs.cgi
# BTRFS Manager - MakeFileSystem

require './btrfsman-lib.pl';
&ReadParse();

ui_print_header(undef, $text{'mkfs_title'}, "", undef, 1, 1);

if($in){
  print $text{'txt_arg'}, $in, $text{'txt_p'};
}

$opt_mk =  $in{'opt_mk'};
$opt_m = $in{'opt_m'};
$opt_d = $in{'opt_d'};
$opt_label =  $in{'opt_label'};
$opt_o = $in{'opt_o'};
$opt_dev = $in{'opt_dev'};
$cmdconfirm = $in{'cmdconfirm'};

#more sanity check would be a good idea...
if ($dev =~ /[ %&<>!\x27\x60\x3B\x3A\x\n\r\l]/) {
	print $text{'txt_error_string'}, $text{'txt_p'} ;
}

if ( ($opt_m) && ($opt_d) && ($opt_dev) ) {

  $cmd = "mkfs.btrfs $opt_mk $opt_m $opt_d $opt_label $opt_o $opt_dev 2>&1";
  print "<b>$cmd</b>";
  $cmd=urlize($cmd);
  #print "<b>$cmd</b>";
  
  print ui_buttons_start();
  print ui_buttons_row("btrfsman_mkfs.cgi", $text{'index_bt_create'}, $text{'txt_confirm_command'}, ui_hidden('cmdconfirm', $cmd));
  print ui_buttons_end();
  

}
else{
		
	if ($cmdconfirm){
		$cmdconfirm=un_urlize($cmdconfirm);
		print  $text{txt_executing}, $cmd, $text{'txt_p'};
		$result=`$cmdconfirm`;
		print $result;
	}
	
	else
	{
		print $text{'mkfs_h'};	
	  print $text{'mkfs_help'};
	  
	  show_parted();
	
	  print $text{'mkfs_expert_h'};
	  print $text{'txt_mkfssynopsis'}; 
	  
	  
	  print ui_form_start("btrfsman_mkfs.cgi");
	
	  print ui_textbox('opt_mk', 'mkfs.btrfs',20,1), $text{'txt_p'};
	  print ui_select('opt_m', 1, ["", "-m raid10", "-m raid1", "-m raid0", "-m single", "-m raid5", "-m raid6"]), $text{'txt_metadata'}, $text{'txt_p'};
	  print ui_select('opt_d', 1, ["", "-d raid10", "-d raid1", "-d raid0", "-d single", "-d raid5", "-d raid6"]), $text{'txt_data'}, $text{'txt_p'};
	  print ui_textbox('opt_label','-L label',30,0), $text{'txt_label'},, $text{'txt_p'};
	  print ui_textbox('opt_o',' ',20,0), $text{'txt_other_opt'}, $text{'txt_p'};
	  print ui_textbox('opt_dev','/dev/sdWW /dev/sdXX /dev/sdYY /dev/sdZZ',40,0), $text{'txt_devices'}, $text{'txt_p'};
	  
	  print ui_form_end( [[undef, $text{'mkfs_expert_bt'}]] );
	
	}
	
	 
	ui_print_footer('/', 'Webmin index', '', 'Module menu');
	
}
