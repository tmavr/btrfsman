#!/usr/bin/perl
# btrfsman_label.cgi
# BTRFS Manager - Label Devices

require './btrfsman-lib.pl';
&ReadParse();

ui_print_header(undef, $text{'label_title'}, "", undef, 1, 1);

if($in){
  print $text{'txt_arg'}, $in, $text{'txt_p'};
}

$act = $in{'act'};
$mountpoint =  $in{'mountpoint'};
$newlabel = $in{'newlabel'};

if ((length $newlabel) > 255){
	print "label too long";
}
if ($newlabel =~ /[ %&<>!\x27\x60\x3B\x3A\x\n\r\l]/) {
	print "not a safe string to use as label";
	
}

if (($act eq 'label') && ($mountpoint) ) {
  if ($newlabel) {
    
    $cmd = "btrfs fi label $mountpoint $newlabel 2>&1";
		print $text{txt_executing}, $cmd, $text{'txt_p'};
	  $result=`$cmd`;
	  print $result, $text{'txt_p'};		
	  print $text{'label_changed'}, $text{'txt_p'} ;
  }
}
else{
		  print $text{'index_btrfslogical'};
	show_fs();
	label_menu();
}
ui_print_footer('/', 'Webmin index', '', 'Module menu');




=head1 label_menu

Display label menu

=cut
sub label_menu {
  print $text{'label_mounted_h'};
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

    if ($result =~ /no stats available/) {
      print ui_columns_row([$text{'index_warn'}, $text{'index_warnnoscrub'}]);
    }
    print ui_columns_end();

    print ui_buttons_start();
    print ui_buttons_row("btrfsman_label.cgi",  $text{'label_bt_change'},  $text{'label_bt_change_help'}, ui_hidden('act', 'label'), ui_hidden('mountpoint', @mountedrive[$did]), ui_textbox('newlabel','NewLabel'));
    print ui_buttons_end();

    print "<p><p>";

    $did++;
  }
}
