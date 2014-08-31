#!/usr/bin/perl
# btrfsman_balance.cgi
# BTRFS Manager - Balance Devices

require './btrfsman-lib.pl';
&ReadParse();

ui_print_header(undef, $text{'balance_title'}, "", undef, 1, 1);

if($in){
  print $text{'txt_arg'}, $in, $text{'txt_p'};
}

$act = $in{'act'};
$mountpoint =  $in{'mountpoint'};
$opt = $in{'opt'};
$opt_m = $in{'opt_m'};
$opt_d = $in{'opt_d'};


if ($mountpoint =~ /[ %&<>!\x27\x60\x3B\x3A\x\n\r\l]/) {
	print "not a safe mountpoint";
}

if (($act) && ($mountpoint) ) {

  $cmd = "btrfs fi $act $opt $opt_m $opt_d $mountpoint 2>&1";
  print  $text{txt_executing}, $cmd, $text{'txt_p'};
  $result=`$cmd`;
  print $cmd, $text{'txt_p'}, $text{'balance_stared'}, $text{'txt_p'} ;
}
else{
	show_fs();
	balancemenu();
}
ui_print_footer('/', 'Webmin index', '', 'Module menu');


=head1 balancemenu

Display balance menu

=cut
sub balancemenu {
  print $text{'balance_h'};
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
 
    $result = `btrfs fi df @mountedrive[$did]`;
    $result =~  s/\n/<br>/g;
    print ui_columns_row([$text{'index_btrfsdf'}, $result]);
    
    $result = `btrfs balance status @mountedrive[$did]`;
    $result =~  s/\n/<br>/g;
    print ui_columns_row([ $text{'index_btrfsbal'} , $result]);

    $result = `btrfs balance status @mountedrive[$did] -v`;
    $result =~  s/\n/<br>/g;
    print ui_columns_row([ $text{'balance_btrfsbal_v'} , $result]);

    print ui_columns_end();

   
    
    if ($result =~ /No balance found on/){
    	
    	#print ui_buttons_start();
	    #print ui_buttons_row("btrfsman_balance.cgi",  $text{'balance_bt_balance'},  $text{'balance_bt_balance_help'}, ui_hidden('act', 'balance start'), ui_hidden('mountpoint', @mountedrive[$did]), ui_textbox('opt',''));
	    #print ui_buttons_end();
    	
    	
    	print $text{'balance_bt_balance_help'}, $text{'balance_bt_balance_raid_help'};
    	print ui_form_start("btrfsman_balance.cgi");
    	
		  #print ui_textbox('act', 'balance start',20,0), $text{'txt_p'};  
		  print ui_hidden('act', 'balance start');
	    print ui_hidden('mountpoint', @mountedrive[$did]), $text{'txt_p'};
	    print ui_textbox('opt_o',' ',20,0), $text{'txt_other_opt'}, $text{'txt_p'};
	    print ui_select('opt_m', 1, ["", "-mconvert=raid10", "-mconvert=raid1", "-mconvert=raid0", "-mconvert=single", "-mconvert=raid5", "-mconvert=raid6"]), $text{'txt_metadata'}, $text{'txt_p'};
	    print ui_select('opt_d', 1, ["", "-dconvert=raid10", "-dconvert=raid1", "-dconvert=raid0", "-dconvert=single", "-dconvert=raid5", "-dconvert=raid6"]), $text{'txt_data'}, $text{'txt_p'};
	    #print ui_textbox('opt_dev','/dev/sdWW /dev/sdXX /dev/sdYY /dev/sdZZ',40,0), $text{'txt_devices'}, $text{'txt_p'};
	  
	    print ui_form_end( [[undef, $text{'balance_bt_balance_raid'}]] );
    	
    }
    else {
    	print ui_buttons_start();
      print ui_buttons_row("btrfsman_balance.cgi",  $text{'balance_bt_pause'},  $text{'balance_bt_pause_help'}, ui_hidden('act', 'balance pause'), ui_hidden('mountpoint', @mountedrive[$did]));
      print ui_buttons_row("btrfsman_balance.cgi",  $text{'balance_bt_resume'},  $text{'balance_bt_resume_help'}, ui_hidden('act', 'balance resume'), ui_hidden('mountpoint', @mountedrive[$did]));
      print ui_buttons_row("btrfsman_balance.cgi",  $text{'balance_bt_cancel'},  $text{'balance_bt_cancel_help'}, ui_hidden('act', 'balance cancel'), ui_hidden('mountpoint', @mountedrive[$did]));
      print ui_buttons_end();
    }
    
    

    print $text{'txt_p'};

    $did++;
  }
  
  
}
