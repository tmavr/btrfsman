#!/usr/bin/perl
# btrfsman_arr.cgi
# BTRFS Manager - Add Remove Replace Management

require './btrfsman-lib.pl';
&ReadParse();

ui_print_header(undef, $text{'arr_title'}, "", undef, 1, 1);

if($in){
  print $text{'txt_arg'}, $in, $text{'txt_p'};
}

$opt_cmd = $in{'opt_cmd'};
$opt_ad =  $in{'opt_ad'};
$opt_o = $in{'opt_o'};
$opt_dev = $in{'opt_dev'};
$opt_mp = $in{'opt_mp'};
$opt_source_dev =  $in{'opt_source_dev'};
$opt_target_dev = $in{'opt_target_dev'};


#more sanity check would be welcome...
if ($dev =~ /[ %&<>!\x27\x60\x3B\x3A\x\n\r\l]/) {
	print "not a safe string";
}

if (($opt_cmd) && ($opt_ad) && ($opt_dev) && ($opt_mp) ) {

	$cmd = "$opt_cmd $opt_ad $opt_o $opt_dev $opt_mp 2>&1";
	print "Taking Action Executing Command:#", $cmd, $text{'txt_p'};
  $result=`$cmd`;
  print $result;
	
}
else{
	if (($opt_cmd) && ($opt_source_dev) && ($opt_target_dev) && ($opt_mp) ) {
		$cmd = "$opt_cmd $opt_o $opt_source_dev $opt_target_dev $opt_mp 2>&1";
		print "Taking Action Executing Command:#", $cmd, $text{'txt_p'};
	  $result=`$cmd`;
	  print $result;		
  }
	else
	{
		print $text{'arr_h'};	
	  print $text{'arr_help'};
	  
	  show_parted();
	  
	  show_fs();
	
	 	@mountedrive=show_replace_status();
	 	
	
	  print $text{'arr_expert_h'};
	  print $text{'txt_devicesynopsis'}; 
	  print ui_form_start("btrfsman_arr.cgi");
	
	  print ui_hidden('opt_cmd', 'btrfs device'), $text{'txt_p'};
	  print ui_select("opt_ad", 1, [ "add", "delete"]), , $text{'txt_p'};  
	  print ui_textbox('opt_o',' ',20,0), $text{'txt_p'};
	  print ui_textbox('opt_dev','/dev/sdWW /dev/sdXX /dev/sdYY /dev/sdZZ',40,0), $text{'txt_p'};
	  print ui_select('opt_mp', 1, [@mountedrive]), $text{'txt_p'};
	  
	  print ui_form_end( [[undef, $text{'arr_expert_bt'}]] );
	  
	  
	  print $text{'arr_expert_replace_h'};
	  print $text{'arr_expert_replace_help'};  
	  print $text{'txt_replacesynopsis'}; 
	 
	  print ui_form_start("btrfsman_arr.cgi");
	  print ui_hidden('opt_cmd', 'btrfs replace start'), $text{'txt_p'};
	  print ui_textbox('opt_o',' ',20,0), $text{'txt_p'};
	  print ui_textbox('opt_source_dev','/dev/sdSOURCE',40,0), $text{'txt_p'};
	  print ui_textbox('opt_target_dev','/dev/sdTARGET',40,0), $text{'txt_p'};
	  print ui_select('opt_mp', 1, [@mountedrive]), $text{'txt_p'};
	  
	  print ui_form_end( [[undef, $text{'arr_expert_replace_bt'}]] ); 
		
	}

}
 
ui_print_footer('/', 'Webmin index', '', 'Module menu');



=head1 show_replace_status

Display show btrfs replace status

=cut
sub show_replace_status{
	#@mountedrive;
  #print $text{'label_mounted_h'};
  $result = `mount |grep btrfs`;
  $result =~  s/\n/<br>/g;
	
  @splitres = split /<br>/, $result;
  print $text{'index_youhave1'}, scalar (@splitres), $text{'index_youhave3'};
  $did=0;
  for (@splitres){
    print ui_columns_start([ @splitres[$did], ""]);
    $drivea = @splitres[$did];
    @driveb = split /on /, $drivea;
    @drivec = split / /, @driveb[1];
    @mountedrive[$did] =  @drivec[0];
    print ui_columns_row([$text{'index_mountp'}, @mountedrive[$did]]) ;

    $result = `btrfs replace status @mountedrive[$did] -1`;
    $result =~  s/\n/<br>/g;
    print ui_columns_row([$text{'index_btrfsrs'}, $result]);

    print ui_columns_end();

    $did++;
  }
  
  return @mountedrive;
}