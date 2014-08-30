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


if ($mountpoint =~ /[ %&<>!\x27\x60\x3B\x3A\x\n\r\l]/) {
	print "not a safe mountpoint";
}

if (($act) && ($mountpoint) ) {
  #if ($newlabel) {
    print "Taking Action Executing Command:#", $text{'txt_p'};
    print "btrfs fi $act $mountpoint $opt", $text{'txt_p'};
    print $text{'balance_stared'}, $text{'txt_p'} ;
  #}
}
else{
	
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

    $result = `btrfs balance status @mountedrive[$did]`;
    $result =~  s/\n/<br>/g;
    print ui_columns_row([ $text{'index_btrfsbal'} , $result]);

    $result = `btrfs balance status @mountedrive[$did] -v`;
    $result =~  s/\n/<br>/g;
    print ui_columns_row([ $text{'balance_btrfsbal_v'} , $result]);

    print ui_columns_end();

    print ui_buttons_start();
    
    if ($result =~ /No balance found on/){
    	print ui_buttons_row("btrfsman_balance.cgi",  $text{'balance_bt_balance'},  $text{'balance_bt_balance_help'}, ui_hidden('act', 'balance start'), ui_hidden('mountpoint', @mountedrive[$did]), ui_textbox('opt',''));
    	
    }
    else {
      print ui_buttons_row("btrfsman_balance.cgi",  $text{'balance_bt_pause'},  $text{'balance_bt_pause_help'}, ui_hidden('act', 'balance pause'), ui_hidden('mountpoint', @mountedrive[$did]));
      print ui_buttons_row("btrfsman_balance.cgi",  $text{'balance_bt_resume'},  $text{'balance_bt_resume_help'}, ui_hidden('act', 'balance resume'), ui_hidden('mountpoint', @mountedrive[$did]));
      print ui_buttons_row("btrfsman_balance.cgi",  $text{'balance_bt_cancel'},  $text{'balance_bt_cancel_help'}, ui_hidden('act', 'balance cancel'), ui_hidden('mountpoint', @mountedrive[$did]));
    }
    
    print ui_buttons_end();

    print $text{'txt_p'};

    $did++;
  }
  
  print "<h1>CONVERT TO: -dconvert=raid1 -mconvert=raid1 /mnt</h1>";
}
